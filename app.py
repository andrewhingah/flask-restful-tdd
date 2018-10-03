from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
from flask_jwt_extended import JWTManager

import random

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)


items = [{'item_id':1, 'name':'unga'}]
class Items(Resource):
	# @jwt_required
	def get (self):
		return {'items':items}, 200


	# @jwt_required
	def post (self):
		data = request.get_json()
		item_id = items[-1].get("item_id") + 1
		# item_id = random.randint(0,100)
		item = {'name':data['name'], 'item_id': item_id }
		items.append(item)
		return item, 201

class Item(Resource):
	def get (self,item_id):
		# item = next(filter(lambda x: x['item_id'] == item_id, items),
		# 	None)
		# return {'item':item}, 200 if item else 404
		for item in items:
			if item['item_id'] == item_id:
				return {'item':item}, 200
		return {"message": "item not found"}, 404


	def delete(self, item_id):
		# item = [item for item in items if item['item_id'] == item_id]
		# if item_id is None:
		# 	return {'message': 'item not found'}
		# items.remove(item[0])
		# global items
		# items = list(filter(lambda x: x['item_id'] != item_id, items))
		# if item_id is None:
		# 	return {"message":"item doesn't exist"}, 404
		# return {'message':'item deleted'} #research about status code for deletion
		# return {}, 204

		for item in items:
			if item['item_id'] == item_id:
				items.remove(item)
				return {'message':'item deleted'}, 200
		return {'message':'item not found'}, 404

	def put(self,item_id):
		data = request.get_json()
		item = next(filter(lambda x:x['item_id']==item_id, items),None)
		if item is None:
			item_id = items[-1].get("item_id") + 1
			item = {'name':data['name'], 'item_id':item_id}
			items.append(item)
		else:
			item.update(data)
		return item


api.add_resource(Items,'/items')
api.add_resource(Item,'/items/<int:item_id>')

if __name__ == '__main__':
	app.run(debug = True)