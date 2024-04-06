from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Video(db.Model):
    __tablename__ = 'Video'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    publish_datetime = db.Column(db.DateTime, nullable=False)
    thumbnail_urls = db.Column(db.JSON)  # Store multiple thumbnails as a list of URLs

    def __repr__(self):
        return f"<Video {self.id}: {self.title}>"