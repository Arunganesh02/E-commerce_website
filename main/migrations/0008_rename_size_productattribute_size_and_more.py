# Generated by Django 4.1.5 on 2023-02-06 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_banner_rename_size_productattribute_size_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productattribute',
            old_name='Size',
            new_name='size',
        ),
        migrations.AlterField(
            model_name='details',
            name='image',
            field=models.ImageField(upload_to='details_imgs/'),
        ),
    ]
