# Generated by Django 5.2.3 on 2025-07-02 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='operation',
            field=models.CharField(choices=[('sale', 'Vente'), ('exchange', 'Échange'), ('both', 'Vente ou échange')], default='sale', max_length=10, verbose_name="Type d'opération"),
        ),
    ]
