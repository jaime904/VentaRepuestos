# Generated by Django 5.0.4 on 2024-06-10 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0006_cliente_boleta_cliente_despacho'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='descripcion',
            field=models.CharField(default='N/A', max_length=50),
            preserve_default=False,
        ),
    ]
