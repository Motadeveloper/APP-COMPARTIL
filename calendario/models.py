from django.db import models

class Reserva(models.Model):
    data = models.DateField(unique=True)
    reservado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.data} - {'Reservado' if self.reservado else 'Disponível'}"
