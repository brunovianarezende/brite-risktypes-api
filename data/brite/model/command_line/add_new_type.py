import os
import argparse
import json

from sqlalchemy import create_engine

from brite.model import Base
from brite.model.service import DbService

def add_new_type_main():
    parser = argparse.ArgumentParser(description="Add a new risk type to the db. The db is created if it doesn't exist")
    parser.add_argument('db_path', help='The path to sqlite db')
    parser.add_argument('json_path', help='The path to the json describing the risk type')
    args = parser.parse_args()
    if not os.path.exists(args.json_path):
        print("'%s' was not found" % args.json_path)
        return
    if not os.path.exists(args.db_path):
        print("there is no db at '%s', one will be created" % args.db_path)
    add_new_type(args.db_path, args.json_path)

def add_new_type(db_path, json_path):
    engine = create_engine('sqlite:///%s' % db_path, echo=False)
    if not os.path.exists(db_path):
        Base.metadata.create_all(engine)
    service = DbService(engine)
    with open(json_path) as f:
        obj = json.load(f)
    service.add_type(obj)

if __name__ == '__main__':
    add_new_type_main()
