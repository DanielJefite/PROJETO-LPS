from django.db import models

class Paciente(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    convenio = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')  # novo campo

    def __str__(self):
        return self.nome


class Profissional(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"Consulta de {self.paciente.nome} com {self.medico.nome} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

class Prontuario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    diagnostico = models.TextField()
    prescricao = models.TextField()

    def __str__(self):
        return f"Prontuário de {self.paciente.nome} em {self.data.strftime('%d/%m/%Y')}"

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Pendencia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    descricao = models.TextField()
    resolvida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.paciente.nome} - {'Resolvida' if self.resolvida else 'Pendente'}"


