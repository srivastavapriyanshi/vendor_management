# Generated by Django 5.0 on 2023-12-14 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_purchaseorder_po_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='items',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
