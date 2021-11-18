from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib import messages

from buyer.views import BuyerForm
from auctioneer.models import Auction
from lot_user.models import Lot

from apps.decorators import *

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('auction_id', 'auction_start', 'auction_end', 'auctioneer', 'auction_winner', 'auction_status')

def auction_list(request, template_name='auction/auction_list.html'):
    auction = Auction.objects.all()
    data = {}
    data['object_list'] = auction

    lot = Lot.objects.all()
    data['lot_list'] = lot
    return render(request, template_name, data)

def update_valid_bid(request, lot, bid):
    lot.number_of_bids_made += 1
    lot.current_winner_buyer = str(request.user)
    lot.highest_value_bid = bid.bid_value
    lot.save()

@login_required
@allowed_users(allowed_roles=['buyer'])
def make_bid(request, id, pk, template_name='auction/auction_bid.html'):
    lot = get_object_or_404(Lot, pk=pk)
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


####### as funcoes abaixo nao estao sendo utilizadas

def auction_create(request, template_name='auction/auction_form.html'):
    form = AuctionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('auction:auction_list')
    return render(request, template_name, {'form':form})

def auction_update(request, pk, template_name='auction/auction_form.html'):
    auction= get_object_or_404(Auction, pk=pk)
    form = AuctionForm(request.POST or None, instance=auction)
    if form.is_valid():
        form.save()
        return redirect('auction:auction_list')
    return render(request, template_name, {'form':form})

def auction_delete(request, pk, template_name='auction/auction_confirm_delete.html'):
    auction= get_object_or_404(Auction, pk=pk)    
    if request.method=='POST':
        auction.delete()
        return redirect('auction:auction_list')
    return render(request, template_name, {'object':auction})