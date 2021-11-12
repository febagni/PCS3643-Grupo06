from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from .models import Lot
from apps.decorators import *

class LotForm(ModelForm):
    class Meta:
        model = Lot
        fields = [ 
            'lot_name',
            'reserve_price',
            'sequential_uuid',
            'minimal_bid',
            'lot_photo',
            'seller_contact',
            'lot_description',
            'minimum_bid_increment', 
            'comissions',
            'taxes',
            'number_of_bids_made',
            'current_winner_buyer',
            'highest_value_bid' 
        ]

@login_required
@allowed_users(allowed_roles=['seller'])
def lot_list(request, template_name='lot_user/lot_list.html'):
    if request.user.is_superuser:
        lot = Lot.objects.all()
    else:
        lot = Lot.objects.filter(user=request.user)
    data = {}
    data['object_list'] = lot
    return render(request, template_name, data)

@login_required
@allowed_users(allowed_roles=['seller'])
def lot_create(request, template_name='lot_user/lot_form.html'):
    form = LotForm(request.POST or None)
    if form.is_valid():
        lot = form.save(commit=False)
        lot.user = request.user
        lot.save()
        return redirect('lot_user:lot_list')
    return render(request, template_name, {'form':form})

@login_required
@allowed_users(allowed_roles=['seller'])
def lot_update(request, pk, template_name='lot_user/lot_form.html'):
    if request.user.is_superuser:
        lot= get_object_or_404(Lot, pk=pk)
    else:
        lot= get_object_or_404(Lot, pk=pk, user=request.user)
    form = LotForm(request.POST or None, instance=lot)
    if form.is_valid():
        form.save()
        return redirect('lot_user:lot_list')
    return render(request, template_name, {'form':form})

@login_required
@allowed_users(allowed_roles=['seller'])
def lot_delete(request, pk, template_name='lot_user/lot_confirm_delete.html'):
    if request.user.is_superuser:
        lot= get_object_or_404(Lot, pk=pk)
    else:
        lot= get_object_or_404(Lot, pk=pk, user=request.user)   
    if request.method=='POST':
        lot.delete()
        return redirect('lot_user:lot_list')
    return render(request, template_name, {'object':lot})
