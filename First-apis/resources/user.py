from blocklist import BLOCKLIST
from db.user import UserDatabase
from flask_smorest import Blueprint,abort
from flask.views import MethodView
from schemas import SuccessMessageSchema, UserSchema, UserQuerySchema
import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

blp = Blueprint("Users",__name__, description= "Operations on users")

@blp.route("/login")
class UserLogin(MethodView):
    def __init__(self):
        self.db = UserDatabase()
    
    @blp.arguments(UserSchema)
    def post(self,request_data):
        username = request_data['username']
        password = hashlib.sha256(request_data['password'].encode('utf-8')).hexdigest() 
        user_id = self.db.verify_user(username, password)
        if user_id:
            return {"access token": create_access_token(identity=str(user_id))}
        abort(400,message="username or password is invalid")


@blp.route("/logout")
class UserLogout(MethodView):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)    
        return {"message":"successfully logged out"}



@blp.route("/user")
class User(MethodView):

    def __init__(self):
        self.db = UserDatabase()

    @blp.response(200, UserSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def get(self, args):
        id = args.get('id')
        result = self.db.get_user(id)
        if result is None:
            abort(404,message="user does not found")
        print(result)
        return result
    

    @blp.response(200,SuccessMessageSchema)
    @blp.arguments(UserSchema)
    def post(self,request_data):
        username = request_data['username']
        password = hashlib.sha256(request_data['password'].encode('utf-8')).hexdigest() 
        if self.db.add_user( username, password):
            return {"message" : "user added successfully"}, 201
        abort(403,message="user already exist")
    
    @blp.response(200,SuccessMessageSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def delete(self, args):
        id = args.get('id')
        if self.db.delete_user(id):
            return {"message" : "user deleted successfully"}
        abort(404, message="Given id doesn't exist")



