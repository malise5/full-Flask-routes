import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operation on stores")


@blp.route("/items/<string:id>")
class Item(MethodView):

    # get specific itemm by id
    @blp.response(200, ItemSchema)
    def get(self, id):
        item = ItemModel.query.get_or_404(id)
        return item

    # Update a specific item by id
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemSchema())
    def put(self, form_data, id):
        item = ItemModel.query.get(id)
        if item:
            item.price = form_data["price"]
            item.name = form_data["name"]
        else:
            item = ItemModel(id=id, **form_data)

        db.session.add(item)
        db.session.commit()

        return item

    # Delete a specific item by id
    def delete(self, id):
        item = ItemModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()

        return {"message": "Delete item  successfully"}, 200


@blp.route("/items")
class itemList(MethodView):

    # get all items
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    # create new item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, form_data):
        item = ItemModel(**form_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "An error has occurred")

        return item, 201
