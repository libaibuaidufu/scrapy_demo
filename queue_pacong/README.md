# queue_pacong
使用队列做一个分布式爬虫
```
# 启动 master
python taskMaster.py
#　启动　url处理  # 可以多线程 进行处理 也可以多开几个窗口
python taskWorker.py
#  进行 保存 #　以时间戳来保存图片　所以　不要同时启动两个　会覆盖的　
python taskWork2.py
```
