将程序包package放到服务器上后：

1.双击run.vbs
  程序即可在服务器上运行，每2个小时更新一次数据。

2.运行run.vbs后即可访问项目网站: localhost/package/train.php(本服务器访问） server_ip/package/train.php（其他主机访问）





程序包内一共有18个文件及文件夹，目录如下：
0. README.txt
1. bs4、html5lib为程序导入包。
2. data为数据存放包
3. Login.py为模拟登陆程序
   Crawler.py为爬取微博程序
4. classfy.py为微博分类程序
   classfication.py为微博分类程序
5. find.php
   lost.php
   train.php
   lost.css
   find.js
   lost.js
   train.js
   以上程序为制作网站代码
6. run.bat 批处理程序
   run.vbs 后台运行批处理程序的程序（双击即可更新数据）
