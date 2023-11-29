# Generated by Django 4.2.5 on 2023-11-27 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clasesYa', '0008_delete_clase'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, default='', max_length=255)),
                ('descripcion', models.CharField(blank=True, default='', max_length=255)),
                ('precio', models.IntegerField(blank=True, default=0)),
                ('rating', models.IntegerField(blank=True, default=0)),
                ('campo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='clasesYa.campo')),
                ('profesor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sesion', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='clasesYa.sesion')),
            ],
        ),
        migrations.CreateModel(
            name='ReservaClase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_reserva', models.DateTimeField(auto_now_add=True)),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clasesYa.clase')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
