# Get-Key-Papers-From-Web-about-spinning-up
Get Key Papers From Web about spinning up with python

**有帮助的话，欢迎点个star~**

原文链接：
https://spinningup.openai.com/en/latest/spinningup/keypapers.html

上面是openai之前总结分类的经典文章；
TXT文件是网友提供的整理链接；

我这个脚本实现的是根据文本内容，自己解析，下载，创建文件夹，保存到本地。

节省大家自己手动创建和下载分类的时间

一共105篇论文，基本上可以成功下载九十篇paper。
大部分是arxiv上的文章，小部分是直接下载的，以及部分其他会议的文章（这个目前不好直接下）
如果中间不断的话，差不多得三个小时能下完（看网速）

基本上不需要安装任何其他的依赖包，直接在Python中run KeyPapers.py就行了
终端进入当前目录，执行下面语句：
```
python KeyPapers.py
```


