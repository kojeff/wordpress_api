import os, json, sqlalchemy as db
from flask import Flask, request
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

app = Flask(__name__)

host = os.environ.get('api_host')
port = os.environ.get('api_port')
conn = "mysql://" + os.environ.get('dbconn')

if host is None:
  host = "127.0.0.1"
if port is None:
  port = 5000

class Post(Base):
    __tablename__ = 'wp_posts'
    ID = Column(Integer, primary_key=True)
    post_author = Column(Integer)
    post_date = Column(DateTime)
    post_date_gmt = Column(DateTime)
    post_content = Column(Text)
    post_title = Column(String)
    post_excerpt = Column(String)
    post_status = Column(String)
    comment_status = Column(String)
    ping_status = Column(String)
    post_password = Column(String)
    post_name = Column(String)
    to_ping = Column(Text)
    pinged = Column(Text)
    post_modified = Column(DateTime)
    post_modified_gmt = Column(DateTime)
    post_content_filtered = Column(Text)
    post_parent = Column(Integer)
    guid = Column(String)
    menu_order = Column(Integer)
    post_type = Column(String)
    post_mime_type = Column(String)
    comment_count = Column(Integer)

    def serialize(self):
       return {
           'id'                  : self.ID,
	   'post_author'         : self.post_author,
	   'post_date'		 : self.post_date.isoformat(),
	   'post_content'	 : self.post_content,
	   'post_title' 	 : self.post_title,
	   'post_name'   	 : self.post_name,
	   'post_type'   	 : self.post_type,
	   'post_status'   	 : self.post_status
       }   

engine = db.create_engine(conn)
connection = engine.connect();

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/post')
def post():
  id = request.args.get('id')
  post = session.query(Post).get(id)
  output = json.dumps(post.serialize())
  return output

@app.route('/post_type')
def post_type():
  post_type = request.args.get('type')
  posts = session.query(Post).filter_by(post_type=post_type).all()
  results = []
  for p in posts:
    output = json.dumps(p.serialize())
    results.append(output)
  return json.dumps(results)

@app.route('/post_type_count')
def post_type_count():
  post_type = request.args.get('type')
  r = {}
  count = session.query(Post).filter_by(post_type=post_type).count()
  r['count'] = count;
  return json.dumps(r)

if __name__ == "__main__":
    app.run(host=host,port=port)
