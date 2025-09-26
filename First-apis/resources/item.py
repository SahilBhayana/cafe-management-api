import uuid
from db.item import ItemDatabase
from flask_smorest import Blueprint,abort
from flask.views import MethodView
from schemas import ItemSchema, ItemGetSchema, SuccessMessageSchema,ItemOptionalQuerySchema,ItemQuerySchema
from flask_jwt_extended import jwt_required

blp = Blueprint("items",__name__, description= "Operations on items")


@blp.route("/item")
class Item(MethodView):

    def __init__(self):
        self.db = ItemDatabase()

    @jwt_required()
    @blp.response(200, ItemGetSchema(many=True))
    @blp.arguments(ItemOptionalQuerySchema, location="query")
    def get(self, args):
        id = args.get('id')
        if id is None:
            return self.db.get_items()
        else:
            result = self.db.get_item(id)
            if result is None:
                abort(404,message="record does not found")
            return result
        

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200,SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def put(self,request_data, args):
        id = args.get('id')
        if self.db.update_item(id, request_data):
            return {"message" : "item updated successfully"}
        abort(404, message="record not found")
    

    @jwt_required()
    @blp.response(200,SuccessMessageSchema)
    @blp.arguments(ItemSchema)
    def post(self,request_data):
        id= uuid.uuid4().hex
        self.db.add_item(id, request_data)
        return {"message" : "item added successfully"}, 201
    

    @jwt_required()
    @blp.response(200,SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def delete(self, args):
        id = args.get('id')
        if self.db.delete_item(id):
            return {"message" : "item deleted successfully"}
        abort(404, message="Given id doesn't exist")