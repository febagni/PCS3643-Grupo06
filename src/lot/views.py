from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from .models import Lot


class LotForm(ModelForm):
    class Meta:
        model = Lot
        fields = [
            # seller
            "lot_name",
            "seller_contact",
            "lot_description",
            "reserve_price",
            # auctioneer
            "minimal_bid",
            "minimum_bid_increment",
            "comissions",
            "taxes",
            # algorithm
            "sequential_uuid",
            "number_of_bids_made",
            "current_winner_buyer",
            "highest_value_bid",
            "is_higher_than_reserve",
        ]


def lot_list(request, template_name="lot/lot_list.html"):
    lot = Lot.objects.all()
    data = {}
    data["object_list"] = lot
    return render(request, template_name, data)


def lot_create(request, template_name="lot/lot_form.html"):
    form = LotForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("lot:lot_list")
    return render(request, template_name, {"form": form})


def lot_update(request, pk, template_name="lot/lot_form.html"):
    lot = get_object_or_404(Lot, pk=pk)
    form = LotForm(request.POST or None, instance=lot)
    if form.is_valid():
        form.save()
        return redirect("lot:lot_list")
    return render(request, template_name, {"form": form})


def lot_delete(request, pk, template_name="lot/lot_confirm_delete.html"):
    lot = get_object_or_404(Lot, pk=pk)
    if request.method == "POST":
        lot.delete()
        return redirect("lot:lot_list")
    return render(request, template_name, {"object": lot})
