# Generated by Django 3.1.2 on 2021-11-05 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lot_user', '0002_lot_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]