# Generated by Django 4.2.5 on 2023-11-21 01:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clasesYa', '0005_alter_user_tipousuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('hora', models.TimeField(auto_now_add=True)),
                ('idAlumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alumno', to=settings.AUTH_USER_MODEL)),
                ('idProfesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profesor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
