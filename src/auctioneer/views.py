from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from .models import Auction
from lot_user.views import LotForm
from lot_user.models import Lot

from apps.decorators import *

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('auction_id', 'auction_start', 'auction_end', 'auctioneer', 'auction_winner', 'auction_published')

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_list(request, template_name='auctioneer/auction_list.html'):
    auction = Auction.objects.all()
    data = {}
    data['object_list'] = auction

    lot = Lot.objects.all()
    data['lot_list'] = lot
    return render(request, template_name, data)

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_create(request, template_name='auctioneer/auction_form.html'):
    form = AuctionForm(request.POST or None)
    if form.is_valid():
        auction = form.save(commit=False)
        auction.user = request.user
        auction.save()
        return redirect('auctioneer:auction_list')
    return render(request, template_name, {'form':form})

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_list_lot(request, template_name='auctioneer/lot_list.html'):
    lot = Lot.objects.all()
    data = {}
    data['object_list'] = lot
    return render(request, template_name, data)

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_add_lot(request, id, pk, template_name='auctioneer/lot_list.html'):
    lot= get_object_or_404(Lot, pk=id)
    
    lot.auction_ref_id = pk
    lot.save()

    print(pk)
    return redirect('auctioneer:auction_list')

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_publish(request, pk, template_name='auctioneer/auction_list.html'):
    auction= get_object_or_404(Auction, pk=pk)
    auction.auction_published = "published"
    auction.save()
    return redirect('auctioneer:auction_list')

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_update(request, pk, template_name='auctioneer/auction_form.html'):
    if request.user.is_superuser:
        auction= get_object_or_404(Auction, pk=pk)
    else:
        auction= get_object_or_404(Auction, pk=pk, user=request.user)
    form = AuctionForm(request.POST or None, instance=auction)
    if form.is_valid():
        form.save()
        return redirect('auctioneer:auction_list')
    return render(request, template_name, {'form':form})

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_delete(request, pk, template_name='auctioneer/auction_confirm_delete.html'):
    if request.user.is_superuser:
        auction= get_object_or_404(Auction, pk=pk)
    else:
        auction= get_object_or_404(Auction, pk=pk, user=request.user)   
    if request.method=='POST':
        auction.delete()
        return redirect('auctioneer:auction_list')
    return render(request, template_name, {'object':auction})
