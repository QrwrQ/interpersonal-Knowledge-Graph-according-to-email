import dbcr
import eml
import feml
import search

def get_from_mailbox():
    eml.get_from_mailbox()

def get_from_file():
    feml.get_from_file()

def create_database():
    dbcr.create_database()

def add_database():
    feml.get_from_addfile()
    dbcr.add_database()

def search_info(search_id):
    nodes=search.search(search_id)
    return nodes
def search_node(search_id):
    nodes= search.search_one(search_id)
    return nodes

def search_all():
    nodes=search.all_node()
    return nodes

def search_fuzzy(search_id):
    nodes = search.fuzzy_search(search_id)
    return nodes

if __name__ == "__main__":
    add_database()
    #get_from_file()
    #nodes=search_all()
    #for node in nodes:
    #    print(node.name+node.rid)
   # create_database()
