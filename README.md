# Ação do FGTS

Cálculo automático do valor da causa do FGTS conforme ADI 5090

## Contexto
A forma como é feito um cálculo jurídico hoje em dia é predominantemente manual. Advogados e contadores muitas vezes utilizam planilhas de excel ou mesmo terceirizam o trabalho operacional. 

## Objetivo

O objetivo do projeto é automatizar o cálculo do valor de causa do FGTS conforme a ADI 5090. O usuário envia o extrato do FGTS em PDF (gerado pela Caixa Econômica) e o programa realiza a extração dos dados, tratamento e cálculo retroativo baseado nos índices de correção monetária dos últimos 20 anos. O programa retorna para o usuário o valor de causa e a memória de cálculo completa em PDF para anexar à ação judicial.

O cálculo jurídico é realizado conforme instruções disponiblizadas pela [Justiça Federal do Rio Grande do Sul](https://www2.jfrs.jus.br/fgts-net-2/).

## Deploy com Heroku

https://acao-fgts.herokuapp.com

O carregamento inicial é lento devido ao app estar inativo no Heroku.

## Liguagem e dependências utilizadas
- [Python](https://www.python.org/)

Framework para desenvolvimento web
- [Django](https://www.djangoproject.com/)

Extrair dados de arquivos PDF
- [Tabula-py](https://pypi.org/project/tabula-py/)

Tratamento dos dados e cálculo do valor de causa
- [Pandas](https://pandas.pydata.org/)

Gerar relatório em PDF
- [XHTML2PDF](https://github.com/xhtml2pdf/xhtml2pdf)

## Como rodar localmente

Siga esse passo-a-passo para rodar a aplicação localmente:

1. Clone ou baixe esse repositório
2. Crie um ambiente virtual e o ative
3. Instale as dependências necessárias utilizando 'pip install -r requirements.txt'
4. Inicie a aplicação com 'python manage.py runserver'
5. Acesse a aplicação através do 'localhost:8080' no seu browser

Necessário Java 8+ instalado para rodar o Tabula-py

## Tarefas em aberto
- [ ] Emails transacionais
- [ ] Upload de múltiplos extratos em PDF
- [ ] Compra de relatórios
- [ ] Melhorar layout da memória de cálculo
