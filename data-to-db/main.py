import json
from model import connect_to_db, Post, Image
import random
import datetime

Session = connect_to_db()


def add_post(record, session_):
    post = Post(
        user_id=1,
        title=record['title'],
        address=record['address'],
        bedroom=record['bedroom'],
        toilet=record['toilet'],
        investor=record['investor'],
        acreage=record['acreage'],
        price=record['price'],
        latitude=record['lat'],
        longitude=record['long'],
        sold=bool(random.getrandbits(1)),
        time_upload=datetime.datetime.now(),
        time_priority=datetime.datetime.now(),
        distance=record['distance'],
        description=record['description']
    )
    session_.add(post)
    session_.flush()
    
    post_id = post.post_id
    session_.commit()

    for image_ in record['images']:
        image = Image(
            post_id=post_id,
            image_url=image_
        )
        session_.add(image)

    session_.commit()


if __name__ == '__main__':
    session = Session()
    with open('data-to-db.json') as js_file:
        data = json.load(js_file)

    for i, record in enumerate(data):
        add_post(record, session)
        print(f'done: {i}')

