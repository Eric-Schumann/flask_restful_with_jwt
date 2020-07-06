import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('price', type=float, required=True, help="The field 'price' is invalid.")

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200
        return {'message': 'Item not found.'}

    def post(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        results = cursor.execute(query, (name,))
        row = results.fetchone()

        if row:
            return {'message': F"An item with name '{name}' already exists."}, 400
            
        data = self.parser.parse_args()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (name, data['price']))
        connection.commit()
        connection.close()
        return {'item': {'name': name, 'price': data['price']}}, 201

    def put(self, name):
        data = self.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {'message': 'Item deleted.'}


class ItemList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('price', type=float, required=True, help="The field 'price' is invalid.")


    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"

        results = cursor.execute(query)
        rows = results.fetchall()

        items_list = []
        for row in rows:
            items_list.append({"name": row[0], "price": row[1]})

        connection.close()

        return {'items': items_list}