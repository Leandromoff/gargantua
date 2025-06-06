# Documentação Técnica - Gargantua

## Arquitetura do Sistema

O sistema Gargantua foi desenvolvido seguindo os princípios de arquitetura limpa e padrões do Django, com algumas adaptações para utilizar arquivos JSON como fonte de dados em vez de banco de dados relacional.

### Componentes Principais

#### 1. Backend de Autenticação Customizado (`accounts/backends.py`)

O sistema implementa um backend de autenticação personalizado que substitui o sistema padrão do Django. Este backend é responsável por:

- Autenticar usuários contra o arquivo JSON
- Gerenciar sessões de usuário
- Converter IDs de usuário para compatibilidade com o sistema de sessões do Django

A classe `JSONFileUser` adapta os dados do arquivo JSON para o formato esperado pelo Django, incluindo:
- Atributos necessários para autenticação (`is_authenticated`, `is_active`, etc.)
- Métodos de compatibilidade (`save`, `has_perm`, etc.)
- Conversão de IDs string para numéricos para compatibilidade com sessões

#### 2. Gerenciador de Usuários (`accounts/models.py`)

O `UserManager` é responsável por todas as operações CRUD no arquivo JSON:

- **Leitura**: Carrega dados do arquivo JSON com tratamento de erros
- **Escrita**: Salva dados no arquivo com backup automático
- **Validação**: Verifica integridade dos dados antes de salvar
- **Autenticação**: Verifica credenciais usando hash seguro

A classe `JSONUser` representa um usuário individual com métodos para:
- Verificação de senha usando PBKDF2
- Definição de nova senha com hash automático
- Validação de dados do usuário

#### 3. Views e Controle de Acesso (`accounts/views.py`)

O sistema implementa views baseadas em função com decoradores de autenticação:

- **LoginView**: Processa autenticação e redireciona usuários
- **UserListView**: Lista usuários (apenas para administradores)
- **CreateUserView**: Criação de novos usuários com geração de senha
- **ChangePasswordView**: Alteração de senha com validação
- **ToggleUserView**: Ativação/desativação de usuários

Todas as views administrativas são protegidas com o decorador `@login_required` e verificação de permissões.

#### 4. Formulários e Validação (`accounts/forms.py`)

Os formulários implementam validação tanto no frontend quanto no backend:

- **LoginForm**: Validação de credenciais
- **CreateUserForm**: Validação de dados de usuário com verificação de duplicatas
- **ChangePasswordForm**: Validação de senha atual e nova senha

#### 5. Templates e Interface (`templates/`)

A interface utiliza Bootstrap 5 com tema escuro personalizado:

- **Template Base**: Estrutura comum com navegação e modo escuro
- **Templates Específicos**: Formulários responsivos e acessíveis
- **JavaScript**: Funcionalidades interativas e validação client-side

### Fluxo de Dados

1. **Autenticação**:
   - Usuário submete credenciais via formulário
   - View processa dados e chama backend customizado
   - Backend verifica credenciais no arquivo JSON
   - Sessão é criada e usuário é redirecionado

2. **Operações CRUD**:
   - View recebe requisição HTTP
   - Dados são validados via formulários Django
   - UserManager executa operação no arquivo JSON
   - Resposta é retornada ao usuário

3. **Persistência**:
   - Dados são mantidos em arquivo JSON
   - Backup automático antes de modificações
   - Validação de integridade após escrita

### Segurança

#### Autenticação e Autorização

- Senhas são armazenadas usando PBKDF2 com salt aleatório
- Sessões são gerenciadas pelo sistema padrão do Django
- Verificação de permissões em todas as operações administrativas

#### Proteção contra Ataques

- **CSRF**: Tokens CSRF em todos os formulários
- **XSS**: Escape automático de dados no template
- **Injection**: Validação rigorosa de entrada de dados

#### Validação de Dados

- Validação de email com regex
- Verificação de força de senha
- Sanitização de entrada de usuário

### Performance e Escalabilidade

#### Otimizações Implementadas

- Cache de dados de usuário em memória durante requisição
- Leitura lazy do arquivo JSON
- Validação incremental de dados

#### Limitações

- Arquivo JSON não é adequado para grandes volumes de usuários (>1000)
- Operações de escrita são síncronas e podem causar bloqueio
- Não há suporte nativo para transações

#### Recomendações para Produção

Para ambientes de produção com mais usuários, recomenda-se:

1. **Migração para Banco de Dados**: Implementar modelos Django tradicionais
2. **Cache**: Utilizar Redis ou Memcached para cache de sessões
3. **Load Balancing**: Distribuir carga entre múltiplos servidores
4. **Monitoramento**: Implementar logs detalhados e métricas

### Manutenção e Extensibilidade

#### Adicionando Novas Funcionalidades

1. **Novos Campos de Usuário**:
   - Adicionar campo na classe `JSONUser`
   - Atualizar formulários e templates
   - Implementar migração de dados

2. **Novas Views**:
   - Criar view seguindo padrão existente
   - Adicionar URL em `urls.py`
   - Criar template correspondente

3. **Validações Customizadas**:
   - Implementar em `validators.py`
   - Adicionar aos formulários relevantes

#### Testes

O sistema deve incluir testes para:

- Autenticação e autorização
- Operações CRUD de usuários
- Validação de formulários
- Integridade de dados

#### Backup e Recuperação

- Implementar backup automático do arquivo JSON
- Criar scripts de recuperação de dados
- Monitorar integridade do arquivo

### Configuração de Ambiente

#### Desenvolvimento

```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

#### Produção

```python
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']
SECRET_KEY = 'chave-secreta-forte'
CSRF_TRUSTED_ORIGINS = ['https://seu-dominio.com']
```

### Monitoramento e Logs

O sistema deve implementar logging para:

- Tentativas de login (sucesso e falha)
- Operações administrativas
- Erros de sistema
- Performance de operações

### Conclusão

O sistema Gargantua fornece uma solução robusta para gerenciamento de usuários em aplicações de pequeno a médio porte. A arquitetura modular permite fácil manutenção e extensão, enquanto as práticas de segurança implementadas garantem proteção adequada dos dados dos usuários.

Para implementações futuras, recomenda-se considerar a migração para banco de dados relacional quando o número de usuários exceder 500-1000 registros, mantendo a mesma interface e funcionalidades já desenvolvidas.

