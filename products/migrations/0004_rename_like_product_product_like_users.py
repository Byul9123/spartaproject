# Generated by Django 4.2 on 2024-04-17 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_like_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='like_product',
            new_name='like_users',
        ),
    ]
