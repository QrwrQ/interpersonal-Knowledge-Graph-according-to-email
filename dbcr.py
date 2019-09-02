# -*- coding: utf-8 -*-
import configparser
import os
import pyorient
import os.path	
import re
import extract1

cfig=configparser.ConfigParser()
cfig.read('config.ini')

phone_ops=cfig.options('phone_re')
phone_regular=[]
for phone_op in phone_ops:
    phone_regular.append(cfig.get('phone_re',phone_op))

phone_re_ops=cfig.options('phone_replus')
phone_re_regular=[]
for phone_re_op in phone_re_ops:
    phone_re_regular.append(cfig.get('phone_replus',phone_re_op))


qq_ops=cfig.options('qq_re')
qq_regular=[]
for qq_op in qq_ops:
    qq_regular.append(cfig.get('qq_re',qq_op))
vx_ops=cfig.options('vx_re')
vx_regular=[]
for vx_op in vx_ops:
    vx_regular.append(cfig.get('vx_re',vx_op))

id_ops=cfig.options('id_re')
id_regular=[]
for id_op in id_ops:
    id_regular.append(cfig.get('id_re',id_op))


#phone_regular=[r'1[3,4,5,7,8]\d{9}\s',r'(?<=phone:).+(?=</td)',r'(?<=电话:).+(?=</td)']

def check_v_exist(vtype,name):    #判断节点是否存在
    if len(client.command("select from "+vtype+" where name='"+name+"'"))==0:
        return 0
    else:
        return 1


def check_e_exist(name1,v2type,name2):
    flag=0
    checkedge=client.command("select expand(out()) from (select from "+v2type+"  where name='"+name2+"')")
    for sin in checkedge:
        compare=sin.name
        #print(compare)
        if compare==name1:
            flag=1
    return flag

def check_xe_exist(name1,v2type,name2):
    checkedge=client.command("select expand(out()) from (select from "+v2type+"  where name='"+name2+"')")
    if checkedge[0].name!=name1:
        return 0
    else:
        return 1



def extract_text(content,person_From,person_To):    #对正文内容进行提取
#提取电话号码
    for phone_re in phone_regular:
        phonenum = re.findall(phone_re,content,re.I)
        if len(phonenum)!=0:
            for phonecursory in phonenum:
                #print(phonecursory)
                for phone_p in phone_re_regular:
                    cursory=re.findall(phone_p,phonecursory,re.I)
                    if len(cursory)!=0: 
                        for num in cursory:
                            num=num.strip()
                            #print("电话"+num)
                            if check_v_exist("textinfo",num)==0:
                                client.command("create vertex textinfo set name='"+num+"',type='phonenum',belong='"+person_To+"'")
                                client.command("create edge from(select from textinfo where name='"+num+"')to(select from person where name='"+person_From+"')set name='phone'")
                            else:
                                if check_e_exist(person_From,"textinfo",num)==0:
                                    client.command("create edge from(select from textinfo where name='"+num+"')to(select from person where name='"+person_From+"')set name='phone'")

#提取邮箱
    mail_re=cfig.get('mail','0')
    mailid = re.findall(mail_re,content)
    if len(mailid)!=0:
        for mid in mailid:
           # print(mid)
            if mid!=person_From and mid!=person_To:
                if  check_v_exist("person",mid)==0:
                    client.command("create vertex person set name='"+mid+"'")
                    client.command("create edge from(select from person where name='"+mid+"')to(select from person where name='"+person_From+"')set name='mention'")
                    client.command("create edge from(select from person where name='"+mid+"')to(select from person where name='"+person_To+"')set name='mention'")
                else:
                    if check_e_exist(person_From,"person",mid)==0:
                        client.command("create edge from(select from person where name='"+mid+"')to(select from person where name='"+person_From+"')set name='mention'")
                    if check_e_exist(person_To,"person",mid)==0:
                        client.command("create edge from(select from person where name='"+mid+"')to(select from person where name='"+person_To+"')set name='mention'")
            
#提取qq号
    content_sub=extract1.filter_tags(content)
    #print(content_sub)
    for qq_re in qq_regular:
        qqcursory = re.findall(qq_re,content_sub,re.I)
        if len(qqcursory)!=0:
            for cursory in qqcursory:
                qqnum=re.findall(cfig.get('qq_replus','0'),cursory,re.I)
                if len(qqnum)!=0:
                    for num in qqnum:
                        if len(num)<13:
                            num=num.strip()
                            #print('QQ'+num)
                            if check_v_exist("textinfo",num)==0:
                                client.command("create vertex textinfo set name='"+num+"',belong='"+person_To+"'")
                                client.command("create edge from(select from textinfo where name='"+num+"')to(select from person where name='"+person_From+"')set name='qq'")
                            else:
                                if check_e_exist(person_From,"textinfo",num)==0:
                                    client.command("create edge from(select from textinfo where name='"+num+"')to(select from person where name='"+person_From+"')set name='qq'")

#提取微信号
    content_sub=extract1.filter_tags(content)
    for vx_re in vx_regular:
        vxcursory = re.findall(vx_re,content_sub,re.I)
        if len(vxcursory)!=0:
            for cursory in vxcursory:
               # print("\ncontent"+cursory)
                vxnum=re.findall(cfig.get('vx_replus','0'),cursory,re.I)
                if len(vxnum)!=0:
                    for num in vxnum:
                        if len(num)<20:
                            num=num.strip()
                           # print(vx_re)
                            #print("result微信"+num)
                            if check_v_exist("textinfo",num)==0:
                                client.command("create vertex textinfo set name='"+num+"',belong='"+person_To+"'")
                                client.command("create edge from(select from textinfo where name='"+num+"')to(select from person where name='"+person_From+"')set name='vx'")
                            else:
                                if check_e_exist(person_From,"textinfo",num)==0:
                                    client.command("create edge from(select from textinfo where name='"+num+"')to(select from person where name='"+person_From+"')set name='vx'")

#提取身份证号
    content_sub=extract1.filter_tags(content)
    for id_re in id_regular:
        idnum = re.findall(id_re,content_sub,re.I)
        if len(idnum)!=0:
            for num in idnum:
                num=num.strip()
                if len(num)==15 or len(num)==18:
                    #print("身份证"+num)
                    if check_v_exist("textinfo",num)==0:
                        client.command("create vertex textinfo set name='"+num+"',belong='"+person_To+"'")
                        client.command("create edge from(select from textinfo where name='"+num+"')to(select from person where name='"+person_From+"')set name='id'")
                    else:
                        if check_e_exist(person_From,"textinfo",num)==0:
                            client.command("create edge from(select from textinfo where name='"+num+"')to(select from person where name='"+person_From+"')set name='id'")

#建立个人节点，同时创建相关的昵称节点
def person_n(value,client):
    pn=re.findall(r'.+(?= <)',value[0])      #提取昵称
    pi=re.findall(r'(?<=<).+(?=>)',value[0])  #提取邮箱帐号
    pid=pi[0]                                 #从提取出的list里面得到值
    if len(client.query("select from person where name='"+pid+"'"))==0:   #判断节点是否存在
        client.command("create vertex person set name='"+pid+"'")   
    if pn:
        pname=pn[0]
        if len(client.query("select from property where name='"+pname+"'"))==0:
            client.command("create vertex property set name='"+pname+"'")
            client.command( "create edge from(select from property where name='"+pname+"')to(select from person where name='"+pid+"')set name='昵称'" )
        else:
            checkedge=client.command("select expand(out()) from (select from property where name='"+pname+"')")
            if check_e_exist(pid,"property",pname)==0:        #检查关系是否存在
                client.command( "create edge from(select from property where name='"+pname+"')to(select from person where name='"+pid+"')set name='昵称'" )      #建立关系

    return pid


#根据一封邮件建立节点和关系
def draw_G(f,client):
    content=f.read()
    #提取from,to的用户信息并建立关系
    value = re.findall(r'(?<=To: ).*',content)
    person_To=person_n(value,client)
    value = re.findall(r'(?<=From: ).*',content)
    person_From=person_n(value,client)
    checkedge=client.command("select expand(out()) from (select from person where name='"+person_From+"')")
    if  check_e_exist(person_To,"person",person_From)==0:
        client.command( "create edge from(select from person where name='"+person_From+"')to(select from person where name='"+person_To+"')set name='email'" )
    #maintext=re.findall(r'Text:([\s\S]*?)<main',content)
    #print(maintext)
    #if len(maintext)!=0:
        #for content in maintext:
    extract_text(content,person_From,person_To)

def create_database():
#与orient建立链接
    global client
    client=pyorient.OrientDB(cfig.get('orientdb','adress'),2424)
    session_id=client.connect(cfig.get('orientdb','id'),cfig.get('orientdb','keys'))
    client.db_open(cfig.get('orientdb','database'), cfig.get('orientdb','id'), cfig.get('orientdb','keys') )

#清理数据库数据并建立类
    client.command("delete vertex V")
    client.command("delete edge E")
    client.command( "drop class person" )
    client.command( "drop class property" )
    client.command( "drop class textinfo" )
    client.command( "create class person extends V" )
    client.command( "create class property extends V" )
    client.command( "create class textinfo extends V" )

    rootdir=cfig.get('path','email_save')
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            f=open(rootdir+filename,"r")
            draw_G(f,client)
            f.close()

def add_database():
#与orient建立链接
    global client
    client=pyorient.OrientDB(cfig.get('orientdb','adress'),2424)
    session_id=client.connect(cfig.get('orientdb','id'),cfig.get('orientdb','keys'))
    client.db_open(cfig.get('orientdb','database'), cfig.get('orientdb','id'), cfig.get('orientdb','keys') )

    rootdir=cfig.get('path','email_add_save')
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            f=open(rootdir+filename,"r")
            draw_G(f,client)
            f.close()

#与orient建立链接
if __name__ == "__main__":
    global client
    client=pyorient.OrientDB(cfig.get('orientdb','adress'),2424)
    session_id=client.connect(cfig.get('orientdb','id'),cfig.get('orientdb','keys'))
    client.db_open(cfig.get('orientdb','database'), cfig.get('orientdb','id'), cfig.get('orientdb','keys') )



#与orient建立链接
    client=pyorient.OrientDB(cfig.get('orientdb','adress'),2424)
    session_id=client.connect(cfig.get('orientdb','id'),cfig.get('orientdb','keys'))
    client.db_open(cfig.get('orientdb','database'), cfig.get('orientdb','id'), cfig.get('orientdb','keys') )

#清理数据库数据并建立类
    client.command("delete vertex V")
    client.command("delete edge E")
    client.command( "drop class person" )
    client.command( "drop class property" )
    client.command( "drop class textinfo" )
    client.command( "create class person extends V" )
    client.command( "create class property extends V" )
    client.command( "create class textinfo extends V" )



    rootdir=cfig.get('path','email_save')
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            f=open(rootdir+filename,"r")
            print(filename)
            draw_G(f,client)
            f.close()


