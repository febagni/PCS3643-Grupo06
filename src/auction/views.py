from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from .models import Auction

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('auction_id', 'auction_start', 'auction_end', 'available_lot_list', 'auctioneer', 'auction_winner')

def auction_list(request, template_name='auction/auction_list.html'):
    auction = Auction.objects.all()
    data = {}
    data['object_list'] = auction
    return render(request, template_name, data)

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