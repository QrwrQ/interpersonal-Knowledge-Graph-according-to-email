from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import configparser
import extract1
import poplib
import email
import os

cfig=configparser.ConfigParser()
cfig.read('config.ini')
email = cfig.get('email','email_id')
password = cfig.get('email','email_key')
pop3_server = cfig.get('email','pop_server')
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
            attach.write(data)
            attach.close()
    return attachments

def part_info(msg):
    content_type = msg.get_content_type()
    if content_type=='text/plain':
        content = msg.get_payload(decode=True)
        charset = guess_charset(msg)
        print("type:"+msg.get_content_type())
        print("charset type:"+charset)
        if charset=="无法读取类型":
            print(msg)
        if charset!='utf-8; format=flowed' and charset!='"utf-8"; format=flowed; delsp=yes':
            content = content.decode(charset,'ignore')
            return("mian Text: "+content+"<main")
        else:
            return("此部分无法读取")
            #print('%sText: %s' % ('  ' * indent, content + '...'))
    if content_type=='text/html':
        content = msg.get_payload(decode=True)
        charset = guess_charset(msg)
        print("type:"+msg.get_content_type())
        print("charset type:"+charset)
        if charset=="无法读取类型":
            print(msg)
        if charset!='utf-8; format=flowed' and charset!='"utf-8"; format=flowed; delsp=yes':
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
        else:
            charset="utf-8"
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
            print('%s%s: %s' % ('  ' * indent, header, value))
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
def get_from_mailbox():

    server = poplib.POP3_SSL(pop3_server, 995)
    server.set_debuglevel(1)
    print(server.getwelcome().decode('utf-8'),'ignore')
    server.user(email)
    server.pass_(password)
    print('Messages: %s. Size: %s' % server.stat())
    resp, mails, octets = server.list()
    print(mails)
    index = len(mails)
    for snum in range(1,index):
        resp, lines, octets = server.retr(snum)
        msg_content = b'\r\n'.join(lines).decode('utf-8','ignore')
        msg = Parser().parsestr(msg_content)
        print_info(msg,snum)
        get_email_content(msg,snum)
    server.quit()


if __name__ == "__main__":

# 连接到POP3服务器:
    server = poplib.POP3_SSL(pop3_server, 995)
# 可以打开或关闭调试信息:
    server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'),'ignore')
# 身份认证:
    server.user(email)
    server.pass_(password)
# stat()返回邮件数量和占用空间:
    print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
    resp, mails, octets = server.list()
# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    print(mails)
# 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    for snum in range(1,index):
        resp, lines, octets = server.retr(snum)
# lines存储了邮件的原始文本的每一行,
# 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8','ignore')
# 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
#    msg = extract1.filter_tags(msg)
#print(msg)
        print_info(msg,snum)
        get_email_content(msg,snum)
# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接:
    server.quit()
