# Generated by Django 5.0 on 2023-12-11 12:28

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_number',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]