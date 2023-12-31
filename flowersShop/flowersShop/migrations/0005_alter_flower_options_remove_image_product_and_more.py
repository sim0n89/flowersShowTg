# Generated by Django 4.2.4 on 2023-08-16 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowersShop', '0004_remove_product_compound_product_compound'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flower',
            options={'verbose_name': 'Цветок', 'verbose_name_plural': 'Цветы'},
        ),
        migrations.RemoveField(
            model_name='image',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(to='flowersShop.image', verbose_name='Картинки'),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=50, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='client',
            name='tlg_id',
            field=models.CharField(max_length=50, verbose_name='ID телеграмм'),
        ),
        migrations.AlterField(
            model_name='product',
            name='compound',
            field=models.ManyToManyField(to='flowersShop.flower', verbose_name='Состав'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_to_category',
            field=models.ManyToManyField(to='flowersShop.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
    ]
