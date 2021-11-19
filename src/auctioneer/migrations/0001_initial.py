# Generated by Django 3.1.2 on 2021-11-19 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction_id', models.IntegerField()),
                ('auction_start', models.DateTimeField()),
                ('auction_end', models.DateTimeField()),
                ('auctioneer', models.CharField(max_length=50)),
                ('auction_status', models.CharField(max_length=50)),
                ('auction_published', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot_name', models.CharField(max_length=200)),
                ('reserve_price', models.IntegerField()),
                ('sequential_uuid', models.IntegerField()),
                ('minimal_bid', models.IntegerField()),
                ('seller_contact', models.IntegerField()),
                ('lot_description', models.CharField(max_length=200)),
                ('minimum_bid_increment', models.IntegerField()),
                ('comissions', models.IntegerField()),
                ('taxes', models.IntegerField()),
                ('number_of_bids_made', models.IntegerField()),
                ('current_winner_buyer', models.CharField(max_length=200)),
                ('highest_value_bid', models.IntegerField()),
                ('auction_ref_id', models.IntegerField()),
                ('auction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctioneer.auction')),
            ],
        ),
    ]
