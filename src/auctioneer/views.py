from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from .models import Auction

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('auction_id', 'auction_start', 'auction_end', 'available_lot_list', 'auctioneer', 'auction_winner')

@login_required
def auction_list(request, template_name='auctioneer/auction_list.html'):
    if request.user.is_superuser:
        auction = Auction.objects.all()
    else:
        auction = Auction.objects.filter(user=request.user)
    data = {}
    data['object_list'] = auction
    return render(request, template_name, data)

@login_required
def auction_create(request, template_name='auctioneer/auction_form.html'):
    form = AuctionForm(request.POST or None)
    if form.is_valid():
        auction = form.save(commit=False)
        auction.user = request.user
        auction.save()
        return redirect('auctioneer:auction_list')
    return render(request, template_name, {'form':form})

@login_required
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
def auction_delete(request, pk, template_name='auctioneer/auction_confirm_delete.html'):
    if request.user.is_superuser:
        auction= get_object_or_404(Auction, pk=pk)
    else:
        auction= get_object_or_404(Auction, pk=pk, user=request.user)   
    if request.method=='POST':
        auction.delete()
        return redirect('auctioneer:auction_list')
    return render(request, template_name, {'object':auction})
