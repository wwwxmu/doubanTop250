# doubanTop250
豆瓣电影Top250爬虫
目标字段：标题，导演、主演、上映时间等信息，星级，评价人数，经典台词
### 运行步骤：
1. 根据sqlCode的代码创建数据库和数据表
2. 根据实际情况修改连接数据库的参数
```
db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="doubanmovie", charset='utf8')
```
