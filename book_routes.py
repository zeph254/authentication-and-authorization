from flask import Blueprint, request, jsonify
from models import Book
from models import db
from flask_jwt_extended import jwt_required

book_blueprint = Blueprint("book", __name__)

@book_blueprint.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@book_blueprint.route("/books", methods=["POST"])
@jwt_required()
def create_book():
    data = request.get_json()
    book = Book(title=data["title"], author=data["author"], publication_date=data["publication_date"])
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict())

@book_blueprint.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict())

@book_blueprint.route("/books/<int:book_id>", methods=["PUT"])
@jwt_required()
def update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    data = request.get_json()
    book.title = data["title"]
    book.author = data["author"]
    book.publication_date = data["publication_date"]
    db.session.commit()
    return jsonify(book.to_dict())

@book_blueprint.route("/books/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})