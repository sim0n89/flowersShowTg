# Generated by Django 4.2.4 on 2023-08-16 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowersShop', '0003_alter_category_options_alter_client_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='compound',
        ),
        migrations.AddField(
            model_name='product',
            name='compound',
            field=models.ManyToManyField(to='flowersShop.flower'),
        ),
    ]
