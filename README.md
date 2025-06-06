# Gargantua - ITSMTools

Sistema de gerenciamento de usuários e ferramentas de rede desenvolvido em Django com interface dark mode e autenticação baseada em arquivo JSON.

## 🚀 Características

- **Autenticação Customizada**: Sistema de login baseado em arquivo JSON (sem banco de dados)
- **Interface Dark Mode**: Design moderno com Bootstrap 5 e tema escuro
- **Menu Lateral Responsivo**: Navegação intuitiva com sidebar colapsível
- **Ferramentas de Rede**: Suite completa de ferramentas para diagnóstico de rede
- **Gerenciamento de Usuários**: CRUD completo para administração de usuários

## 🛠️ Ferramentas de Rede Incluídas

- **Ping**: Verificação básica de conectividade e tempo de resposta
- **Traceroute**: Análise de rota de pacotes até o destino
- **Port Scanner**: Verificação de portas abertas, fechadas ou filtradas
- **Nmap**: Escaneamento avançado de rede com detecção de serviços
- **DNS Lookup**: Consulta de diversos tipos de registros DNS
- **HTTP Headers**: Análise de cabeçalhos de resposta HTTP
- **SSL Certificate Check**: Verificação de certificados SSL/TLS
- **Geolocalização IP**: Localização geográfica de endereços IP
- **Monitoramento de Latência**: Verificação contínua de tempo de resposta

## 📋 Pré-requisitos

- Python 3.11+
- Django 4.2.16
- PyYAML
- Ferramentas de sistema: traceroute, nmap, dnsutils

## 🔧 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/gargantua.git
cd gargantua
```

2. **Instale as dependências Python**
```bash
pip install -r requirements.txt
```

3. **Instale as ferramentas de sistema (Ubuntu/Debian)**
```bash
sudo apt-get update
sudo apt-get install traceroute nmap dnsutils
```

4. **Execute as migrações**
```bash
python manage.py migrate
```

5. **Inicie o servidor**
```bash
python manage.py runserver
```

## 👤 Usuário Padrão

- **Usuário**: admin
- **Senha**: 12345679

## 📁 Estrutura do Projeto

```
gargantua/
├── accounts/                 # App de autenticação
│   ├── backends.py          # Backend de autenticação customizado
│   ├── models.py            # Modelo de usuário JSON
│   ├── views.py             # Views de autenticação
│   └── forms.py             # Formulários
├── network_tools/           # App de ferramentas de rede
│   ├── views.py             # Views das ferramentas
│   └── urls.py              # URLs das ferramentas
├── templates/               # Templates HTML
│   ├── base.html            # Template base com sidebar
│   ├── registration/        # Templates de login
│   ├── accounts/            # Templates de usuários
│   └── network_tools/       # Templates das ferramentas
├── users.json               # Arquivo de usuários
├── requirements.txt         # Dependências Python
└── manage.py               # Script de gerenciamento Django
```

## 🔐 Sistema de Autenticação

O sistema utiliza um backend de autenticação customizado que armazena usuários em arquivo JSON em vez de banco de dados relacional. Características:

- Hash de senhas com PBKDF2
- Backup automático do arquivo de usuários
- Validação de senhas seguras
- Geração de senhas aleatórias
- Suporte a diferentes níveis de acesso

## 🎨 Interface

- **Design**: Bootstrap 5 com tema dark mode
- **Responsivo**: Adaptável para desktop e mobile
- **Sidebar**: Menu lateral colapsível com categorias organizadas
- **Ícones**: Bootstrap Icons para interface consistente
- **Animações**: Transições suaves e efeitos hover

## 🔧 Configuração

### Arquivo de Usuários (users.json)

```json
{
  "admin": {
    "username": "admin",
    "password": "hash_da_senha",
    "email": "admin@exemplo.com",
    "is_staff": true,
    "is_active": true,
    "date_joined": "2025-06-06T10:00:00Z"
  }
}
```

### Configurações Django

- **CSRF_TRUSTED_ORIGINS**: Configurado para domínios proxy
- **AUTHENTICATION_BACKENDS**: Backend customizado para JSON
- **ALLOWED_HOSTS**: Configurado para aceitar qualquer host

## 🚀 Deploy

O sistema pode ser facilmente deployado em qualquer servidor que suporte Django. Certifique-se de:

1. Configurar as variáveis de ambiente adequadas
2. Instalar as ferramentas de sistema necessárias
3. Configurar um servidor web (nginx/apache) se necessário
4. Ajustar as configurações de CSRF e ALLOWED_HOSTS

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas, abra uma issue no repositório do GitHub.

---

**Gargantua** - ITSMTools para diagnóstico e gerenciamento de rede

