# #根据邮件信息建立社交网络



### 环境

linux系统（我是在ubuntu16.04）

java

python3

orientdb2



### 使用说明

在所有开始所有工作之前要开起orientdb服务，在我的os上可以执行以下命令，如果是自己的电脑请先下载orientdb2

```
/opt/orientdb/orientdb-community-2.2.37/bin/server.sh
```



#### 从邮箱中获取邮件

在config,ini中修改email_id,email_key,email_server为想要获取的邮箱的配置

更改完成后在email-kb文件夹下输入以下命令

```
python eml.py
```

抽取出来的邮件被放在efile文件夹中，附件放在attachment文件夹下

#### 从下载下来的.eml获取邮件信息

把.eml文件放在emlfile文件夹下

在email-kb文件下执行

```
python feml.py
```

#### 根据邮件信息建立数据库

启动orientdb服务

在orientdb中建立自己数据库

在config,ini文件中更改id,keys,database为自己的数据库

在email-kb文件夹下执行

```
python dbcr.py
```

#### 搜索功能

以上配置都完成后在email-kb文件下执行

```
python search.py
```

根据其中的提示完成查询功能

#### 可供调用的函数

如果调用这些功能可以把项目中所有文件复制到你的文件夹下然后

```
import KBemail
```

可供调用的功能

```
get_from_mailbox    #从邮箱中获取邮件，不过邮箱名密码等设置要在config.ini中配好
get_from_file        #从下载好的eml格式邮件中获取邮件信息
create_database      #建立数据库
add_database        #往数据库中添加内容
search_info（”你要搜索的用户名“）         #查询节点所有信息
search_node（“你要查询的用户名”）        #检查是否有你要查询的用户名
search_all                      #显示所有用户
search_fuzzy（“你要搜索的内容”）        #进行模糊查询
```

根据一两封邮件建立的人际关系网

![](/home/roosi/ren/email-kb/人际关系网.png)

#### 注意事项

尽量使用正常的邮件，如若使用一些特殊格式的邮件系统可能会产生报错