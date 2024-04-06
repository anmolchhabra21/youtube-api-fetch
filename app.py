from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import config
from datetime import datetime

# Flask app configuration (adjust accordingly)
app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

# Video data model (replace with your desired fields)
class Video(db.Model):
    __tablename__ = 'Video'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    publish_datetime = db.Column(db.DateTime, nullable=False)
    thumbnail_urls = db.Column(db.JSON)  # Store multiple thumbnails as a list of URLs

    def __repr__(self):
        return f"<Video {self.id}: {self.title}>"


def fetch_videos(search_query, db, app):
    with app.app_context():
        print("running")
        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': search_query,
            'type': 'video',
            'publishedAfter': '2022-05-01T00:00:00Z',
            'maxResults': 10,
            'order': 'date',
        }

        for api_key in app.config['API_KEYS']:
            params['key'] = api_key
            response = requests.get(url, params=params)
            print("status", response.status_code)
            if response.status_code == 200:
                videos = response.json().get('items', [])
                for video in videos:
                    video_obj = Video(
                        title=video['snippet']['title'],
                        description=video['snippet']['description'],
                        publish_datetime=datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                        thumbnail_urls=[video['snippet']['thumbnails']['default']['url']]
                    )
                    db.session.add(video_obj)
                db.session.commit()
                return videos
            elif response.status_code == 403:  # Quota exceeded error
                continue  # Try the next API key
            else:
                break  # Some other error occurred, break the loop


scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_videos, trigger="interval", seconds=60, args=["sports", db, app])  # Replace with your search query


# API route to retrieve paginated video data
@app.route('/videos', methods=['GET'])
def get_videos():
    page = request.args.get('page', 1, type=int)  # Default to page 1
    per_page = request.args.get('per_page', 10, type=int)  # Default to 10 videos per page

    if 'page' not in request.args or 'per_page' not in request.args:
        return redirect(url_for('get_videos', page=page, per_page=per_page))
    
    pagination = Video.query.order_by(Video.publish_datetime.desc()).paginate(page=page, per_page=per_page, error_out=False)
    videos = pagination.items
    total = pagination.total
    
    videos = {
        'videos': [serialize_video(video) for video in videos],
        'page': page,
        'per_page': per_page,
        'total': total
    }
    return render_template('home.html', videos = videos)

@app.route('/', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'msg': 'Please head over to http://localhost:5000/videos?page=3&per_page=10'
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

