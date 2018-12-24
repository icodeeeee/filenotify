#!/usr/bin/python
# coding:utf-8
import pyinotify

class NotifyEvent(pyinotify.ProcessEvent):
    def process_IN_ACCESS(self,event):
        #文件被访问==>侦听不到文件夹访问
        print("文件被访问")
    def process_IN_MOVED_TO(self,event):
        #有文件移动过来
        print("有文件移动过来")
    def process_IN_CREATE(self,event):
        #创建文件夹
        print("创建文件夹")
    def process_MOVED_FROM(self,event):
        #文件被移走
        print("文件被移走")
    def process_IN_DELETE(self,event):
        #文件被删除
        print("文件被删除")


def start(path):
    watch_manager=pyinotify.WatchManager()
    watch_manager.add_watch(path,pyinotify.ALL_EVENTS,rec=True)
    notify_event=NotifyEvent()
    notify = pyinotify.Notifier(watch_manager,notify_event)
    notify.loop()
if __name__=="__main__":
    print("start notify")
    path="/home/hyd/testnotify"
    start(path)
