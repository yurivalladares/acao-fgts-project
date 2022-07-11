import tabula
import pandas as pd
import numpy as np
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from acao_fgts.apps.calculo.models import CalculoFgts
from acao_fgts.apps.indice.models import IndicePeriodo
from acao_fgts.apps.common.services import search_dataframe, to_datetime_replacer


class CalularAcaoFgts:

    def __init__(self, nome_completo, empregador, arquivo_extrato, user: User):
        self.nome_completo = nome_completo
        self.arquivo_extrato = arquivo_extrato
        self.empregador = empregador
        self.user = user
        self.df = tabula.read_pdf(arquivo_extrato, pages='all', stream=True, pandas_options={'header': 0})

    def extrair_juros_anual(self):
        if not search_dataframe('3 %', self.df[0]).empty:
            return 3
        else:
            return 6

    def tratar_extrato(self):
        df = pd.concat(self.df[1:], ignore_index=True)
        df.drop(index=0, inplace=True)
        filtro = df['LANÇAMENTO'].str.contains(pat='CREDITO DE JAM')
        df_filtrado = df[filtro]
        df_filtrado.index = range(df_filtrado.shape[0])
        df_extrato = df_filtrado.copy()
        df_extrato.drop(axis=1, columns=['TOTAL', 'LANÇAMENTO'], inplace=True)
        df_extrato['VALOR'] = df_extrato['VALOR'].str.replace('R$', '', regex=False)
        df_extrato['VALOR'] = df_extrato['VALOR'].str.replace('.', '', regex=False)
        df_extrato['VALOR'] = df_extrato['VALOR'].str.replace(',', '.', regex=False)
        df_extrato['VALOR'] = df_extrato['VALOR'].astype('float64')
        df_extrato['DATA'] = pd.to_datetime(df_extrato['DATA'], dayfirst=True)
        df_extrato.rename(columns={'DATA': 'periodo', 'VALOR': 'credito_jam'}, inplace=True)
        df_extrato['periodo'] = to_datetime_replacer(df_extrato['periodo'], day=1)
        df_extrato.set_index('periodo', inplace=True)
        return df_extrato

    def extrair_inicio_periodo(self):
        return self.tratar_extrato().index[0]

    def extrair_termino_periodo(self):
        return self.tratar_extrato().index[-1]

    def calcular_saldo_acumulado(self, a, b):
        res = [0] * len(a)
        res[0] = a[0]
        for i in range(1, len(a)):
            res[i] = res[i - 1] * (b[i] + 1) + a[i]
        return res

    def ler_indice(self):
        df_indice = pd.DataFrame(data=IndicePeriodo.objects.all().values(),
                                 columns=['periodo', 'indice_jam_3', 'indice_jam_6', 'variacao_inpc'])
        df_indice['periodo'] = pd.to_datetime(df_indice['periodo'], dayfirst=True)
        df_indice.set_index('periodo', inplace=True)
        return df_indice

    def gerar_memoria_calculo(self):
        JUROS_MENSAL_3_AA = 0.00246627
        JUROS_MENSAL_6_AA = 0.00486755

        df_causa = pd.concat([self.ler_indice(), self.tratar_extrato()], join='outer', axis=1)
        df_causa.fillna(0, inplace=True)
        df_causa = df_causa.loc[self.extrair_inicio_periodo():]
        df_causa.reset_index(inplace=True)
        if self.extrair_juros_anual() == 3:
            df_causa.rename(inplace=True, columns={'indice_jam_3': 'indice_jam'})
            df_causa['base_calculo_jam_creditado'] = df_causa['credito_jam'] / df_causa['indice_jam']
            df_causa['novo_indice_jam'] = ((1 + df_causa['variacao_inpc']) * (1 + JUROS_MENSAL_3_AA)) - 1
        else:
            df_causa.rename(inplace=True, columns={'indice_jam_6': 'indice_jam'})
            df_causa['base_calculo_jam_creditado'] = df_causa['credito_jam'] / df_causa['indice_jam']
            df_causa['novo_indice_jam'] = ((1 + df_causa['variacao_inpc']) * (1 + JUROS_MENSAL_6_AA)) - 1

        df_causa['novo_credito_jam'] = df_causa['base_calculo_jam_creditado'] * df_causa['novo_indice_jam']
        df_causa['diferenca_jam_devida'] = df_causa['novo_credito_jam'] - df_causa['credito_jam']
        df_causa.sort_index(axis=1, inplace=True)
        df_causa['saldo_acumulado'] = self.calcular_saldo_acumulado(df_causa['diferenca_jam_devida'],
                                                                    df_causa['novo_indice_jam'])
        df_causa.replace([np.inf, -np.inf], 0, inplace=True)
        df_causa = df_causa[['periodo',
                             'credito_jam',
                             'indice_jam',
                             'base_calculo_jam_creditado',
                             'variacao_inpc',
                             'novo_indice_jam',
                             'novo_credito_jam',
                             'diferenca_jam_devida',
                             'saldo_acumulado'
                             ]]
        return df_causa

    def get_memoria_calculo(self):
        return self.gerar_memoria_calculo()

    def gerar_memoria_json(self):
        df = self.get_memoria_calculo()
        df1 = df.copy()
        df1['periodo'] = df1['periodo'].dt.strftime('%Y-%m')
        df1 = df1.round({'credito_jam': 2,
                         'base_calculo_jam_creditado': 2,
                         'novo_indice_jam': 6,
                         'novo_credito_jam': 2,
                         'diferenca_jam_devida': 2,
                         'saldo_acumulado': 2
                         })
        df1 = df1.astype({'credito_jam': 'str',
                          'indice_jam': 'str',
                          'base_calculo_jam_creditado': 'str',
                          'variacao_inpc': 'str',
                          'novo_indice_jam': 'str',
                          'novo_credito_jam': 'str',
                          'diferenca_jam_devida': 'str',
                          'saldo_acumulado': 'str'
                          })
        df1.replace('\\.', ',', regex=True, inplace=True)
        df1.rename(inplace=True,
                   columns={'periodo': 'Período',
                            'credito_jam': 'Valor do crédito JAM',
                            'indice_jam': 'Índice JAM',
                            'base_calculo_jam_creditado': 'Base cálculo do JAM creditado',
                            'variacao_inpc': 'Variação INPC',
                            'novo_indice_jam': 'Novo índice JAM',
                            'novo_credito_jam': 'Novo valor do crédito JAM',
                            'diferenca_jam_devida': 'Diferença de JAM devida',
                            'saldo_acumulado': 'Total Corrigido Acumulado'
                            })
        df_json = df1.to_json(orient='records')
        return df_json

    def extrair_valor_causa(self):
        # return self.get_memoria_calculo().iloc[-1, -1].round(2)
        for i in reversed(range(-200, 0)):
            if self.get_memoria_calculo().iloc[i, -1].round(2) > 0:
                return self.get_memoria_calculo().iloc[i, -1].round(2)
        return 0

    def criar_calculo_fgts(self):

        obj = CalculoFgts(
            nome_completo=self.nome_completo,
            arquivo_extrato=self.arquivo_extrato,
            empregador=self.empregador,
            valor_causa=self.extrair_valor_causa(),
            juros_anual=self.extrair_juros_anual(),
            user=self.user,
            inicio_periodo=self.extrair_inicio_periodo(),
            termino_periodo=self.extrair_termino_periodo(),
            df_json=self.gerar_memoria_json(),
        )

        obj.save()

        return obj
