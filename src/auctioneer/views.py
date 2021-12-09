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
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus.flowables import Image
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

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
    if lot.reserve_price <= 1000:
        lot.taxes =  1
        lot.comissions = 3
    elif lot.reserve_price > 1000 and lot.reserve_price <= 10000:
        lot.taxes = 2
        lot.comissions = 4
    elif lot.reserve_price > 10000 and lot.reserve_price < 50000:
        lot.taxes = 3
        lot.comissions = 5
    elif lot.reserve_price > 50000 and lot.reserve_price < 100000:
        lot.taxes = 4
        lot.comissions = 6
    else:
        lot.taxes = 5
        lot.comissions = 7
        
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

    all_lots = Lot.objects.all()
    for i in range(len(all_lots)):
        lot_ref_id = Lot.objects.values_list('auction_ref_id')[i][0]
        if (lot_ref_id == auction.auction_id):
            auction_lots = Lot.objects.filter(pk=Lot.objects.values_list('id')[i][0])
            auction_lots.update(number_of_bids_made = 0)
            auction_lots.update(current_winner_buyer = "No one")
            auction_lots.update(highest_value_bid = 0)
            auction_lots.update(auction_ref_id = -999)
            
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

def report_header(title):
    buffer = io.BytesIO()
    canv = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
    textob = canv.beginText()
    
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 20)
    textob.textLine("")
    textob.textLine(title)
    textob.setFont("Helvetica", 12)
    img = os.path.join(__location__, "../theme/static/images/BidCoin.png")
    canv.drawImage(image=img, x=20.0,y=20.0, width=134.4,height=33.0,mask=None, preserveAspectRatio='nw')

    return buffer, canv, textob

@login_required
@allowed_users(allowed_roles=['auctioneer'])
def auction_performance_report(request, pk):
    auc = Auction.objects.filter(pk=pk)
    auction_id = auc.values_list('auction_id')[0][0]

    buffer, canv, textob = report_header("Performance Report")

    lots = Lot.objects.filter(auction_ref_id=auction_id)
    lines = [
        "",
        "User: " + str(request.user),
        "Auction ID: " + str(auction_id),
        ""
    ]

    for line in lines:
        textob.textLine(line)

    tab_data = []

    for i in range(len(lots)):
        lot_name = lots.values_list('lot_name')[i][0]
        bids_made = lots.values_list('number_of_bids_made')[i][0]
        current_winner_buyer = lots.values_list('current_winner_buyer')[i][0]
        
        if lots.values_list('is_higher_than_reserve')[i][0] == "TRUE":
            tab_data.append([" "])
            tab_data.append(["Number of Bids Made: " + str(bids_made)])
            tab_data.append(["Winner username: " + str(current_winner_buyer)])
            tab_data.append(["Lot Name: " + str(lot_name)])
            tab_data.append([" "])
        else:
            tab_data.append(["The reserve price could not be matched."])
            tab_data.append(["Lot Name: " + str(lot_name)])
            tab_data.append([" "])


    width = 400
    height = 100
    x = 70
    y = 150
    f = Table(tab_data)
    GRID_STYLE = TableStyle(
        [
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#00FFFFFF')),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('LINEAFTER', (0,0), (-1,-1), 0.25, colors.black),

        ]
    )
    f.setStyle(GRID_STYLE)
    f.wrapOn(canv, width, height)
    f.drawOn(canv, x, y)

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

    buffer, canv, textob = report_header("Financial Report")

    lots = Lot.objects.filter(auction_ref_id=auction_id)
    lines = [
        "",
        "User: " + str(request.user),
        "Auction ID: " + str(auction_id),
        ""
    ]

    for line in lines:
        textob.textLine(line)

    tab_data = []
    gross_revenue = 0
    liquid_revenue = 0

    for i in range(len(lots)):
        lot_name = lots.values_list('lot_name')[i][0]
        bids_made = lots.values_list('number_of_bids_made')[i][0]
        highest_value_bid = lots.values_list('highest_value_bid')[i][0]
        current_winner_buyer = lots.values_list('current_winner_buyer')[i][0]
        comissions = lots.values_list('comissions')[i][0]
        taxes = lots.values_list('taxes')[i][0]

        if lots.values_list('is_higher_than_reserve')[i][0] == "TRUE":
            tab_data.append([" "])
            tab_data.append(["Taxes: " + str(taxes) + "% = USD" + str(taxes*highest_value_bid/100)])
            tab_data.append(["Comissions: " + str(comissions) + "% = USD"+ str(comissions*highest_value_bid/100)])
            tab_data.append(["Number of Bids Made: " + str(bids_made)])
            tab_data.append(["Winner username: " + str(current_winner_buyer)])
            tab_data.append(["Winner Bid: USD" + str(highest_value_bid)])
            tab_data.append(["Lot Name: " + str(lot_name)])
            tab_data.append([" "])
        
            gross_revenue = gross_revenue + highest_value_bid
            liquid_revenue = gross_revenue - taxes*highest_value_bid/100

    tab_data.append(["Auction liquid revenue: USD" + str(liquid_revenue)])
    tab_data.append(["Auction gross revenue: USD" + str(gross_revenue)])

    tab_data.append([" "])

    width = 400
    height = 100
    x = 70
    y = 150
    f = Table(tab_data)
    GRID_STYLE = TableStyle(
        [
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#00FFFFFF')),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('LINEAFTER', (0,0), (-1,-1), 0.25, colors.black),

        ]
    )
    f.setStyle(GRID_STYLE)
    f.wrapOn(canv, width, height)
    f.drawOn(canv, x, y)

    canv.drawText(textob)
    canv.showPage()
    canv.save()
    buffer.seek(0)
    
    file = "auction.pdf"

    return FileResponse(buffer, as_attachment=True, filename=file)


@login_required
@allowed_users(allowed_roles=['auctioneer'])
def full_performance_report(request):
    auction = Auction.objects.all()

    total_auctions = len(auction)
    total_finished_lot_bids = 0
    total_not_finished_lot_bids = 0

    total_finished_lots = 0
    total_not_finished_lots = 0
    
    buffer, canv, textob = report_header("Full Performance Report")
    textob.textLine("User: " + str(request.user))

    for index in range(total_auctions):
        if auction.values_list('auction_status')[index][0] == "FINISHED":
            auction_id = auction.values_list('auction_id')[index][0]
            start_date = auction.values_list('auction_start')[index][0]
            end_date = auction.values_list('auction_end')[index][0]
            
            lines = [
                "",
                "Auction ID: " + str(auction_id),
                "Start date: " + str(start_date.date()),
                "End date: " + str(end_date.date()),
            ]

            for line in lines:
                textob.textLine(line)

            tab_data = []
            lots = Lot.objects.filter(auction_ref_id=auction_id)
            number_of_lots = len(lots)

            finished_lots = 0
            not_finished_lots = 0

            for i in range(number_of_lots):
                
                if lots.values_list('is_higher_than_reserve')[i][0] == "TRUE":
                    finished_lots = finished_lots + 1
                    total_finished_lot_bids = total_finished_lot_bids + lots.values_list('number_of_bids_made')[i][0]
                else:
                    not_finished_lots = not_finished_lots + 1
                    total_not_finished_lot_bids = total_not_finished_lot_bids + lots.values_list('number_of_bids_made')[i][0]

            total_finished_lots = total_finished_lots + finished_lots
            total_not_finished_lots = total_not_finished_lots + not_finished_lots

            textob.textLine(" ")
            textob.textLine("Auction performance: ")
            textob.textLine("Number of sold lots in this auction: " + str(finished_lots))
            textob.textLine("Number of unsold lots in this auction: " + str(not_finished_lots))
    
    textob.textLine(" ")
    textob.setFont("Helvetica", 16)
    textob.textLine("General performance: ")
    textob.setFont("Helvetica", 14)
    textob.textLine("Total number of auctions: " + str(total_auctions))
    textob.textLine("Number of sold lots in this period: " + str(total_finished_lots))
    textob.textLine("Number of unsold lots in this period: " + str(total_not_finished_lots))

    canv.drawText(textob)
    canv.showPage()
    canv.save()
    buffer.seek(0)
    
    file = "full_auction_performance_report.pdf"

    return FileResponse(buffer, as_attachment=True, filename=file)



@login_required
@allowed_users(allowed_roles=['auctioneer'])
def full_financial_report(request):
    auction = Auction.objects.all()

    total_auctions = len(auction)
    total_gross_revenue = 0
    total_taxes_revenue = 0
    total_comission_revenue = 0
    
    buffer, canv, textob = report_header("Full Financial Report")
    
    textob.textLine("User: " + str(request.user))

    for index in range(total_auctions):
        auction_id = auction.values_list('auction_id')[index][0]
        start_date = auction.values_list('auction_start')[index][0]
        end_date = auction.values_list('auction_end')[index][0]
        
        lines = [
            "",
            "Auction ID: " + str(auction_id),
            "Start date: " + str(start_date.date()),
            "End date: " + str(end_date.date()),
            ""
        ]

        for line in lines:
            textob.textLine(line)

        lots = Lot.objects.filter(auction_ref_id=auction_id)
        number_of_lots = len(lots)

        gross_revenue = 0
        taxes_revenue = 0
        comission_revenue = 0

        for i in range(number_of_lots):
            
            highest_value_bid = lots.values_list('highest_value_bid')[i][0]
            comissions = lots.values_list('comissions')[i][0]
            taxes = lots.values_list('taxes')[i][0]

            if lots.values_list('is_higher_than_reserve')[i][0] == "TRUE":
                gross_revenue = gross_revenue + highest_value_bid
                comission_revenue = comission_revenue + comissions*highest_value_bid/100
            taxes_revenue = taxes_revenue + taxes*highest_value_bid/100
        
        total_gross_revenue = total_gross_revenue + gross_revenue
        total_taxes_revenue = total_taxes_revenue + taxes_revenue 
        total_comission_revenue = total_comission_revenue + comission_revenue 

        textob.textLine("Auction taxes revenue: USD" + str(taxes_revenue))
        textob.textLine("Auction comission revenue: USD" + str(comission_revenue))
        textob.textLine("Auction gross revenue: USD" + str(gross_revenue))


    textob.textLine(" ")
    textob.setFont("Helvetica", 16)
    textob.textLine("General performance: ")
    textob.setFont("Helvetica", 14)
    textob.textLine("Taxes revenue of this period: USD" + str(total_taxes_revenue))
    textob.textLine("Comissions revenue of this period: USD" + str(total_comission_revenue))
    textob.textLine("Gross revenue of this period: USD" + str(total_gross_revenue))

    canv.drawText(textob)
    canv.showPage()
    canv.save()
    buffer.seek(0)
    
    file = "full_auction_financial_report.pdf"

    return FileResponse(buffer, as_attachment=True, filename=file)