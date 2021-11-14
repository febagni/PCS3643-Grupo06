from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from .models import Lot
from apps.decorators import *

import uuid

class LotForm(ModelForm):
    class Meta:
        model = Lot
        fields = [ 
            #seller
            'lot_name',
            'seller_contact',
            'lot_description',
            'reserve_price',
            #auctioneer
            'minimal_bid',
            'minimum_bid_increment', 
            'comissions',
            'taxes',
            #algorithm
            'sequential_uuid',
            'number_of_bids_made',
            'current_winner_buyer',
            'highest_value_bid' 
        ]

my_uuid = uuid.uuid4()

@login_required
@allowed_users(allowed_roles=['auctioneer', 'seller'])
def lot_list(request, template_name='lot_user/lot_list.html'):
    lot = Lot.objects.all()
    data = {}
    data['object_list'] = lot
    return render(request, template_name, data)

@login_required
@allowed_users(allowed_roles=['auctioneer', 'seller'])
def lot_detail(request, pk, template_name='lot_user/lot_detail.html'):
    lot = Lot.objects.filter(pk=pk)
    data = {}
    data['object_list'] = lot
    return render(request, template_name, data)

@login_required
@allowed_users(allowed_roles=['seller'])
def lot_create(request, template_name='lot_user/lot_form.html'):
    form = LotForm(request.POST, initial={'minimal_bid': 0})
    if form.is_valid():
        lot = form.save(commit=False)
        lot.user = request.user
        lot.save()
        return redirect('lot_user:lot_list')
    return render(request, template_name, {'form':form})

@login_required
@allowed_users(allowed_roles=['auctioneer', 'seller'])
def lot_update(request, pk, template_name='lot_user/lot_form.html'):
    if request.user.groups.all()[0].name == 'auctioneer':
        lot= get_object_or_404(Lot, pk=pk)
    else:
        lot= get_object_or_404(Lot, pk=pk, user=request.user)
    form = LotForm(request.POST or None, instance=lot)
    if form.is_valid():
        form.save()
        return redirect('lot_user:lot_list')
    return render(request, template_name, {'form':form})

@login_required
@allowed_users(allowed_roles=['auctioneer', 'seller'])
def lot_delete(request, pk, template_name='lot_user/lot_confirm_delete.html'):
    if request.user.groups.all()[0].name == 'auctioneer':
        lot= get_object_or_404(Lot, pk=pk)
    else:
        lot= get_object_or_404(Lot, pk=pk, user=request.user)   
    if request.method=='POST':
        lot.delete()
        return redirect('lot_user:lot_list')
    return render(request, template_name, {'object':lot})
