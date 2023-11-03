from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)

    def __init__(self, title, content):
        self.title = title
        self.content = content

class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
