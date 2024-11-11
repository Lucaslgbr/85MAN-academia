# Generated by Django 3.2.13 on 2024-06-27 18:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContaBancaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agencia', models.CharField(max_length=255)),
                ('conta', models.CharField(max_length=255)),
                ('nome', models.CharField(max_length=255)),
                ('saldo', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'verbose_name': 'Conta Bancária',
                'verbose_name_plural': 'Contas Bancárias',
            },
        ),
        migrations.CreateModel(
            name='EntradaFinanceira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('descricao', models.CharField(max_length=255)),
                ('conta_bancaria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='birl.contabancaria')),
            ],
            options={
                'verbose_name': 'Entrada financeira',
                'verbose_name_plural': 'Entradas financeiras',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255, verbose_name='Descrição')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Mensalidade',
                'verbose_name_plural': 'Mensalidades',
            },
        ),
        migrations.CreateModel(
            name='SaidaFinanceira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('descricao', models.CharField(max_length=255)),
                ('conta_bancaria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='birl.contabancaria')),
            ],
            options={
                'verbose_name': 'Saída financeira',
                'verbose_name_plural': 'Saídas financeiras',
            },
        ),
        migrations.DeleteModel(
            name='FluxoCaixa',
        ),
        migrations.AlterField(
            model_name='venda',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='birl.produto'),
        ),
    ]
