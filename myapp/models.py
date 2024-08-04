from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    cor = models.CharField(max_length=7)  # Hex code para a cor

    def __str__(self):
        return self.nome

class MyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    description = models.CharField(max_length=100, null=True, blank=True)

@receiver(post_save, sender=User)
def my_handler(sender, **kwargs):
    """
    Quando Criar um usuário no Django, vai rodar essa função
    para criar uma instancia nesse modelo MyProfile no campo "user".
    """
    if kwargs.get('created', False):
        MyProfile.objects.create(user=kwargs['instance'])

class Cliente(models.Model):
    cpf = models.CharField(max_length=11, unique=True, null=True)
    nome_completo = models.CharField(max_length=255, null=True)
    data_nascimento = models.DateField(null=True)
    email = models.EmailField(null=True)
    telefone = models.CharField(max_length=15, null=True)
    documento_oficial = models.ImageField(upload_to='documentos_oficiais/', null=True, blank=True)
    comprovante_residencia = models.ImageField(upload_to='comprovantes_residencia/', null=True, blank=True)

    def __str__(self):
        return self.nome_completo

class Equipamento(models.Model):
    nome = models.CharField(max_length=100, null=True)
    fotos = models.ImageField(upload_to='equipamentos/', null=True)
    descricao = models.TextField(null=True)
    preco_diaria = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)  # Adicionando categoria
    

    def __str__(self):
        return self.nome

class Disponibilidade(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, null=True)
    data = models.DateField(null=True)
    disponivel = models.BooleanField(default=True)
    horario_final_locacao = models.TimeField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.equipamento.nome} - {self.data} - {'Disponível' if self.disponivel else 'Indisponível'}"

class Agendamento(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, null=True)
    frete_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    frete_entrega = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    frete_coleta = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    data_inicio = models.DateField(null=True)
    data_fim = models.DateField(null=True)
    hora_inicio = models.TimeField(null=True)
    hora_fim = models.TimeField(null=True)
    opcao_frete = models.CharField(max_length=50, null=True)
    logradouro = models.CharField(max_length=255, null=True)
    numero = models.CharField(max_length=10, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    def __str__(self):
        return f"Agendamento de {self.equipamento.nome} para {self.cliente.nome_completo}"
    
class FAQ(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()

    def __str__(self):
        return self.titulo
