from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib import messages

from .models import Lot
from apps.decorators import *

import uuid

class LotForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lot_name'].required = False
        self.fields['seller_contact'].required = False
        self.fields['lot_description'].required = False
        self.fields['reserve_price'].required = False

        self.fields['minimal_bid'].required = False
        self.fields['minimal_bid'].disabled = True
        self.fields['minimal_bid'].initial = 0

        self.fields['minimum_bid_increment'].required = False
        self.fields['minimum_bid_increment'].disabled = True
        self.fields['minimum_bid_increment'].initial = 0

        self.fields['comissions'].required = False
        self.fields['comissions'].disabled = True
        self.fields['comissions'].initial = 0

        self.fields['taxes'].required = False
        self.fields['taxes'].disabled = True
        self.fields['taxes'].initial = 0

        self.fields['sequential_uuid'].required = False
        self.fields['sequential_uuid'].disabled = True
        self.fields['sequential_uuid'].initial = uuid.uuid4()

        self.fields['number_of_bids_made'].required = False
        self.fields['number_of_bids_made'].disabled = True
        self.fields['number_of_bids_made'].initial = 0

        self.fields['current_winner_buyer'].required = False
        self.fields['current_winner_buyer'].disabled = True
        self.fields['current_winner_buyer'].initial = "No one"

        self.fields['highest_value_bid'].required = False
        self.fields['highest_value_bid'].disabled = True
        self.fields['highest_value_bid'].initial = 0

        self.fields['auction_ref_id'].required = False
        self.fields['auction_ref_id'].disabled = True
        self.fields['auction_ref_id'].initial = -999

        self.fields['is_higher_than_reserve'].required = False
        self.fields['is_higher_than_reserve'].disabled = True
        self.fields['is_higher_than_reserve'].initial = "FALSE"

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
            'highest_value_bid',
            #auction
            'auction_ref_id',
            'is_higher_than_reserve'
        ]

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
    form = LotForm(request.POST or None)
    if form.is_valid():
        lot = form.save(commit=False)
        lot.user = request.user
        if lot.lot_name != "" and lot.lot_description != "" and lot.reserve_price != "" and lot.seller_contact != "":
            messages.info(request, 'Successful lot submission!')
            lot.save()
            return HttpResponseRedirect('/lot_user/new/')
        else:
            messages.info(request, 'Incomplete form! Please, fill all the required information before submission.')
            return HttpResponseRedirect('/lot_user/new/')
    return render(request, template_name, {'form':form})

@login_required
@allowed_users(allowed_roles=['auctioneer', 'seller'])
def lot_update(request, pk, template_name='lot_user/lot_form_edit.html'):
    if request.user.groups.all()[0].name == 'auctioneer':
        lot= get_object_or_404(Lot, pk=pk)
    else:
        lot= get_object_or_404(Lot, pk=pk, user=request.user)
    form = LotForm(request.POST or None, instance=lot)
    if request.user.groups.all()[0].name == 'auctioneer':
        form.fields['lot_name'].disabled = True
        form.fields['seller_contact'].disabled = True
        form.fields['lot_description'].disabled = True
        form.fields['reserve_price'].disabled = True
        form.fields['minimal_bid'].disabled = False
        form.fields['minimum_bid_increment'].disabled = False

    elif request.user.groups.all()[0].name == 'seller':
        template_name = 'lot_user/lot_form_edit_seller.html'
        form.fields['lot_name'].disabled = False
        form.fields['seller_contact'].disabled = False
        form.fields['lot_description'].disabled = False
        form.fields['reserve_price'].disabled = False

    if form.is_valid():
        if request.user.groups.all()[0].name == 'auctioneer':
            if lot.minimal_bid!= 0 and lot.minimum_bid_increment != 0:
                messages.info(request, 'Successful lot edition!')
                form.save()
                return HttpResponseRedirect('/lot_user/edit/' + str(pk) + '/')
            else:
                messages.info(request, 'Please, edit all the required information before submission.')
                return HttpResponseRedirect('/lot_user/edit/' + str(pk) + '/')
        elif request.user.groups.all()[0].name == 'seller':
            if lot.lot_name != "" and lot.lot_description != "" and lot.reserve_price != "" and lot.seller_contact != "":
                messages.info(request, 'Successful lot edition!')
                form.save()
                return HttpResponseRedirect('/lot_user/edit/' + str(pk) + '/')
            else:
                messages.info(request, 'Incomplete form! Please, fill all the required information before submission.')
                return HttpResponseRedirect('/lot_user/edit/' + str(pk) + '/')

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

@login_required
@allowed_users(allowed_roles=['auctioneer', 'seller'])
def lot_remove(request, pk, template_name='auctioneer/auction_list.html'):

    auction_lots = Lot.objects.filter(pk=pk)
    auction_lots.update(number_of_bids_made = 0)
    auction_lots.update(current_winner_buyer = "No one")
    auction_lots.update(highest_value_bid = 0)
    auction_lots.update(auction_ref_id = -999)
    return redirect('auctioneer:auction_list')