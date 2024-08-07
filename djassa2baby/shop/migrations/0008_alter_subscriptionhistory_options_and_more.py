# Generated by Django 5.0.3 on 2024-05-28 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_shop_options_category_slug_product_shop_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptionhistory',
            options={},
        ),
        migrations.AddField(
            model_name='productreview',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shopreview',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
