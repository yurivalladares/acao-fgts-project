from django.db import models
from acao_fgts.apps.common.models import BaseModel
from django.contrib.auth.models import User

class CalculoFgts(BaseModel):
    juros_anual_3= 3
    juros_anual_6 = 6

    JUROS_ANUAL = [
        (juros_anual_3, '3%'),
        (juros_anual_6, '6%'),
    ]

    nome_completo = models.CharField(max_length=50, blank=True)
    arquivo_extrato = models.FileField(upload_to='extrato_pdf/%Y/%m/%d/')
    empregador = models.CharField(max_length=50, blank=True)
    juros_anual = models.IntegerField(choices=JUROS_ANUAL, default=juros_anual_3, blank=True)
    valor_causa = models.FloatField(editable=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    inicio_periodo = models.DateField(editable=False, blank=True)
    termino_periodo = models.DateField(editable=False, blank=True)
    hide = models.BooleanField(default=False)
    pago = models.BooleanField(default=True)
    df_json = models.JSONField(blank=True)

    @property
    def intervalo_periodo_str(self):
        intervalo_periodo = self.inicio_periodo.strftime('%B/%Y') + "até" + self.termino_periodo.strftime('%B/%Y')
        return intervalo_periodo

    @property
    def username(self):
        return self.user.username

