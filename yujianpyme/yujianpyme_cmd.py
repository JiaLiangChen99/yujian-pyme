#coding=utf-8
import sys
import os
from   os.path import abspath, dirname
sys.path.insert(0,abspath(dirname(__file__)))
import tkinter
from   tkinter import *
import Fun
ElementBGArray={}  
ElementBGArray_Resize={} 
ElementBGArray_IM={} 

from concurrent.futures import ThreadPoolExecutor
import threading
import requests
lock = threading.Lock()
def sent_request(task_id, url, code_dict, uiName, time_out):
    code = requests.get(url, timeout=time_out).status_code
    Fun.SetText(uiName,"Label_14",f"扫描信息:{url}")
    if code == 200:
        if code_dict['is_200code']:
            Fun.AddRowText(uiName, "ListView_1", rowIndex='end', values=(task_id, url, code))
    elif str(code).startswith('3'):
        if code_dict['is_3xxcode']:
            Fun.AddRowText(uiName, "ListView_1", rowIndex='end', values=(task_id, url, code))
    elif code == 403:
        if code_dict['is_403code']:
            Fun.AddRowText(uiName, "ListView_1", rowIndex='end', values=(task_id, url, code))
    lock.acquire()
    value = Fun.GetCurrentValue(uiName,"Progress_1")
    Fun.SetCurrentValue(uiName,"Progress_1",value+1)
    lock.release()
def get_task_info(all_scan, code_dict, uiName, thread_num=1, time_out=1):
    import  time
    time1 = time.time()
    with ThreadPoolExecutor(max_workers=int(thread_num)) as executor:
        futures = [executor.submit(sent_request, task_id, url, code_dict, uiName, time_out) for task_id, url in
  enumerate(all_scan)]
    Fun.SetElementEnable(uiName,"Button_4",False)
    Fun.SetElementEnable(uiName,"Button_3",True)
    Fun.SetText(uiName,"Label_14",f"扫描信息:扫描完成")
    value = Fun.GetCurrentValue(uiName,"Progress_1")
    time2 = time.time()
    print(time2-time1)
def create_task_thread(all_scan,code_dict,uiname,thread_num=1, time_out=1):
    run_thread = threading.Thread(target=get_task_info, args=[all_scan,code_dict,uiname,thread_num,time_out])
    run_thread.Daemon = True
    run_thread.start()
def setting_task_scan(uiName, text):
    scan_type_dict = {'is_dir':'配置/DIR.txt', 'is_asp':'配置/ASP.txt',
     'is_mdb':'配置/MDB.txt', 'is_php':'配置/PHP.txt', 'is_jsp':'配置/JSP.txt', 'is_aspx':'配置/ASPX.txt',}
    all_scan = []
    for key in scan_type_dict.keys():
        value = Fun.GetCurrentValue(uiName,key)
        if value:
            with open(scan_type_dict[key],'r+',encoding='gbk') as f:
                contents = f.read()
                lines = contents.split('\n')
                lines.remove('')
                all_scan.extend(lines)
    all_scan = [text+i for i in all_scan]
    return all_scan
def setting_task_code(uiName):
    task_code_dict = {}
    for code in ["is_200code","is_3xxcode","is_403code"]:
        task_code_dict[code] = Fun.GetCurrentValue(uiName,code)
    return task_code_dict
def Form_1_onLoad(uiName):
    # 初始化线程数的选择
    for i in range(100):
        Fun.AddItemText(uiName,"ComboBox_3",i+1,"end")
    Fun.SetCurrentValue(uiName,"ComboBox_3",1)
    # 初始化超时时间的选择
    for i in range(30):
        Fun.AddItemText(uiName,"ComboBox_4",i+1,"end")
    Fun.SetCurrentValue(uiName,"ComboBox_4",1)
#Button '开始扫描's Event :Command
def Button_3_onCommand(uiName,widgetName):
    Fun.SetCurrentValue(uiName,"Progress_1",0)
    Fun.SetEnable(uiName,"Button_3",False)
    Fun.SetEnable(uiName,"Button_4",True)
    # 获取线程数，超时时间，扫描目录，选择的状态码
    thread_num = int(Fun.GetCurrentValue(uiName,"ComboBox_3"))
    time_out = int(Fun.GetCurrentValue(uiName,"ComboBox_4"))
    # 获取域名
    text = Fun.GetText(uiName,"Entry_2")
    if text.endswith('/'):
        text = text[:-1]
    task_scan = setting_task_scan(uiName, text)
    task_code_dict = setting_task_code(uiName)
    Fun.SetProgress(uiName,"Progress_1",len(task_scan),0)
    create_task_thread(all_scan=task_scan,code_dict=task_code_dict,thread_num=thread_num,time_out=time_out,uiname=uiName)
    

    
#CheckButton 'DIR's Event :Command
def is_dir_onCommand(uiName,widgetName):
    pass













