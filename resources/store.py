
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operation on stores")


@blp.route("/stores/<string:id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, id):
        store = StoreModel.query.get_or_404(id)
        return store

    def delete(self, id):
        store = ItemModel.query.get_or_404(id)
        db.session.delete(store)
        db.session.commit()

        return {"message": "Delete store  successfully"}


@blp.route("/stores")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, form_data):
        new_store = StoreModel(**form_data)

        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store that name already exists")

        except SQLAlchemyError:
            abort(500, message="An error occurred")

        return new_store
