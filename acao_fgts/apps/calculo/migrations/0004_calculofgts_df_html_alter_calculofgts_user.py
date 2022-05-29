# Generated by Django 4.0.4 on 2022-05-24 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calculo', '0003_calculofgts_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculofgts',
            name='df_html',
            field=models.TextField(blank=True, default='', max_length=200000),
        ),
        migrations.AlterField(
            model_name='calculofgts',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
