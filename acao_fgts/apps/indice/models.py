from django.db import models
from datetime import datetime


class IndicePeriodo(models.Model):
    YEAR_CHOICES = [(y, y) for y in range(1999, datetime.today().year + 1)]
    MONTH_CHOICE = [(m, m) for m in range(1, 13)]

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    periodo_ano = models.IntegerField(verbose_name='Ano do Período', choices=YEAR_CHOICES,
                                        default=datetime.today().year, )
    periodo_mes = models.IntegerField(verbose_name='Mês do Período', choices=MONTH_CHOICE,
                                        default=datetime.today().month, )
    periodo = models.DateField(verbose_name='Período', unique=True, editable=False)
    indice_jam_3 = models.FloatField(verbose_name='Índice Jam 3%')
    indice_jam_6 = models.FloatField(verbose_name='Índice Jam 6%')
    variacao_inpc = models.FloatField(verbose_name='Variação do INPC')

    @property
    def get_periodo(self):
        if self.periodo_ano and self.periodo_mes:
            return datetime(year=self.periodo_ano, month=self.periodo_mes, day=1)
        else:
            return None

    def __str__(self):
        return str(self.periodo.strftime('%Y-%m'))

    def save(self, *args, **kwargs):
        self.periodo = self.get_periodo
        super(IndicePeriodo, self).save(*args, **kwargs)