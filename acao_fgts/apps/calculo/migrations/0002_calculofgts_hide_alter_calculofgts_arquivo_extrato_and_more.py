# Generated by Django 4.0.4 on 2022-05-20 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calculo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculofgts',
            name='hide',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='calculofgts',
            name='arquivo_extrato',
            field=models.FileField(upload_to='extrato_pdf/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='calculofgts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
