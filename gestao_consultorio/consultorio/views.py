from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Consulta
from datetime import datetime
from .models import Paciente
from django.shortcuts import get_object_or_404
from .models import Prontuario, Paciente
from .models import Profissional
from .models import Produto
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Consulta, Paciente, Profissional  # ajuste se seu model de médico for diferente
from datetime import datetime, time
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from .models import Pendencia, Paciente
from .models import Consulta, Prontuario

def login_view(request):
    if request.method == 'POST':
        identificador = request.POST.get('username')  # pode ser username ou email
        senha = request.POST.get('password')

        # Tenta autenticar por nome de usuário
        user = authenticate(request, username=identificador, password=senha)

        if not user:
            # Tenta autenticar por e-mail
            user_obj = User.objects.filter(email=identificador).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=senha)

        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Credenciais inválidas. Verifique e tente novamente.')
            return redirect('login')

    return render(request, 'consultorio/login.html')


def index(request):
    return render(request, 'consultorio/index.html')


def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verifica se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já está em uso.')
            return redirect('cadastro')

        # Verifica se o e-mail já está em uso
        if User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
            return redirect('cadastro')

        # Validação de senha forte com mensagem única
        try:
            validate_password(password, user=User(username=username, email=email))
        except ValidationError:
            messages.error(request, 'A senha não atende aos critérios de segurança.')
            return redirect('cadastro')

        # Cria o novo usuário
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Usuário cadastrado com sucesso! Faça login.')
        return redirect('login')

    return render(request, 'consultorio/cadastro.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def consulta_view(request):
    if request.method == 'POST':
        paciente = request.POST.get('paciente')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        motivo = request.POST.get('motivo')

        # Você pode salvar isso em um modelo depois
        print(f"Consulta agendada: {paciente}, {data} às {hora} - Motivo: {motivo}")
        return redirect('index')  # Redireciona após agendar

    return render(request, 'consultorio/consulta.html')

def lista_consultas(request):
    data_filtro = request.GET.get('data')
    profissional_id = request.GET.get('profissional')

    consultas = Consulta.objects.all()

    if data_filtro:
        consultas = consultas.filter(data_hora__date=parse_date(data_filtro))

    if profissional_id:
        consultas = consultas.filter(medico_id=profissional_id)

    consultas = consultas.order_by('data_hora')

    profissionais = Profissional.objects.all()

    return render(request, 'consultorio/agenda.html', {
        'consultas': consultas,
        'data_filtro': data_filtro,
        'profissionais': profissionais,
        'profissional_id': profissional_id,
    })


def agendar_consulta_view(request):
    # Só pacientes ativos devem ser mostrados
    pacientes = Paciente.objects.filter(status='ativo')
    profissionais = Profissional.objects.all()

    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        medico_id = request.POST.get('medico')
        data_str = request.POST.get('data')
        horario_str = request.POST.get('horario')
        descricao = request.POST.get('descricao')

        try:
            paciente = Paciente.objects.get(id=paciente_id, status='ativo')  # valida se é ativo
            profissional = Profissional.objects.get(id=medico_id)
        except Paciente.DoesNotExist:
            messages.error(request, 'Paciente inválido ou inativo.')
            return redirect('agendar_consulta')
        except Profissional.DoesNotExist:
            messages.error(request, 'Profissional inválido.')
            return redirect('agendar_consulta')

        if data_str and horario_str:
            data_hora_str = f"{data_str} {horario_str}"
            data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')

            if data_hora.weekday() >= 5:
                messages.error(request, 'Consultas devem ser agendadas em dias úteis.')
                return redirect('agendar_consulta')

            if not (8 <= data_hora.hour < 18):
                messages.error(request, 'Horário fora do expediente (08h às 18h).')
                return redirect('agendar_consulta')

            if Consulta.objects.filter(medico=profissional, data_hora=data_hora).exists():
                messages.error(request, 'Este horário já está ocupado para esse profissional.')
                return redirect('agendar_consulta')

            Consulta.objects.create(
                paciente=paciente,
                medico=profissional,
                data_hora=data_hora,
                descricao=descricao
            )
            messages.success(request, 'Consulta agendada com sucesso!')
            return redirect('lista_consultas')

    return render(request, 'consultorio/agendar.html', {
        'pacientes': pacientes,
        'profissionais': profissionais
    })

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'consultorio/pacientes.html', {'pacientes': pacientes})



def cadastrar_paciente(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        telefone = request.POST['telefone']
        cpf = request.POST['cpf']
        data_nascimento = request.POST['data_nascimento']
        convenio = request.POST['convenio']

        # Verifica se já existe paciente com o email informado
        if Paciente.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado para outro paciente.')
            return redirect('cadastrar_paciente')

        Paciente.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            cpf=cpf,
            data_nascimento=data_nascimento,
            convenio=convenio
        )
        messages.success(request, 'Paciente cadastrado com sucesso!')
        return redirect('lista_pacientes')
    return render(request, 'consultorio/cadastrar_paciente.html')

def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        paciente.nome = request.POST.get('nome')
        paciente.email = request.POST.get('email')
        paciente.telefone = request.POST.get('telefone')
        paciente.cpf = request.POST.get('cpf')
        paciente.data_nascimento = request.POST.get('data_nascimento')
        paciente.convenio = request.POST.get('convenio')
        paciente.status = request.POST.get('status')  # <-- ADICIONADO
        paciente.save()
        return redirect('lista_pacientes')

    return render(request, 'consultorio/editar_paciente.html', {'paciente': paciente})



def excluir_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    paciente.delete()
    return redirect('lista_pacientes')

def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    pacientes = Paciente.objects.all()
    profissionais = Profissional.objects.all()

    if request.method == "POST":
        paciente_id = request.POST.get('paciente')
        medico_id = request.POST.get('medico')
        data_hora_str = request.POST.get('data_hora')
        descricao = request.POST.get('descricao')

        paciente = get_object_or_404(Paciente, id=paciente_id)
        medico = get_object_or_404(Profissional, id=medico_id)

        data_hora = datetime.strptime(data_hora_str, '%Y-%m-%dT%H:%M')

        consulta.paciente = paciente
        consulta.medico = medico
        consulta.data_hora = data_hora
        consulta.descricao = descricao
        consulta.save()

        return redirect('lista_consultas')

    context = {
        'consulta': consulta,
        'pacientes': pacientes,
        'profissionais': profissionais,
    }
    return render(request, 'consultorio/editar_consulta.html', context)


def excluir_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    consulta.delete()
    return redirect('lista_consultas')


def lista_prontuarios(request):
    prontuarios = Prontuario.objects.all()
    return render(request, 'consultorio/lista_prontuarios.html', {'prontuarios': prontuarios})


def criar_prontuario(request):
    pacientes = Paciente.objects.all()

    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        data = request.POST.get('data')
        diagnostico = request.POST.get('diagnostico')
        prescricao = request.POST.get('prescricao')

        # Busca o paciente ou retorna 404 se não existir
        paciente = get_object_or_404(Paciente, id=paciente_id)

        # Converte a data (se precisar)
        if data:
            data_prontuario = datetime.strptime(data, '%Y-%m-%d').date()
        else:
            data_prontuario = None  # ou defina a data atual

        # Crie o prontuário e salve no banco
        Prontuario.objects.create(
            paciente=paciente,
            data=data_prontuario,
            diagnostico=diagnostico,
            prescricao=prescricao
        )
        return redirect('lista_prontuarios')

    return render(request, 'consultorio/criar_prontuario.html', {'pacientes': pacientes})


def lista_profissionais(request):
    profissionais = Profissional.objects.all()
    return render(request, 'consultorio/profissionais.html', {'profissionais': profissionais})

def cadastrar_profissional(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        telefone = request.POST['telefone']
        especialidade = request.POST['especialidade']
        Profissional.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            especialidade=especialidade
        )
        return redirect('lista_profissionais')
    return render(request, 'consultorio/cadastrar_profissional.html')


def editar_profissional(request, id):
    profissional = get_object_or_404(Profissional, id=id)

    if request.method == 'POST':
        profissional.nome = request.POST.get('nome')
        profissional.especialidade = request.POST.get('especialidade')
        profissional.email = request.POST.get('email')
        profissional.telefone = request.POST.get('telefone')
        profissional.save()
        return redirect('lista_profissionais')  # redireciona para a lista após salvar

    return render(request, 'consultorio/editar_profissional.html', {'profissional': profissional})


def excluir_profissional(request, id):
    profissional = get_object_or_404(Profissional, id=id)
    profissional.delete()
    return redirect('lista_profissionais')

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'consultorio/lista_produtos.html', {'produtos': produtos})

def cadastrar_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        quantidade = request.POST.get('quantidade')

        Produto.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            quantidade=quantidade
        )
        return redirect('lista_produtos')

    return render(request, 'consultorio/cadastrar_produto.html')

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        produto.preco = request.POST.get('preco')
        produto.quantidade = request.POST.get('quantidade')
        produto.save()
        return redirect('lista_produtos')

    return render(request, 'consultorio/editar_produto.html', {'produto': produto})

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('lista_produtos')


def pendencias_view(request):
    pacientes = Paciente.objects.filter(status='ativo')
    pendencias = Pendencia.objects.all().order_by('-data_criacao')

    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        descricao = request.POST.get('descricao')

        paciente = get_object_or_404(Paciente, id=paciente_id)
        Pendencia.objects.create(paciente=paciente, descricao=descricao)
        messages.success(request, 'Pendência registrada com sucesso.')
        return redirect('pendencias')

    return render(request, 'consultorio/pendencias.html', {
        'pacientes': pacientes,
        'pendencias': pendencias
    })


def excluir_pendencia(request, pendencia_id):
    pendencia = get_object_or_404(Pendencia, id=pendencia_id)

    if request.method == 'POST':
        pendencia.delete()
        messages.success(request, 'Pendência excluída com sucesso.')
    return redirect('pendencias')

def historico_medico_view(request):
    pacientes = pacientes = Paciente.objects.all().order_by('nome') # Exibe apenas pacientes ativos
    paciente_id = request.GET.get('paciente')
    consultas = prontuarios = None

    if paciente_id:
        consultas = Consulta.objects.filter(paciente_id=paciente_id).select_related('medico').order_by('-data_hora')
        prontuarios = Prontuario.objects.filter(paciente_id=paciente_id).order_by('-data')

    return render(request, 'consultorio/historico_medico.html', {
        'pacientes': pacientes,
        'consultas': consultas,
        'prontuarios': prontuarios,
        'paciente_selecionado': paciente_id
    })