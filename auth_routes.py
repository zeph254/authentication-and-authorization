from flask import Blueprint, request, jsonify
from models import User
from models import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/register", methods=["POST"])
def register():    
    data = request.get_json()
    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"})

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user is None or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token})

@auth_blueprint.route("/current_user", methods=["GET"])
@jwt_required()
def current_user():
    user = User.query.get(get_jwt_identity())
    return jsonify(user.to_dict())

@auth_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Logged out"})

@auth_blueprint.route("/user/update", methods=["PUT"])
@jwt_required()
def update_user():
    user = User.query.get(get_jwt_identity())
    data = request.get_json()
    user.username = data["username"]
    user.email = data["email"]
    db.session.commit()
    return jsonify(user.to_dict())

@auth_blueprint.route("/user/updatepassword", methods=["PUT"])
@jwt_required()
def update_password():
    user = User.query.get(get_jwt_identity())
    data = request.get_json()
    user.set_password(data["password"])
    db.session.commit()
    return jsonify({"message": "Password updated"})

@auth_blueprint.route("/user/delete_account", methods=["DELETE"])
@jwt_required()
def delete_account():
    user = User.query.get(get_jwt_identity())
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted"})