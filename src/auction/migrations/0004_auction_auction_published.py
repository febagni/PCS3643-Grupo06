# Generated by Django 3.1.2 on 2021-11-15 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auto_20211105_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='auction_published',
            field=models.CharField(default='a', max_length=50),
            preserve_default=False,
        ),
    ]