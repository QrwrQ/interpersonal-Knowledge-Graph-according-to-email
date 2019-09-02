import KBemail as K

def test():
    K.get_from_file()
    print("获取邮件成功！")
    K.create_database()
    print("建立数据库成功！")
    nodes=K.search_all()
    for node in nodes:
        if node.name=="542391873":
            print("test1  pass")
            break
    for node in nodes:
        if node.name=="542391873":
            print("test2  pass")
            break
    for node in nodes:
        if node.name=="31231212":
            print("test3  pass")
            break
    for node in nodes:
        if node.name=="312312129":
            print("test4  pass")
            break
    for node in nodes:
        if node.name=="8720184374":
            print("test5  pass")
            break
    for node in nodes:
        if node.name=="933567211":
            print("test6  pass")
            break
    for node in nodes:
        if node.name=="927635521":
            print("test7  pass")
            break
    for node in nodes:
        if node.name=="9467352809":
            print("test8  pass")
            break
    for node in nodes:
        if node.name=="12198372001":
            print("test9  pass")
            break
    for node in nodes:
        if node.name=="qwq-asda12asdapppq":
            print("test10 pass")
            break
    for node in nodes:
        if node.name=="qpqmdas":
            print("test11 pass")
            break
    for node in nodes:
        if node.name=="Pfweepp":
            print("test12 pass")
            break
    for node in nodes:
        if node.name=="PPPwdwd12":
            print("test13 pass")
            break
    for node in nodes:
        if node.name=="pasqp-121":
            print("test14 pass")
            break
    for node in nodes:
        if node.name=="alal-qiq12":
            print("test15 pass")
            break

    for node in nodes:
        if node.name=="P1219asd":
            print("test16 pass")
            break
    for node in nodes:
        if node.name=="13954616860":
            print("test17 pass")
            break
    for node in nodes:
        if node.name=="17323476549":
            print("test18 pass")
            break
    for node in nodes:
        if node.name=="（0546）1231-122":
            print("test19 pass")
            break
    for node in nodes:
        if node.name=="511823198401103576":
            print("test20 pass")
            break
    for node in nodes:
        if node.name=="511823198401103218":
            print("test21 pass")
            break
    for node in nodes:
        if node.name=="511823198401108334":
            print("test22 pass")
            break
    for node in nodes:
        if node.name=="511823198401109871":
            print("test23 pass")
            break
    for node in nodes:
        if node.name=="511823198401109150":
            print("test24 pass")
            break
    for node in nodes:
        if node.name=="qowda@qq.com":
            print("test25 pass")
            break
    for node in nodes:
        if node.name=="qwqasas@163.com":
            print("test26 pass")
            break
    all=0
    for node in nodes:
        all=all+1
    acc=26*100/(all-8)
    print("命中率："+str(acc)+"%")

if __name__ == "__main__":
    test()

    
