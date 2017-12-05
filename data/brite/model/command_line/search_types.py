import os
import argparse
import json

from sqlalchemy import create_engine

from brite.model.service import DbService

def search_types_main():
    parser = argparse.ArgumentParser(description="Search the existing types")
    parser.add_argument('db_path', help='The path to sqlite db')
    args = parser.parse_args()
    if not os.path.exists(args.db_path):
        print("'%s' was not found" % args.db_path)
        return
    search_types(args.db_path)

def search_types(db_path):
    engine = create_engine('sqlite:///%s' % db_path, echo=False)
    service = DbService(engine)
    all_types = service.get_types()
    print('found %s types' % len(all_types))
    for risk_type in all_types:
        print('--------------------')
        print(json.dumps(risk_type, indent=2))

if __name__ == '__main__':
    search_types_main()
