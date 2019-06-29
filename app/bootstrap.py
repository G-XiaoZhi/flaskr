# coding:utf-8

import os
import sqlite3
from flask import Flask, g


app = Flask(__name__)

DATABASE = os.path.join(app.root_path, 'flaskr.db')


# 初始化配置
cnf = {
    "DATABASE": DATABASE,
    "SECRET_KEY": b'_5#y2L"F4Q8z\n\xec]/',
    "USERNAME": 'admin',
    "PASSWORD": 'default'
}

app.config.from_mapping(cnf)


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(DATABASE)  # 建立数据库连接
        g.sqlite_db.row_factory = sqlite3.Row

    return g.sqlite_db


# close_connection()
@app.teardown_appcontext # 这个装饰器用于实现在请求的最后自动关闭数据库连接的功能
def close_connection(exception): # 关闭数据库连接
    db = getattr(g, 'sqlite_db', None)
    if db is not None:
        db.close()


def register():
    from flaskr.app.views import bp as views_bp
    app.register_blueprint(views_bp)


if __name__ == "__main__":
    init_db()
    register()
    app.run(debug=True)
