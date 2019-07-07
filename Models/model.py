from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@127.0.0.1/bilibili'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class VideoInfo(db.Model):
    __tablename__='video'
    id = db.Column(db.Integer, primary_key=True)

    cid = db.Column(db.String(20))
    ep_id = db.Column(db.String(20))
    titleFormat = db.Column(db.PickleType)
    longTitle = db.Column(db.PickleType)
    split_num = db.Column(db.Integer)
    urls = db.relationship('VideoUrl', back_populates='v_cid')


class VideoUrl(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    v_id = db.Column(db.Integer, db.ForeignKey('video.id')) 
    v_cid = db.relationship('VideoInfo',back_populates='urls')


if __name__ == "__main__":
    db.drop_all()
    db.create_all()

    with open('_vinfo_刺客.json','r') as f:
        # content = f.read()
        for line in f.readlines():
            d = json.loads(line)
            # print(d['cid'])
            split_num = len(d['v_split_list'])
            vi = VideoInfo(cid=d['cid'],ep_id=d['ep_id'],titleFormat=d['titleFormat'],longTitle=d['longTitle'],split_num=split_num)
            db.session.add(vi)
            for i in range(split_num):
                vu = VideoUrl(url=d['v_split_list'][i])
                vi.urls.append(vu)
                db.session.add(vu)
            # vu = VideoUrl(url=d[])
    db.session.commit()

    
    # d = json.loads(content)
 
    # a = VideoInfo(cid='')