# Generated by Django 3.1.2 on 2021-11-11 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctioneer', '0005_lot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='auction_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='auction',
            name='auction_start',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='lot',
            name='auction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctioneer.auction'),
        ),
    ]
