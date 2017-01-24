
## 火车票查询工具
- 1.使用pip安装相应模块，因为是基于python3写的，因此安装的时候需要`pip3 install -r requirements.txt`
- 2.使用方法如下:
```
Usage:
    tickets [-gdtkz] <from> <to> <date>
Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达
    
例如:python3 tickets.py -d 成都 上海 2017-02-10
     python3 tickets.py 成都 上海 2017-02-10
```
