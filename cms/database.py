from datetime import datetime
import os
from sqlite3 import dbapi2 as sqlite

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists

DATABASE_NAME = 'database.sqlite3'

class Database(object):
    def __init__(self, database_dir='./output'):
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)

        path = os.path.join(database_dir, DATABASE_NAME)

        self.engine = sqlalchemy.create_engine('sqlite:///'+path, module=sqlite, echo=False)
        self.Sessionmaker = sessionmaker(bind=self.engine)

        Base = declarative_base()
        class PostORM(Base):
            __tablename__ = 'posts'
            __table_args__ = {'sqlite_autoincrement': True}

            id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
            name = sqlalchemy.Column(sqlalchemy.String)
            password = sqlalchemy.Column(sqlalchemy.String)
            title = sqlalchemy.Column(sqlalchemy.String)
            author = sqlalchemy.Column(sqlalchemy.String)
            url = sqlalchemy.Column(sqlalchemy.String)
            shortlink = sqlalchemy.Column(sqlalchemy.String)
            subreddit = sqlalchemy.Column(sqlalchemy.String)
            folder = sqlalchemy.Column(sqlalchemy.String)
            num_files = sqlalchemy.Column(sqlalchemy.String)
            date_added = sqlalchemy.Column(DATETIME)

            def __init__(self, title, author, url, shortlink, subreddit, num_files, folder):
                self.title = title
                self.author = author
                self.url = url
                self.shortlink = shortlink
                self.subreddit = subreddit
                self.folder = folder
                self.num_files = num_files
                self.date_added = datetime.now()

        self.PostORM = PostORM

        self.Base = Base
        if not self.engine.dialect.has_table(self.engine, PostORM.__tablename__):
            self.Base.metadata.create_all(self.engine)
        self.session = self.Sessionmaker()

    def add_post(self, post, files, path):
        self.session.add(
        self.PostORM(post.title,
                post.author,
                post.url,
                post.shortlink,
                post.subreddit,
                files,
                path)
        )
        self.session.commit()

    def exists(self, post):
        return self.session.query(exists().where(self.PostORM.author==post.author)
                .where(self.PostORM.title==post.title)
                .where(self.PostORM.subreddit==post.subreddit)).scalar()
