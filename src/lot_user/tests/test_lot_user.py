from django.test import TestCase

from django.urls import reverse
from lot_user.models import Lot

from django.contrib.auth.models import User

class CRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Lot.objects.create(
            user = User.objects.create_user(username='testuser1', password='senha'),
            lot_name='Lote#1',
            reserve_price=10,
            sequential_uuid=11,
            minimal_bid=12,
            lot_photo='foo.png',
            seller_contact=911,
            lot_description='it is a lot',
            minimum_bid_increment=13, 
            comissions=14,
            taxes=15,
            number_of_bids_made=16,
            current_winner_buyer='tobias',
            highest_value_bid=17
        )
    
    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    # model tests

    def test_get_lot_name(self):
        lot = Lot.objects.get()
        self.assertEquals('Lote#1', lot.get_lot_name())

    def test_set_lot_name(self):
        lot = Lot.objects.get()
        lot.set_lot_name('Lote#1.1')
        self.assertEquals('Lote#1.1', lot.get_lot_name())

    def test_get_reserve_price(self):
        lot = Lot.objects.get()
        self.assertEquals(10, lot.get_reserve_price())

    def test_set_reserve_price(self):
        lot = Lot.objects.get()
        lot.set_reserve_price(30)
        self.assertEquals(30, lot.get_reserve_price())

    # view tests

    # def test_view_list(self):
    #     response = self.client.get(reverse('lot:lot_list'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'lot/lot_list.html')

    # def test_view_create(self):
    #     response = self.client.get(reverse('lot:lot_new'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'lot/lot_form.html')


