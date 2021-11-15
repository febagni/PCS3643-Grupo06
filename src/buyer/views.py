from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from lot_user.views import LotForm
from lot_user.models import Lot

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

@login_required
@allowed_users(allowed_roles=['buyer'])
def bid_request(request, pk, template_name='buyer/bid_form.html'):
    lot = get_object_or_404(Lot, pk=pk)
    if request.method == 'POST':
        if 'value1' in request.POST:
            # …
            pass
        

    return render(request, template_name, {'form':form})

