# Generated by Django 3.2 on 2023-05-09 07:25

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
                ('product_name', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
    ]