from django.forms import ModelForm

from apps.decorators import *
from buyer.models import Buyer

class BuyerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['auction_id'].required = False
        self.fields['auction_id'].disabled = True
        self.fields['auction_id'].initial = 0

        self.fields['lot_id'].required = False
        self.fields['lot_id'].disabled = True
        self.fields['lot_id'].initial = 0

        self.fields['bid_value'].required = True
        self.fields['bid_value'].disabled = False
        self.fields['bid_value'].initial = 0

    class Meta:
        model = Buyer
        fields = [ 
            #seller
            'auction_id',
            'lot_id',
            'bid_value', 
        ]


