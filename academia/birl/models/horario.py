
from django.db import models

class Horario(models.Model):
    descricao = models.CharField(max_length=255)
    inicio = models.TimeField()
    fim = models.TimeField()

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Horário"
        verbose_name_plural = "Horários"
