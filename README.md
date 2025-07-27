🏥 Sistema de Gestão de Consultório Sistema desenvolvido com Django para gerenciar pacientes, agendamentos, prontuários, histórico médico e envio de lembretes por e-mail.

✅ Pré-requisitos Antes de rodar o sistema, certifique-se de que o computador tenha:

Python 3.10 ou superior


📥 Como executar o projeto

Copie ou baixe a pasta do projeto
Você pode clonar do GitHub:

bash Copiar Editar git clone https://github.com/seu-usuario/seu-repositorio.git cd seu-repositorio Ou apenas copiar a pasta completa para outro computador.

Crie um ambiente virtual (recomendado)
bash Copiar Editar python -m venv venv Ative o ambiente virtual:

Windows:

bash Copiar Editar venv\Scripts\activate Linux/Mac:

bash Copiar Editar source venv/bin/activate 3. Instale o Django bash Copiar Editar pip install django 4. Aplique as migrações do banco de dados bash Copiar Editar python manage.py migrate 5. (Opcional) Crie um superusuário bash Copiar Editar python manage.py createsuperuser Esse usuário permite acessar o painel de administração do Django.

Execute o servidor
bash Copiar Editar python manage.py runserver Acesse o sistema no navegador:

cpp Copiar Editar http://127.0.0.1:8000/
