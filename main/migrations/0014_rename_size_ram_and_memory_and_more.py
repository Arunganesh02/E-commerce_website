# Generated by Django 4.1.6 on 2023-02-25 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_price_range_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='size',
            new_name='Ram_and_memory',
        ),
        migrations.AlterModelOptions(
            name='ram_and_memory',
            options={'verbose_name_plural': '5.Ram_and_memorys'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='size',
            new_name='Ram_and_memory',
        ),
        migrations.RenameField(
            model_name='productattribute',
            old_name='size',
            new_name='Ram_and_memory',
        ),
    ]
