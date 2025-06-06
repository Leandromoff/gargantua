import json
import os
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings


class JSONUser:
    """Classe que representa um usuário armazenado em JSON"""
    
    def __init__(self, username, email, password_hash, is_admin_site=False, 
                 is_active=True, created_at=None, roles=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin_site = is_admin_site
        self.is_active = is_active
        self.created_at = created_at or datetime.now().isoformat()
        self.roles = roles or []
        
    def check_password(self, raw_password):
        """Verifica se a senha fornecida está correta"""
        return check_password(raw_password, self.password_hash)
    
    def set_password(self, raw_password):
        """Define uma nova senha (com hash)"""
        self.password_hash = make_password(raw_password)
    
    def to_dict(self):
        """Converte o usuário para dicionário"""
        return {
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'is_admin_site': self.is_admin_site,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'roles': self.roles
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria um usuário a partir de um dicionário"""
        return cls(
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            is_admin_site=data.get('is_admin_site', False),
            is_active=data.get('is_active', True),
            created_at=data.get('created_at'),
            roles=data.get('roles', [])
        )


class UserManager:
    """Gerenciador de usuários para arquivo JSON"""
    
    def __init__(self, file_path=None):
        self.file_path = file_path or settings.USERS_FILE
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Garante que o arquivo de usuários existe"""
        if not os.path.exists(self.file_path):
            self._save_users({})
    
    def _load_users(self):
        """Carrega usuários do arquivo JSON"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {username: JSONUser.from_dict(user_data) 
                       for username, user_data in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_users(self, users):
        """Salva usuários no arquivo JSON"""
        data = {username: user.to_dict() for username, user in users.items()}
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_user(self, username):
        """Obtém um usuário pelo username"""
        users = self._load_users()
        return users.get(username)
    
    def create_user(self, username, email, password, is_admin_site=False, roles=None):
        """Cria um novo usuário"""
        users = self._load_users()
        
        if username in users:
            raise ValueError(f"Usuário '{username}' já existe")
        
        user = JSONUser(
            username=username,
            email=email,
            password_hash=make_password(password),
            is_admin_site=is_admin_site,
            roles=roles or []
        )
        
        users[username] = user
        self._save_users(users)
        return user
    
    def update_user(self, username, **kwargs):
        """Atualiza um usuário existente"""
        users = self._load_users()
        
        if username not in users:
            raise ValueError(f"Usuário '{username}' não encontrado")
        
        user = users[username]
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        users[username] = user
        self._save_users(users)
        return user
    
    def delete_user(self, username):
        """Remove um usuário"""
        users = self._load_users()
        
        if username not in users:
            raise ValueError(f"Usuário '{username}' não encontrado")
        
        del users[username]
        self._save_users(users)
    
    def list_users(self):
        """Lista todos os usuários"""
        users = self._load_users()
        return list(users.values())
    
    def authenticate(self, username, password):
        """Autentica um usuário"""
        user = self.get_user(username)
        
        if user and user.is_active and user.check_password(password):
            return user
        
        return None

