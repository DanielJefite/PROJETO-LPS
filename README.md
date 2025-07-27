## 🏥 Sistema de Gestão de Consultório

Sistema desenvolvido com Django para gerenciar pacientes, agendamentos, prontuários, histórico médico e envio de lembretes por e-mail.

----------

### ✅ Pré-requisitos

Antes de rodar o sistema, certifique-se de que o computador tenha:

-   Python 3.10 ou superior
    
-   Git (opcional, se for clonar do GitHub)
    

----------

### 📥 Como executar o projeto

#### 1. Copie ou baixe a pasta do projeto

Você pode clonar do GitHub:

bash

CopiarEditar

`git clone https://github.com/seu-usuario/seu-repositorio.git cd seu-repositorio` 

Ou apenas copiar a pasta completa para outro computador.

----------

#### 2. Crie um ambiente virtual (recomendado)

bash

CopiarEditar

`python -m venv venv` 

Ative o ambiente virtual:

-   **Windows:**
    
    bash
    
    CopiarEditar
    
    `venv\Scripts\activate` 
    
-   **Linux/Mac:**
    
    bash
    
    CopiarEditar
    
    `source venv/bin/activate` 
    

----------

#### 3. Instale o Django

bash

CopiarEditar

`pip install django` 

----------

#### 4. Aplique as migrações do banco de dados

bash

CopiarEditar

`python manage.py migrate` 

----------

#### 5. (Opcional) Crie um superusuário

bash

CopiarEditar

`python manage.py createsuperuser` 

Esse usuário permite acessar o painel de administração do Django.

----------

#### 6. Execute o servidor

bash

CopiarEditar

`python manage.py runserver` 

Acesse o sistema no navegador:

cpp

CopiarEditar

`http://127.0.0.1:8000/` 

----------

### ✉️ Envio de lembretes por e-mail

Para funcionar, o e-mail precisa estar configurado no arquivo `settings.py`:

python

CopiarEditar

`EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' EMAIL_HOST = 'smtp.gmail.com' EMAIL_PORT = 587 EMAIL_USE_TLS = True EMAIL_HOST_USER = 'seuemail@gmail.com' EMAIL_HOST_PASSWORD = 'senhaouapppassword' DEFAULT_FROM_EMAIL = EMAIL_HOST_USER` 

> 💡 Dica: se usar Gmail, ative a verificação em duas etapas e gere uma senha de aplicativo (App Password).

----------

### 👨‍💻 Tecnologias utilizadas

-   Python 3.10+
    
-   Django 5.x
    
-   SQLite
    
-   HTML/CSS
    
-   SMTP (para envio de e-mails)
    

----------

### 📄 Licença

Projeto acadêmico desenvolvido com fins educacionais.
