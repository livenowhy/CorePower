#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/12/28
"""

from flask import jsonify, Flask, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


from views.trade import trade
from views.authuser import auth_user
app = Flask(__name__)

app.register_blueprint(trade, url_prefix='/api/v1/trade')          # 交易相关
app.register_blueprint(auth_user, url_prefix='/api/v1/authuser')   # 用户相关

CORS(app=app)     # 全局跨域访问

app.config.from_object('config')
db = SQLAlchemy(app=app)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'), echo=True)  # , encoding='utf8', pool_size=30, max_overflow=20)
Session = sessionmaker(bind=engine)


@app.before_request
def before_request():
    print 'before_requestbefore_requestbefore_request'
    g.db_session = Session()


