from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Article, article_schema, articles_schema
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE_URI = 'sqlite:///articles.db'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

db.init_app(app)  # Use this to initialize with the app

@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())

@app.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify(articles_schema.dump(articles))

@app.route('/articles', methods=['POST'])
def add_article():
    data = request.get_json()
    article = Article(title=data['title'], content=data['content'])
    db.session.add(article)
    db.session.commit()
    return jsonify(article_schema.dump(article)), 201

@app.after_request
def log_response(response):
    app.logger.info('Response status: %s', response.status)
    app.logger.info('Response headers: %s', response.headers)
    return response

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
