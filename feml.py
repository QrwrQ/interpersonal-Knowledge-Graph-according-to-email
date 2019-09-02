from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import os
import configparser
import email

import poplib

cfig=configparser.ConfigParser()
cfig.read('config.ini')

jump=0

def get_email_content(message, snum):
    attachments = []
    for part in message.walk():
        filename = part.get_filename()
        if filename:
            filename = decode_str(filename)
            data = part.get_payload(decode=True)
            attachfile=cfig.get('path','attach_save')
            abs_filename = os.path.join(attachfile, filename)
            efile=cfig.get('path','email_save')
            attach = open(efile+str(snum)+".txt", 'a+')
            attachments.append(filename)
            attach.write("\nattachment:"+filename+"\n")
            attach.close()
            attach=open(abs_filename,"wb")
            #attachments.append(filename)
            attach.write(data)
            attach.close()
           # attach.write(data.decode('utf-8','ignore'))
           # print("type:"+msg.get_content_type())
           # print("partcontent:%s"+data.decode('utf-8','ignore'))
          
    return attachments

def get_addemail_content(message, snum):
    attachments = []
    for part in message.walk():
        filename = part.get_filename()
        if filename:
            filename = decode_str(filename)
            data = part.get_payload(decode=True)
            attachfile=cfig.get('path','attach_save')
            abs_filename = os.path.join(attachfile, filename)
            efile=cfig.get('path','email_add_save')
            attach = open(efile+str(snum)+".txt", 'a+')
            attachments.append(filename)
            attach.write("\nattachment:"+filename+"\n")
            attach.close()
            attach=open(abs_filename,"wb")
            #attachments.append(filename)
            attach.write(data)
            attach.close()
           # attach.write(data.decode('utf-8','ignore'))
           # print("type:"+msg.get_content_type())
           # print("partcontent:%s"+data.decode('utf-8','ignore'))
          
    return attachments


def part_info(msg):
    content_type = msg.get_content_type()
    if content_type=='text/plain' or content_type=='text/html':
        content = msg.get_payload(decode=True)
        charset = guess_charset(msg)
        # print("type:"+msg.get_content_type())
        # print("charset type:"+charset)
        if charset!='utf-8; format=flowed':
            content = content.decode(charset,'ignore')
            return("Text: "+content)
        else:
            return("此部分无法读取") 
            #print('%sText: %s' % ('  ' * indent, content + '...'))
    else:
        return("Attachment: "+content_type)
 



def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg,snum,indent=0):
    if indent == 0:
        efile=cfig.get('path','email_save')
        f=open(efile+str(snum)+".txt","w+")
        fname=msg.get('From')
        fnamw=decode_str(fname)
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            if type(value)==bytes:
                value=value.decode()
            f.write(header+": "+value+"\n")
            #print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
#    if (jump==1):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            part_content=part_info(part)
            f.write(part_content)
            #print('%spart %s' % ('  ' * indent, n))
           # print('%s--------------------' % ('  ' * indent))
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            #print("charset type:"+charset)
            if charset:
                content = content.decode(charset)
                f.write("Text: "+content)
            #print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            f.write(str(indent)+"Attachment: "+content_type)
            #print('%sAttachment: %s' % ('  ' * indent, content_type))
    f.close()

def print_add_info(msg,snum,indent=0):
    if indent == 0:
        efile=cfig.get('path','email_add_save')
        f=open(efile+str(snum)+".txt","w+")
        fname=msg.get('From')
        fnamw=decode_str(fname)
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            if type(value)==bytes:
                value=value.decode()
            f.write(header+": "+value+"\n")
            #print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
#    if (jump==1):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            part_content=part_info(part)
            f.write(part_content)
            #print('%spart %s' % ('  ' * indent, n))
           # print('%s--------------------' % ('  ' * indent))
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            #print("charset type:"+charset)
            if charset:
                content = content.decode(charset)
                f.write("Text: "+content)
            #print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            f.write(str(indent)+"Attachment: "+content_type)
            #print('%sAttachment: %s' % ('  ' * indent, content_type))
    f.close()



def get_from_file():
    rootdir=cfig.get('path','email_get')
    snum=0
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            emlfile=cfig.get('path','email_get')
            f=open(emlfile+filename,"r")
            msg=email.message_from_file(f)   #read the content of .eml file 
            f.close()
            print_info(msg,snum)
            get_email_content(msg,snum)
            snum=snum+1

def get_from_addfile():
    rootdir=cfig.get('path','email_add')
    snum=0
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            emlfile=cfig.get('path','email_add')
            f=open(emlfile+filename,"r")
            msg=email.message_from_file(f)   #read the content of .eml file 
            f.close()
            print_add_info(msg,snum)
            get_addemail_content(msg,snum)
            snum=snum+1

if __name__ == "__main__":
    rootdir=cfig.get('path','email_add')
    snum=0
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            emlfile=cfig.get('path','email_get')
            f=open(emlfile+filename,"r")
            msg=email.message_from_file(f)   #read the content of .eml file 
            f.close()
            print_info(msg,snum)
            get_email_content(msg,snum)
            snum=snum+1
'''
for snum in range(1,index):
    f=open("efile/"+str(snum)+".txt","r")
    file_content=f.read()
    print(file_content)
    f.close()
    f=open("efile/"+str(snum)+".txt","w+")
    file_ext=extract1.filter_tags(file_content)
    f.write(file_ext)
    f.close()
'''
