# Generated by Django 3.2.13 on 2024-06-27 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birl', '0002_auto_20240627_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='frequencia',
        ),
        migrations.CreateModel(
            name='Frequencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('presente', models.BooleanField()),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='birl.aluno')),
            ],
            options={
                'verbose_name': 'Frequência',
                'verbose_name_plural': 'Frequências',
            },
        ),
    ]