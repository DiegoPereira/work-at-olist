from channels.models import Channel, Categories
from django.test import TestCase, Client
from django.core.management import call_command
from django.utils.six import StringIO
import unittest


class CategoriesTestCase(TestCase):
    def setUp(self):
        self.walmart = Channel.objects.create(name='walmart')
        self.games = Categories.objects.create(name='games',
                                               channel=self.walmart)
        self.nintendo = Categories.objects.create(name='nintendo',
                                                  channel=self.walmart,
                                                  parent=self.games)
        self.console = Categories.objects.create(name='console',
                                                 channel=self.walmart,
                                                 parent=self.nintendo)

    def test_parent_and_children(self):
        self.assertEqual(self.games.channel.id, self.walmart.id)
        self.assertEqual(self.games.get_children()[0].id, self.nintendo.id)

    def test_tree(self):
        self.assertEqual(self.console.get_root().id, self.games.id)
        self.assertTrue(self.nintendo.is_child_node())


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.americanas = Channel.objects.create(name='americanas')
        self.submarino = Channel.objects.create(name='submarino')
        self.games = Categories.objects.create(name='games',
                                               channel=self.americanas)
        self.nintendo = Categories.objects.create(name='nintendo',
                                                  channel=self.americanas,
                                                  parent=self.games)
        self.console = Categories.objects.create(name='console',
                                                 channel=self.americanas,
                                                 parent=self.nintendo)

    def test_responses(self):
        categories_uri = '/channels/categories?channel=americanas'
        relatives_uri = '/channels/relatives?category=games'
        rel_empty_uri = '/channels/relatives?category=gamesxpto'
        cat_empty_uri = '/channels/categories?channel=loja1'
        response_channels = self.client.get('/channels/channels/')

        response_categories = self.client.get(categories_uri)
        response_relatives = self.client.get(relatives_uri)
        self.assertEqual(response_channels.status_code, 200)
        self.assertEqual(response_categories.status_code, 200)
        self.assertEqual(response_relatives.status_code, 200)
        self.assertEqual(response_channels.json().get('count'), 2)
        self.assertEqual(response_categories.json().get('count'), 3)
        self.assertEqual(response_relatives.json()
                         .get('relatives')[0].get('descendants'),
                         ['nintendo', 'console'])
        # Test empty responses
        response_relatives_empty = self.client.get(rel_empty_uri)
        response_categories_empty = self.client.get(cat_empty_uri)
        self.assertEqual(response_relatives_empty.json().get('relatives'), [])
        self.assertEqual(response_categories_empty.json().get('count'), 0)


class ImportcategoriesTest(TestCase):

    def test_command_output(self):
        out = StringIO()
        args = ['a', 'example.csv']
        call_command('importcategories', *args, stdout=out)
        self.assertIn('Successfully imported the channel', out.getvalue())
        call_command('importcategories', *args, stdout=out)
        self.assertIn('Remove channel\'s old records', out.getvalue())
