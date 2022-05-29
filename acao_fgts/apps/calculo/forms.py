from django import forms
from acao_fgts.apps.calculo.models import CalculoFgts

class CalculoFgtsForms(forms.ModelForm):
    nome_completo = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nome Completo'}))
    empregador = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Empregador'}))

    class Meta:
        model = CalculoFgts
        fields = ['nome_completo', 'empregador', 'arquivo_extrato']
