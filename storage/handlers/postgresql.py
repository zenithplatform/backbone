__author__ = 'civa'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2

from hubs.auth.model.user import User, Base
from storage.enums import Status
from storage.handlers.base import BaseHandler

class PostgresqlHandler(BaseHandler):
    def insert(self):
        engine = create_engine('sqlite:///sqlalchemy_example.db')
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        session = DBSession()

        # Insert a Person in the person table
        new_person = User(username='new person')
        session.add(new_person)
        session.commit()

class PostgresqlDirectHandler(BaseHandler):
    conn = None
    cur = None

    def create(self, db_name, username, password, app_name):
        try:
            self.conn = psycopg2.connect("dbname={0} user={1} password={2} application_name={3}".format(db_name, username, password, app_name))
        except psycopg2.OperationalError as e:
            raise DbAccessException("Unable to connect", Status.ServerUnavailable)
        else:
            if self.conn:
                self.cur = self.conn.cursor()

    def execute_proc(self, procedure_name, *args):
        self.cur.callproc(procedure_name, *args)
        self.conn.commit()

        return self.cur.fetchone()

    def execute_query(self, query, *args):
        try:
            if args:
                self.cur.execute(query, *args)
            else:
                self.cur.execute(query)

            if query.startswith("SELECT"):
                result = self.cur.fetchall()
                return result

            self.conn.commit()

            return self.cur.rowcount
        except psycopg2.IntegrityError as ex:
            if ex.pgcode == '23505':
                raise DbAccessException("Data already exist.", Status.AlreadyExists)
            else:
                raise DbAccessException("Unknown error.", Status.Unknown)

    def dispose(self):
        self.cur.close()
        self.conn.close()

class DbAccessException(Exception):
    def __init__(self, message, status):
        super(DbAccessException, self).__init__(message)
        self.status = status