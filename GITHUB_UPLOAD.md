# Gargantua - ITSMTools

## Arquivos para Upload no GitHub

Este diretório contém todos os arquivos necessários para fazer upload do projeto Gargantua no GitHub.

### Estrutura do Projeto

- **accounts/**: App Django para autenticação de usuários
- **network_tools/**: App Django com ferramentas de rede
- **templates/**: Templates HTML com Bootstrap 5 e dark mode
- **gargantua_users/**: Configurações principais do Django
- **users.json**: Arquivo de usuários (admin/12345679)
- **requirements.txt**: Dependências Python
- **manage.py**: Script de gerenciamento Django

### Como usar

1. Faça upload de todos os arquivos para seu repositório GitHub
2. Clone o repositório em seu servidor
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute: `python manage.py runserver`
5. Acesse com admin/12345679

### Funcionalidades Implementadas

✅ Sistema de autenticação baseado em JSON
✅ Interface dark mode com Bootstrap 5
✅ Menu lateral responsivo com ferramentas de rede
✅ Layout completo e funcional
✅ Redirecionamento após login para dashboard

### Próximos Passos

- Implementar funcionalidades das ferramentas de rede
- Adicionar validações e tratamento de erros
- Melhorar interface e experiência do usuário

