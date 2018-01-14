#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/12/28
"""

from corepower import app

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models.users import db as usersdb
from models.trade import db as tradedb

migrate = Migrate(app, db=usersdb)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


trade_migrate = Migrate(app, db=tradedb)
trade_manager = Manager(app)
trade_manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    trade_manager.run()

# python db.py db init
# python db.py db migrate
# python db.py db upgrade
