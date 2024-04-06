from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime

# Flask app configuration (adjust accordingly)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myflaskuser:mypassword@db:5432/myflaskapp'  # Replace with your database details

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

# Function to fetch videos from YouTube Data API (replace with actual API logic)
def fetch_videos(search_query, db, app):
    with app.app_context():
        print("running")
        # Simulate API call (replace with actual YouTube Data API integration)
        videos=[{
    'kind': 'youtube#searchResult',
    'etag': 'eOU03aAOf0NWxNJVpBwFraYaeY4',
    'id': {
        'kind': 'youtube#video',
        'videoId': 'Gz22x60i9To'
    },
    'snippet': {
        'publishedAt': '2024-04-06T06:30:06Z',
        'channelId': 'UCb29f7G7wHiFLxz8yzkyFag',
        'title': 'IISC-CBRAIN INTERNSHIPS 2024 || Rs 20,000 pm fellowship || UG/PG #iiscbangalore #internship',
        'description': 'Link- https://cbr-iisc.ac.in/cbrain-internships-2024/ Email ID- drneelabhinstantbiology@gmail.com Link to Purchase Bioprocess ...',
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/Gz22x60i9To/default.jpg',
                'width': 120,
                'height': 90
            },
            'medium': {
                'url': 'https://i.ytimg.com/vi/Gz22x60i9To/mqdefault.jpg',
                'width': 320,
                'height': 180
            },
            'high': {
                'url': 'https://i.ytimg.com/vi/Gz22x60i9To/hqdefault.jpg',
                'width': 480,
                'height': 360
            }
        },
        'channelTitle': 'Instant Biology by Dr. Neelabh',
        'liveBroadcastContent': 'none',
        'publishTime': '2024-04-06T06:30:06Z'
    }
}, {
    'kind': 'youtube#searchResult',
    'etag': 'IeME9AbdRe1L8HCM-mt3k0U22XI',
    'id': {
        'kind': 'youtube#video',
        'videoId': 'XAZTxOJflcU'
    },
    'snippet': {
        'publishedAt': '2024-04-06T06:15:01Z',
        'channelId': 'UCzyL4UTA1PTTroj7aFaJmuw',
        'title': 'Off-Campus Hiring😍| Software Engineer Job Internships for Fresher | Salary 30k/M🔥 #jobswithshubham',
        'description': 'Apply link : Seagate Apply link:- https://seagatecareers.com/job/Pune-Intern-Data-Science/1126888900/ Pinnacle Apply ...',
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/XAZTxOJflcU/default.jpg',
                'width': 120,
                'height': 90
            },
            'medium': {
                'url': 'https://i.ytimg.com/vi/XAZTxOJflcU/mqdefault.jpg',
                'width': 320,
                'height': 180
            },
            'high': {
                'url': 'https://i.ytimg.com/vi/XAZTxOJflcU/hqdefault.jpg',
                'width': 480,
                'height': 360
            }
        },
        'channelTitle': 'JobsWithShubham',
        'liveBroadcastContent': 'none',
        'publishTime': '2024-04-06T06:15:01Z'
    }
}, {
    'kind': 'youtube#searchResult',
    'etag': '2xPfeQwkBIDFqYUM6Qct128VKOQ',
    'id': {
        'kind': 'youtube#video',
        'videoId': 'wxYF1JUFVuY'
    },
    'snippet': {
        'publishedAt': '2024-04-06T04:19:09Z',
        'channelId': 'UCBck2rlnKhisJtHXvoj8RCA',
        'title': 'Subscribe to know more about Supreme Court and internships ❤.',
        'description': 'lawwithag #supremecourt #internship.',
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/wxYF1JUFVuY/default.jpg',
                'width': 120,
                'height': 90
            },
            'medium': {
                'url': 'https://i.ytimg.com/vi/wxYF1JUFVuY/mqdefault.jpg',
                'width': 320,
                'height': 180
            },
            'high': {
                'url': 'https://i.ytimg.com/vi/wxYF1JUFVuY/hqdefault.jpg',
                'width': 480,
                'height': 360
            }
        },
        'channelTitle': 'Law With AG',
        'liveBroadcastContent': 'none',
        'publishTime': '2024-04-06T04:19:09Z'
    }
}, {
    'kind': 'youtube#searchResult',
    'etag': 'LZhICqJ3VHCl2k4S9UxdqZKoYBM',
    'id': {
        'kind': 'youtube#video',
        'videoId': 'AFgbeFIGVsc'
    },
    'snippet': {
        'publishedAt': '2024-04-05T23:19:55Z',
        'channelId': 'UC_W-_nnyeZUXW96LxMwdCrw',
        'title': 'How to get hired for internships: Standout strategies by Expert | iDreamCareer',
        'description': "Are you struggling to get noticed for internship opportunities despite sending out countless applications? Don't miss our upcoming ...",
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/AFgbeFIGVsc/default.jpg',
                'width': 120,
                'height': 90
            },
            'medium': {
                'url': 'https://i.ytimg.com/vi/AFgbeFIGVsc/mqdefault.jpg',
                'width': 320,
                'height': 180
            },
            'high': {
                'url': 'https://i.ytimg.com/vi/AFgbeFIGVsc/hqdefault.jpg',
                'width': 480,
                'height': 360
            }
        },
        'channelTitle': 'iDreamCareer',
        'liveBroadcastContent': 'none',
        'publishTime': '2024-04-05T23:19:55Z'
    }
}, {
    'kind': 'youtube#searchResult',
    'etag': 'trAA2O5oCHACtM9xBBHMvMBqIjw',
    'id': {
        'kind': 'youtube#video',
        'videoId': '16vwkbT18NM'
    },
    'snippet': {
        'publishedAt': '2024-04-05T21:47:55Z',
        'channelId': 'UCnT2lcMeAHiQgWR-g7H5XBA',
        'title': 'Want to Get an Internship At Your Favorite Company? #shorts #career #internship',
        'description': '',
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/16vwkbT18NM/default.jpg',
                'width': 120,
                'height': 90
            },
            'medium': {
                'url': 'https://i.ytimg.com/vi/16vwkbT18NM/mqdefault.jpg',
                'width': 320,
                'height': 180
            },
            'high': {
                'url': 'https://i.ytimg.com/vi/16vwkbT18NM/hqdefault.jpg',
                'width': 480,
                'height': 360
            }
        },
        'channelTitle': 'TUN',
        'liveBroadcastContent': 'none',
        'publishTime': '2024-04-05T21:47:55Z'
    }
}, {
    'kind': 'youtube#searchResult',
    'etag': 'ZoKsUgikQwlvY8deJ7FfyAY5rho',
    'id': {
        'kind': 'youtube#video',
        'videoId': 'pe0u4vk90_E'
    },
    'snippet': {
        'publishedAt': '2024-04-05T19:30:09Z',
        'channelId': 'UCz6XquIbM5OcfK7r3hQQCXA',
        'title': 'I Hired My College Roommate as a Security Guard | Unpaid Intern',
        'description': 'follow me on twitter: https://twitter.com/LudwigAhgren main channel: https://youtube.com/user/MrAndersLa Edited by: ...',
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/pe0u4vk90_E/default.jpg',
                'width': 120,
                'height': 90
            },
            'medium': {
                'url': 'https://i.ytimg.com/vi/pe0u4vk90_E/mqdefault.jpg',
                'width': 320,
                'height': 180
            },
            'high': {
                'url': 'https://i.ytimg.com/vi/pe0u4vk90_E/hqdefault.jpg',
                'width': 480,
                'height': 360
            }
        },
        'channelTitle': 'Ludwin',
        'liveBroadcastContent': 'none',
        'publishTime': '2024-04-05T19:30:09Z'
    }
}, {
    'kind': 'youtube#searchResult',
    'etag': 'N4Op23TMQl9JJ064Ajo-Bkdl5Gc',
    'id': {
        'kind': 'youtube#video',
        'videoId': 'pERGoaOGu7M'
    },
    'snippet': {
        'publishedAt': '2024-04-05T18:50:52Z',
        'channelId': 'UCfB_nNMs_l7xdHVnpHLRYow',
        'title': 'Internships let you EARN while you learn = no college debt!  Contact a Career Consultant today #Jobs',
        'description': '',
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/pERGoaOGu7M/default.jpg',
                'width': 120,
                'height': 90
            },
            'medium': {
                'url': 'https://i.ytimg.com/vi/pERGoaOGu7M/mqdefault.jpg',
                'width': 320,
                'height': 180
            },
            'high': {
                'url': 'https://i.ytimg.com/vi/pERGoaOGu7M/hqdefault.jpg',
                'width': 480,
                'height': 360
            }
        },
        'channelTitle': 'Workforce Connection of Central New Mexico',
        'liveBroadcastContent': 'none',
        'publishTime': '2024-04-05T18:50:52Z'
    }
}, {
    'kind': 'youtube#searchResult',
    'etag': 'FAyT3Dw0vwbpAHVSNSB4H3LIawM',
    'id': {
        'kind': 'youtube#video',
        'videoId': 'QoRVfH9VM1s'
    },
    'snippet': {
        'publishedAt': '2024-04-05T17:36:32Z',
        'channelId': 'UCGoLw0tC_QAXy0b4KCoxYZw',
        'title': 'Zoho off campus internship? #codeio',
        'description': '',
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/QoRVfH9VM1s/default.jpg',
                'width': 120,
                'height': 90
            },
            'medium': {
                'url': 'https://i.ytimg.com/vi/QoRVfH9VM1s/mqdefault.jpg',
                'width': 320,
                'height': 180
            },
            'high': {
                'url': 'https://i.ytimg.com/vi/QoRVfH9VM1s/hqdefault.jpg',
                'width': 480,
                'height': 360
            }
        },
        'channelTitle': 'code io - Tamil',
        'liveBroadcastContent': 'none',
        'publishTime': '2024-04-05T17:36:32Z'
    }
}, {
    'kind': 'youtube#searchResult',
    'etag': 'u7WxLmKOiIipEscFK7JF52owOQA',
    'id': {
        'kind': 'youtube#video',
        'videoId': 'jbsdcp_Q6tw'
    },
    'snippet': {
        'publishedAt': '2024-04-05T17:08:26Z',
        'channelId': 'UCEyaHLYVG0WIAABOLbCb27A',
        'title': 'WHY MOST OF STUDENTS GET DISAPPOINTED WITH INTERNSHIPS? ITS NOT THAT FANCY AS IT LOOKS!',
        'description': 'WHY MOST OF STUDENTS GET DISAPPOINTED WITH INTERNSHIPS? ITS NOT THAT FANCY AS IT LOOKS! #mediamentor ...',
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/jbsdcp_Q6tw/default.jpg',
                'width': 120,
                'height': 90
            },
            'medium': {
                'url': 'https://i.ytimg.com/vi/jbsdcp_Q6tw/mqdefault.jpg',
                'width': 320,
                'height': 180
            },
            'high': {
                'url': 'https://i.ytimg.com/vi/jbsdcp_Q6tw/hqdefault.jpg',
                'width': 480,
                'height': 360
            }
        },
        'channelTitle': 'MEDIA MENTOR',
        'liveBroadcastContent': 'none',
        'publishTime': '2024-04-05T17:08:26Z'
    }
}, {
    'kind': 'youtube#searchResult',
    'etag': 'bsDLdrCruGWUe-1eGKW41I-ekd0',
    'id': {
        'kind': 'youtube#video',
        'videoId': 'rkVMMo8_wx0'
    },
    'snippet': {
        'publishedAt': '2024-04-05T16:00:43Z',
        'channelId': 'UCsmMJdrZJnMQ4G7hPfBwNMQ',
        'title': 'Elemental | Ember Shot Progression | Animation Breakdowns | 3D Animation Internships',
        'description': 'My second run of shots from Elemental - The biggest challenge was choreographing all the actions in a way that read clearly.',
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/rkVMMo8_wx0/default.jpg',
                'width': 120,
                'height': 90
            },
            'medium': {
                'url': 'https://i.ytimg.com/vi/rkVMMo8_wx0/mqdefault.jpg',
                'width': 320,
                'height': 180
            },
            'high': {
                'url': 'https://i.ytimg.com/vi/rkVMMo8_wx0/hqdefault.jpg',
                'width': 480,
                'height': 360
            }
        },
        'channelTitle': '3D Animation Internships',
        'liveBroadcastContent': 'none',
        'publishTime': '2024-04-05T16:00:43Z'
    }
}]
        # url = 'https://www.googleapis.com/youtube/v3/search'
        # params = {
        #     'part': 'snippet',
        #     'q': search_query,
        #     'type': 'video',
        #     'publishedAfter': '2022-05-01T00:00:00Z',
        #     'maxResults': 10,
        #     'order': 'date',
        #     'key': 'AIzaSyBf6otg6w526Ep9mM5XNA_7t9Lx19pD2Jg'  # Replace with your API key
        # }
        # response = requests.get(url, params=params)
        # videos = response.json().get('items', [])
        # print("videos", videos)
        print("chk");
        for video in videos:
        #     video_obj = Video(
        #         title=video['title'],
        #         description=video['description'],
        #         publish_datetime=datetime.now(),
        #         # publish_datetime=datetime.strptime(video['publish_datetime'], '%Y-%m-%dT%H:%M:%SZ'),
        #         thumbnail_urls=[video['thumbnails']]
        #     )
            video_obj = Video(
                title=video['snippet']['title'],
                description=video['snippet']['description'],
                # publish_datetime=video['snippet']['publishedAt'],
                publish_datetime=datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                thumbnail_urls=[video['snippet']['thumbnails']['default']['url']]
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

