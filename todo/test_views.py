from django.test import TestCase
from .models import Item


class TestViews(TestCase):
    def test_get_todo_list(self):
        response = self.client.get('/todo/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo.html')

    def test_get_add_items_page(self):
        response = self.client.get('/add_todo')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/add_todo.html')
    
    def test_get_edit_items_page(self):
        item = Item.objects.create(name='Test Todo Item')
        response = self.client.get(f'/edit/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/edit_todo.html')

    def test_can_add_items(self):
        response = self.client.post('/add_todo', {'name': 'Test Added Item'})
        self.assertRedirects(response, '/todo/')

    def test_can_delete_items(self):
        item = Item.objects.create(name='Test Todo Item')
        response = self.client.get(f'/delete/{item.id}')
        self.assertRedirects(response, '/todo/')
        existing_items = Item.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)      
              
    def test_can_toggle_items(self):
        item = Item.objects.create(name='Test Todo Item', done='True')
        response = self.client.get(f'/toggle/{item.id}')
        self.assertRedirects(response, '/todo/')
        updated_item = Item.objects.get(id=item.id)
        self.assertFalse(updated_item.done)
