from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from .models import Auction
from lot_user.views import LotForm
from lot_user.models import Lot

from datetime import date, datetime, timedelta
from apps.decorators import *

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus.flowables import Image

from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import purple, PCMYKColor, red, Color, CMYKColor, yellow
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF

class AuctionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['auction_status'].disabled = True
        self.fields['auction_status'].required = False
        self.fields['auction_published'].disabled = True
        self.fields['auction_published'].required = False
        self.fields['auction_published'].initial = False
    class Meta:
        model = Auction
        fields = ('auction_id', 'auction_start', 'auction_end', 'auctioneer', 'auction_status', 'auction_published')

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
    lot = get_object_or_404(Lot, pk=id)
    lot.auction_ref_id = pk
    lot.save()

    return redirect('auctioneer:auction_list')

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_publish(request, pk, template_name='auctioneer/auction_list.html'):
    auction= get_object_or_404(Auction, pk=pk)
    auction.auction_published = True
    auction.save()
    return redirect('auctioneer:auction_list')

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_cancel(request, pk, template_name='auctioneer/auction_list.html'):
    auction= get_object_or_404(Auction, pk=pk)
    auction.auction_published = False
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

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_performance_report(request, pk):
    auc = Auction.objects.filter(pk=pk)
    auction_id = auc.values_list('auction_id')[0][0]

    buffer = io.BytesIO()
    canv = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
    textob = canv.beginText()
    #im = Image("../theme/static/images/logo.png", width=2*inch, height=2*inch)
    # canv.drawImage(image="theme/static/images/background_image.jpeg", x=0,y=0, width=500.0,height=500.0,mask=None)
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 16)
    textob.textLine("")
    textob.textLine("Performance Report")
    textob.setFont("Helvetica", 12)
    canv.drawImage(image="theme/static/images/BidCoin.png", x=20.0,y=20.0, width=134.4,height=33.0,mask=None, preserveAspectRatio='nw')

    lots = Lot.objects.filter(auction_ref_id=auction_id)
    lines = [
        "",
        "User: " + str(request.user),
        "Auction ID: " + str(auction_id),
        ""
    ]
    for i in range(len(lots)):
        lot_name = lots.values_list('lot_name')[i][0]
        bids_made = lots.values_list('number_of_bids_made')[i][0]
        lines.append("Lot Name: " + str(lot_name))
        lines.append("Number of Bids Made: " + str(bids_made))
        lines.append("")
    for line in lines:
        textob.textLine(line)

    drawing = Drawing(300, 150)
    lc = HorizontalLineChart()
    lc.x = 20
    lc.y = 200
    lc.height = 120
    lc.width = 240
    drawing.hAlign = 'CENTER'
    drawing.add(lc)

    bc = VerticalBarChart()
    bc.height = 120
    bc.width = 240
    bc.barSpacing = 4
    bc.barWidth = 14
    drawing.add(bc)

    drawing.save()
    renderPDF.draw(drawing, canv, x=250, y=100, showBoundary=False)

    canv.drawText(textob)
    canv.showPage()
    canv.save()
    buffer.seek(0)
    
    file = "auction" + ".pdf"

    return FileResponse(buffer, as_attachment=True, filename=file)

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_financial_report(request, pk):
    auc = Auction.objects.filter(pk=pk)
    auction_id = auc.values_list('auction_id')[0][0]

    buffer = io.BytesIO()
    canv = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
    textob = canv.beginText()
    #im = Image("../theme/static/images/logo.png", width=2*inch, height=2*inch)
    # canv.drawImage(image="theme/static/images/background_image.jpeg", x=0,y=0, width=500.0,height=500.0,mask=None)
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 16)
    textob.textLine("")
    textob.textLine("Financial Report")
    textob.setFont("Helvetica", 12)
    canv.drawImage(image="theme/static/images/BidCoin.png", x=20.0,y=20.0, width=134.4,height=33.0,mask=None, preserveAspectRatio='nw')

    lots = Lot.objects.filter(auction_ref_id=auction_id)
    lines = [
        "",
        "User: " + str(request.user),
        "Auction ID: " + str(auction_id),
        ""
    ]
    for i in range(len(lots)):
        lot_name = lots.values_list('lot_name')[i][0]
        bids_made = lots.values_list('number_of_bids_made')[i][0]
        highest_value_bid = lots.values_list('highest_value_bid')[i][0]
        current_winner_buyer = lots.values_list('current_winner_buyer')[i][0]
        comissions = lots.values_list('comissions')[i][0]
        taxes = lots.values_list('taxes')[i][0]

        lines.append("Lot Name: " + str(lot_name))
        lines.append("Number of Bids Made: " + str(bids_made))
        lines.append("Winner Bid: $" + str(highest_value_bid))
        lines.append("Winner username: " + str(current_winner_buyer))
        lines.append("Comissions: " + str(comissions) + "%")
        lines.append("Taxes: " + str(taxes) + "%")
        lines.append(" ")
        

    for line in lines:
        textob.textLine(line)

    drawing = Drawing(300, 150)
    lc = HorizontalLineChart()
    lc.x = 20
    lc.y = 200
    lc.height = 120
    lc.width = 240
    drawing.hAlign = 'CENTER'
    drawing.add(lc)

    bc = VerticalBarChart()
    bc.height = 120
    bc.width = 240
    bc.barSpacing = 4
    bc.barWidth = 14
    drawing.add(bc)

    drawing.save()
    renderPDF.draw(drawing, canv, x=270, y=100, showBoundary=False)

    canv.drawText(textob)
    canv.showPage()
    canv.save()
    buffer.seek(0)
    
    file = "auction" + ".pdf"

    return FileResponse(buffer, as_attachment=True, filename=file)
