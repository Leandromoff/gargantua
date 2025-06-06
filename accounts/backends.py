from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from .models import UserManager


class JSONFileUser:
    """Classe que adapta JSONUser para o sistema de autenticação do Django"""
    
    def __init__(self, json_user):
        self.json_user = json_user
        self.username = json_user.username
        self.email = json_user.email
        self.is_active = json_user.is_active
        self.is_staff = json_user.is_admin_site
        self.is_superuser = json_user.is_admin_site
        # Usar hash do username como ID numérico para compatibilidade
        self.pk = abs(hash(json_user.username)) % (10 ** 8)
        self.id = self.pk
        self.last_login = timezone.now()
        
        # Adicionar atributos necessários para o sistema de sessão do Django
        self.backend = 'accounts.backends.JSONFileBackend'
        
        # Simular o atributo _meta para compatibilidade com o sistema de sessão
        class Meta:
            def __init__(self, user):
                self.user = user
                
            @property
            def pk(self):
                return PKMeta(self.user)
        
        class PKMeta:
            def __init__(self, user):
                self.user = user
                
            def value_to_string(self, obj):
                return str(obj.pk)
        
        self._meta = Meta(self)
    
    def __str__(self):
        return self.username
    
    def get_username(self):
        return self.username
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def check_password(self, raw_password):
        return self.json_user.check_password(raw_password)
    
    def set_password(self, raw_password):
        self.json_user.set_password(raw_password)
        # Salvar no arquivo
        user_manager = UserManager()
        user_manager.update_user(
            self.username,
            password_hash=self.json_user.password_hash
        )
    
    def save(self, update_fields=None):
        """Método save para compatibilidade com Django (não faz nada)"""
        pass
    
    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def has_perms(self, perm_list, obj=None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return self.is_staff


class JSONFileBackend(BaseBackend):
    """Backend de autenticação que usa arquivo JSON"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        user_manager = UserManager()
        json_user = user_manager.authenticate(username, password)
        
        if json_user:
            return JSONFileUser(json_user)
        
        return None
    
    def get_user(self, user_id):
        # Converter o ID numérico de volta para username
        user_manager = UserManager()
        all_users = user_manager.list_users()
        
        # Se all_users for uma lista, converter para dicionário
        if isinstance(all_users, list):
            users_dict = {}
            for user_data in all_users:
                if isinstance(user_data, dict) and 'username' in user_data:
                    users_dict[user_data['username']] = user_data
            all_users = users_dict
        
        for username, user_data in all_users.items():
            if abs(hash(username)) % (10 ** 8) == int(user_id):
                json_user = user_manager.get_user(username)
                if json_user and json_user.is_active:
                    return JSONFileUser(json_user)
        
        return None

