# Generated by Django 5.0.3 on 2024-07-15 21:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_alter_product_quantity_in_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shop',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='shop.shop'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
