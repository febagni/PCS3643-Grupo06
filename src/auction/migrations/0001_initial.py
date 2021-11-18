# Generated by Django 3.1.2 on 2021-11-17 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction_id', models.IntegerField()),
                ('auction_start', models.IntegerField()),
                ('auction_end', models.IntegerField()),
                ('auctioneer', models.CharField(max_length=50)),
                ('auction_winner', models.CharField(max_length=50)),
                ('auction_status', models.CharField(max_length=50)),
            ],
        ),
    ]
