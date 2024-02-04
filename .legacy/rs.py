import cv2 as cv
import numpy as np
import win32gui,win32ui,win32con
import os
import time
import pytesseract
from pytesseract import Output

def cap_(size=(600,30)):
    w,h=size
    bmpfilename="out.bmp"
    # hwnd=win32gui.FindWindow(None,windowname)
    hwnd=None

    wDC=win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap=win32ui.CreateBitmap()

    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    # basis, end, obj, offset, ?
    cDC.BitBlt((0,0), (w,h), dcObj, (110,75), win32con.SRCCOPY)

    # img mat to bmpfile
    dataBitMap.SaveBitmapFile(cDC, bmpfilename)

    # img mat
    arr=dataBitMap.GetBitmapBits(True)
    img=np.frombuffer(arr,dtype="uint8")
    img.shape=(h,w,4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return img

def print_(stat,txt="",et=None):
    if stat==0:print(txt,f"({et})","DONE")
    elif stat==1:print(txt,f"({et})","DUPE")
    elif stat==2:print(txt,"FAIL")
    else:print(f"unspecified error")

taskids=[]

while True:

    try:
        img=cap_()
        results=pytesseract.image_to_data(img,output_type=Output.DICT)
        taskurl=max(results["text"],key=len)
        taskid="".join([q for q in taskurl[taskurl.index("s=")+2:] if q.isdigit()])
    except:
        time.sleep(10)
        continue
    
    if len(taskid)!=10:
        stat=2
        elapsedTime=0
    else:
        stat=0
        if len(taskids)==0:
            t0=time.time()
            elapsedTime=0
            taskids.append([taskid,0])
        elif len(taskids)==1:
            t1=time.time()
            elapsedTime=round((time.time()-t0)/60,1)
            taskids.append([taskid,elapsedTime])
        elif len(taskids)>1:
            if taskids[-1][0]!=taskid:
                elapsedTime=round(doneTime/6,2)
                taskids.append([taskid,elapsedTime])
            else:
                stat=1
                elapsedTime=0
        doneTime+=1

    print_(stat,taskid,elapsedTime)
    time.sleep(10)