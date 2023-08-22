from models import db, User, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

alan = User(first_name="Alan", last_name="Alda", image_url="https://i1.wp.com/cornellsun.com/wp-content/uploads/2016/04/Pg-1-Alda-Mug.jpg?w=647&ssl=1")
joel = User(first_name="Joel", last_name="Burton", image_url="https://pbs.twimg.com/profile_images/1217917608/IMG_3419_400x400.jpg")
jane = User(first_name="Jane", last_name="Smith", image_url="https://assets.mycast.io/characters/jane-smith-2096505-normal.jpg?1618937696")

db.session.add_all([alan,joel,jane])
db.session.commit()

post1 = Post(title="test1", content="tester", user_id=1)
post2 = Post(title="test2", content="tester", user_id=1)
post3 = Post(title="test3", content="tester", user_id=2)
post4 = Post(title="test4", content="tester", user_id=2)
post5 = Post(title="test5", content="tester", user_id=3)
post6 = Post(title="test6", content="tester", user_id=3)

db.session.add_all([post1,post2,post3,post4,post5,post6])
db.session.commit()