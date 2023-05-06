# Generated by Django 4.1.5 on 2023-01-29 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('alt_text', models.CharField(max_length=300)),
            ],
        ),
        migrations.RenameField(
            model_name='productattribute',
            old_name='size',
            new_name='Size',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
    ]
