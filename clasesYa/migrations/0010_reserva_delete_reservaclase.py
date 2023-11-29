# Generated by Django 4.2.5 on 2023-11-29 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clasesYa', '0009_clase_reservaclase'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHora', models.DateTimeField(auto_now_add=True)),
                ('idAlumno', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='alumno', to=settings.AUTH_USER_MODEL)),
                ('idProfesor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profesor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='ReservaClase',
        ),
    ]
