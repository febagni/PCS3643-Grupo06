from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib import messages
from django.utils import timezone

from datetime import date, datetime, time, timedelta
from dateutil.tz import tzoffset
from pytz import timezone

from buyer.views import BuyerForm
from auctioneer.models import Auction
from lot_user.models import Lot


from apps.decorators import *

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('auction_id', 'auction_start', 'auction_end', 'auctioneer', 'auction_status', 'auction_published')

def auction_list(request, template_name='auction/auction_list.html'):
    auction = Auction.objects.all()
    data = {}
    data['object_list'] = auction
    
    lot = Lot.objects.all()
    data['lot_list'] = lot

    current_date = datetime.today()
    data['today'] = current_date

    for i in range(len(auction)):
        end_date = Auction.objects.values_list('auction_end')[i][0].replace(tzinfo=None)
        start_date = Auction.objects.values_list('auction_start')[i][0].replace(tzinfo=None)
        iterable_pk = Auction.objects.values_list('id')[i][0]
        if current_date < end_date:
            if current_date >= start_date:
                Auction.objects.filter(pk=iterable_pk).update(auction_status="ON GOING")
            else:
                Auction.objects.filter(pk=iterable_pk).update(auction_status="TO BE STARTED")
        else:
            Auction.objects.filter(pk=iterable_pk).update(auction_status="FINISHED")

    return render(request, template_name, data)

def update_valid_bid(request, lot, bid):
    lot.number_of_bids_made += 1
    lot.current_winner_buyer = str(request.user)
    lot.highest_value_bid = bid.bid_value
    if lot.reserve_price <= lot.highest_value_bid: 
        lot.is_higher_than_reserve = "TRUE"
    print(lot.is_higher_than_reserve)
    lot.save()
    pass

@login_required
@allowed_users(allowed_roles=['buyer'])
def make_bid(request, id, pk, template_name='auction/auction_bid.html'):
    lot = get_object_or_404(Lot, pk=pk)
    #LotList.addBidToLotList(lot)
    data = {}
    data['lot'] = lot

    form = BuyerForm(request.POST or None)
    form.fields['auction_id'].initial = id
    form.fields['lot_id'].initial = pk
    
    if form.is_valid():
        bid = form.save(commit=False)
        bid.user = request.user
        bid.save()
        if lot.number_of_bids_made == 0:
            if bid.bid_value >= lot.minimal_bid:
                update_valid_bid(request, lot, bid)
                return HttpResponseRedirect('/auction/')
            else:
                messages.info(request, 'Invalid bid. Please enter a valid value.')
                return HttpResponseRedirect('/auction/bid/' + str(id) + '/' + str(pk) + '/')
        else:
            if bid.bid_value >= (lot.highest_value_bid + lot.minimum_bid_increment):
                update_valid_bid(request, lot, bid)
                return HttpResponseRedirect('/auction/')
            else:
                messages.info(request, 'Invalid bid. Please enter a valid value.')
                return HttpResponseRedirect('/auction/bid/' + str(id) + '/' + str(pk) + '/')
   
    data['bid_form'] = form

    return render(request, template_name, data)

def get_today():
    return datetime.now()

def get_time():
    return datetime.now().time()
