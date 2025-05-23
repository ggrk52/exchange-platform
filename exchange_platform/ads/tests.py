from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class AdTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test Description',
            category='electronics',
            condition='new'
        )

    def test_create_ad(self):
        self.assertEqual(self.ad.title, 'Test Ad')

    def test_edit_ad(self):
        self.ad.title = 'Updated Title'
        self.ad.save()
        self.assertEqual(self.ad.title, 'Updated Title')

    def test_delete_ad(self):
        ad_id = self.ad.id
        self.ad.delete()
        with self.assertRaises(Ad.DoesNotExist):
            Ad.objects.get(id=ad_id)