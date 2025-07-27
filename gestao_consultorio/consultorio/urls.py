from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Agora login é a página principal
    path('index/', views.index, name='index'),  # Página protegida, por exemplo
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('consulta/', views.consulta_view, name='consulta'),
    path('agenda/', views.lista_consultas, name='lista_consultas'),
    path('agendar/', views.agendar_consulta_view, name='agendar_consulta'),
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/cadastrar/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('pacientes/editar/<int:paciente_id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/excluir/<int:id>/', views.excluir_paciente, name='excluir_paciente'),
    path('consulta/editar/<int:consulta_id>/', views.editar_consulta, name='editar_consulta'),
    path('consulta/excluir/<int:id>/', views.excluir_consulta, name='excluir_consulta'),
    path('prontuarios/', views.lista_prontuarios, name='lista_prontuarios'),
    path('prontuarios/novo/', views.criar_prontuario, name='criar_prontuario'),
    path('profissionais/', views.lista_profissionais, name='lista_profissionais'),
    path('profissionais/novo/', views.cadastrar_profissional, name='cadastrar_profissional'),
    path('profissionais/editar/<int:id>/', views.editar_profissional, name='editar_profissional'),
    path('profissionais/excluir/<int:id>/', views.excluir_profissional, name='excluir_profissional'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/novo/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produtos/editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('produtos/excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),
    path('pendencias/', views.pendencias_view, name='pendencias'),
    path('pendencias/excluir/<int:pendencia_id>/', views.excluir_pendencia, name='excluir_pendencia'),
   path('historico-medico/', views.historico_medico_view, name='historico_medico'),








    


]
