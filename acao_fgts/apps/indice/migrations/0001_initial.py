# Generated by Django 4.0.4 on 2022-05-19 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IndicePeriodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('periodo_ano', models.IntegerField(choices=[(1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022)], default=2022, verbose_name='Ano do Período')),
                ('periodo_mes', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], default=5, verbose_name='Mês do Período')),
                ('periodo', models.DateField(editable=False, unique=True, verbose_name='Período')),
                ('indice_jam_3', models.FloatField(verbose_name='Índice Jam 3%')),
                ('indice_jam_6', models.FloatField(verbose_name='Índice Jam 6%')),
                ('variacao_inpc', models.FloatField(verbose_name='Variação do INPC')),
            ],
        ),
    ]
