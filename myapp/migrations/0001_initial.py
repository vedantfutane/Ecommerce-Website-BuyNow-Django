# Generated by Django 4.2.1 on 2023-07-19 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('discounted_price', models.FloatField()),
                ('description', models.TextField()),
                ('composition', models.TextField(default='')),
                ('prodapp', models.TextField(default='')),
                ('category', models.CharField(choices=[('PR1', 'prod1'), ('PR2', 'prod2'), ('PR3', 'prod3'), ('PR4', 'prod4'), ('PR5', 'prod5'), ('PR6', 'prod6'), ('PR7', 'prod7'), ('PR8', 'prod8')], max_length=3)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
    ]
