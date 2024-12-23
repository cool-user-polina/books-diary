from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask import Response
import json
from flask_cors import CORS  # Импортируем CORS


app = Flask(__name__)
CORS(app)  # Включаем CORS для всех маршрутов
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///base.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    books = db.relationship('Books', back_populates='author', cascade='all, delete-orphan')

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    ganre = db.Column(db.String(50), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    author = db.relationship('Author', back_populates='books')
    impression = db.relationship('Impression', back_populates='books', cascade='all, delete-orphan')
    notes = db.relationship('Notes', back_populates='books', cascade='all, delete-orphan')

class Impression(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    impression = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    books = db.relationship('Books', back_populates='impression')

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    notes = db.Column(db.Text, nullable=True)
    books = db.relationship('Books', back_populates='notes')

@app.route('/books', methods=['GET'])
def books():
    book_list = Books.query.all()
    # Преобразуем список книг в JSON
    books = [
        {
            "id": book.id,
            "name": book.name,
            "author_id": book.author_id,
            "author":  book.author.author if book.author else None,
            "ganre": book.ganre,
            "year": book.year,
        }
        for book in book_list
    ]
    return Response(json.dumps(books, ensure_ascii=False), content_type="application/json")

@app.route('/create-books', methods=['POST'])
def create():
    data = request.get_json()  # Получение данных из JSON-запроса
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    # json = {"name": "", "author" : "", "ganre": "", "year":""}
    name = data.get('name')
    author_name = data.get('author')
    ganre = data.get('ganre')
    year = data.get('year')

    # author = db.query(Author).filter(Author.author.ilike(f'%{author_name}%')).first()
    author = Author.query.filter(Author.author.like(f'%{author_name}%')).first()
    if author:
         new_book = Books(name=name, author_id=author.id)
         db.session.add(new_book)
         db.session.commit()
         return jsonify({"message": "Book Created Successfully!", "book_id": new_book.id}), 201
    else:
        return jsonify({"error": "error, author not found!"})

    # if not name or not author_id:
    #     return jsonify({"error": "Name and author_id are required"}), 400

    # new_book = Books(name=name, author_id=author_id)
    # db.session.add(new_book)
    # db.session.commit()

    # return jsonify({"message": "Book Created Successfully!", "book_id": new_book.id}), 201
    




@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Извлечение книги из базы данных по id
    book = Books.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Формирование данных для ответа
    book_data = {
        "id": book.id,
        "name": book.name,
        "ganre": book.ganre,
        "year": book.year,
        "author": book.author.author if book.author else None,
        "impressions": [
            {
                "id": imp.id,
                "impression": imp.impression,
                "rating": imp.rating,
            } for imp in book.impression
        ],
        "notes": [
            {
                "id": note.id,
                "notes": note.notes,
            } for note in book.notes
        ],
    }

    # Возвращаем данные в формате JSON
    return Response(json.dumps(book_data, ensure_ascii=False), content_type="application/json")



if __name__ == '__main__':
    app.run(debug=True)
