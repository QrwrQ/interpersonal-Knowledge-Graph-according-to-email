import configparser
import os
import pyorient
import os.path
import re

cfig=configparser.ConfigParser()
cfig.read('config.ini')
class snode:
    def __init__(self):
        self.name=""
        self.rid=""

def search(search_id):
    #search_id = input("请输入你想查询内容：")
    finall=[]
    client=pyorient.OrientDB(cfig.get('orientdb','adress'),2424)
    session_id=client.connect(cfig.get('orientdb','id'),cfig.get('orientdb','keys'))
    client.db_open(cfig.get('orientdb','database'), cfig.get('orientdb','id'), cfig.get('orientdb','keys') )

    nodes=client.command("select expand(in()) from (select from person where name='"+search_id+"')")
    if len(nodes)!=0:
        for node in nodes:
            res=snode()
            res.name=node.name
            res.rid=node._rid
            finall.append(res)

    nodes=client.command("select from person where belong='"+search_id+"'")
    if len(nodes)!=0:
        for node in nodes:
            res=snode()
            res.name=node.name
            res.rid=node._rid
            finall.append(res)
    return finall


def search_one(search_id):
    #search_id = input("请输入你想查询内容：")
    client=pyorient.OrientDB(cfig.get('orientdb','adress'),2424)
    session_id=client.connect(cfig.get('orientdb','id'),cfig.get('orientdb','keys'))
    client.db_open(cfig.get('orientdb','database'), cfig.get('orientdb','id'), cfig.get('orientdb','keys') )

    nodes=client.command("select from V where name='"+search_id+"'")
    finall=[]
    if len(nodes)!=0:
        for node in nodes:
            res=snode()
            res.name=node.name
            res.rid=node._rid
            finall.append(res)
    return finall


def fuzzy_search(search_id):
    #search_id = input("请输入你想查询的id：")
    client=pyorient.OrientDB(cfig.get('orientdb','adress'),2424)
    session_id=client.connect(cfig.get('orientdb','id'),cfig.get('orientdb','keys'))
    client.db_open(cfig.get('orientdb','database'), cfig.get('orientdb','id'), cfig.get('orientdb','keys') )

    nodes=client.command("select from V where name like '"+search_id+"%'")
    finall=[]
    if len(nodes)!=0:
        for node in nodes:
            res=snode()
            res.name=node.name
            res.rid=node._rid
            finall.append(res)
    return finall



def all_node():
    client=pyorient.OrientDB(cfig.get('orientdb','adress'),2424)
    session_id=client.connect(cfig.get('orientdb','id'),cfig.get('orientdb','keys'))
    client.db_open(cfig.get('orientdb','database'), cfig.get('orientdb','id'), cfig.get('orientdb','keys') )

    nodes=client.command("select from V")
    finall=[]
    if len(nodes)!=0:
        for node in nodes:
            res=snode()
            res.name=node.name
            res.rid=node._rid
            finall.append(res)
    return finall

'''
if __name__ == "__main__":

    while True:
        print("1.显示所有节点\n2.模糊查询\n3.查询一个节点的信息")
        op = input("选择：")
        if op=='1':
            all_node()
        if op=='2':
            fuzzy_search()
        if op=='3':
            search()
        if op=='q':
            break

'''
