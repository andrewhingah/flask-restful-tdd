eimport unittest
import json
from copy import deepcopy
import app

class AppTestCase(unittest.TestCase):
	def setUp(self):
		self.backup_items = deepcopy(app.items)
		self.app = app.app.test_client()
		self.app.testing = True
	def test_get(self):
		"""
		tests fetch all items
		"""
		response = self.app.get('/items')
		assert response.status_code == 200
	def test_post(self):
		"""
		tests user can post a single question
		"""
		item = {"name": "bag"}
		response = self.app.post('/items',
			data=json.dumps(item),
			content_type='application/json')
		assert response.status_code == 201
	def test_get_one_item(self):
		"""
		tests one can fetch a specific
		question by id
		"""
		response = self.app.get('/items/1')
		assert response.status_code == 200

	def test_get_no_item(self):
		"""
		tests that a non existing item
		cannot be retrieved
		"""
		response = self.app.get('/items/100')
		assert response.status_code == 404

	def test_delete(self):
		"""
		tests an item can be deleted by id
		"""
		response = self.app.delete('/items/1')
		assert response.status_code == 200
		assert response.data == b'{"message": "item deleted"}\n'
	def test_delete_no_item(self):
		"""
		tests a non existing item cannot be deleted
		"""
		response = self.app.delete('/items/99')
		assert response.status_code == 404

	def test_put(self):
		"""
		test that an item can be edited
		or added if it doesn't exist
		"""
		item = {"name":"hen"}
		response = self.app.put('/items/1',
			data=json.dumps(item),
			content_type='application/json')
		assert response.status_code == 200
		assert b'hen' in response.data

	def tearDown(self):
		app.items = self.backup_items

if __name__ == '__main__':
	unittest.main()