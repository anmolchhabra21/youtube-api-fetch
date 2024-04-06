from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime

# Flask app configuration (adjust accordingly)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myflaskuser:mypassword@db:5432/myflaskapp'  # Replace with your database details

db = SQLAlchemy(app)

class Video(db.Model):
    __tablename__ = 'Video'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    publish_datetime = db.Column(db.DateTime, nullable=False)
    thumbnail_urls = db.Column(db.JSON) 

    def __repr__(self):
        return f"<Video {self.id}: {self.title}>"

# Function to fetch videos from YouTube Data API (replace with actual API logic)
def fetch_videos(search_query, db, app):
    with app.app_context():
        print("running")
        videos = [
            {
                'title': 'Video 1',
                'description': 'Description 1',
                'publish_datetime': '2022-05-01T00:00:00Z',
                'thumbnails': 'https://via.placeholder.com/150'
            },
            {
                'title': 'Video 2',
                'description': 'Description 2',
                'publish_datetime': '2022-05-02T00:00:00Z',
                'thumbnails': 'https://via.placeholder.com/150'
            },
            {
                'title': 'Video 3',
                'description': 'Description 3',
                'publish_datetime': '2022-05-03T00:00:00Z',
                'thumbnails': 'https://via.placeholder.com/150'
            }
        ]
        print("chk");
        for video in videos:
            video_obj = Video(
                title=video['title'],
                description=video['description'],
                publish_datetime=datetime.now(),
                # publish_datetime=datetime.strptime(video['publish_datetime'], '%Y-%m-%dT%H:%M:%SZ'),
                thumbnail_urls=[video['thumbnails']]
            )
            db.session.add(video_obj)

        db.session.commit()
        return videos

# Background task to periodically fetch videos (replace with your desired scheduling logic)

scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_videos, trigger="interval", seconds=10, args=["internships", db, app])  # Replace with your search query


# API route to retrieve paginated video data
@app.route('/videos', methods=['GET'])
def get_videos():
    print("3")
    page = request.args.get('page', 1, type=int)  # Default to page 1
    per_page = request.args.get('per_page', 10, type=int)  # Default to 10 videos per page

    pagination = Video.query.order_by(Video.publish_datetime.desc()).paginate(page=page, per_page=per_page, error_out=False)
    videos = pagination.items
    total = pagination.total

    return jsonify({
        'videos': [serialize_video(video) for video in videos],
        'page': page,
        'per_page': per_page,
        'total': total
    })

@app.route('/', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok'
    })

# Helper function to serialize Video objects (customize as needed)
def serialize_video(video):
    return {
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'publish_datetime': video.publish_datetime.isoformat(),
        'thumbnail_urls': video.thumbnail_urls
    }

with app.app_context():
    print("1")  
    db.create_all()
    scheduler.start()
    print("2")

if __name__ == '__main__':    
    app.run(debug=True)

