import os
import csv
import requests
import concurrent.futures
from bs4 import BeautifulSoup as bs

ua={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "\
    "AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/104.0.0.0 Safari/537.36"}

def dn(v):
    # (vidname,vidurl)
    os.system(
        f'ffmpeg -n -loglevel 24 '
        f'-i "{v[1]}" '
        f'-user_agent "{ua["user-agent"]}" ' 
        f'-multiple_requests 0 -reconnect_at_eof 1 ' 
        f'-reconnect_streamed 1 -reconnect_on_network_error 1 ' 
        f'-bsf:a aac_adtstoasc -c copy '
        f'"d:/{v[2]}_{v[0]}.mp4"')

def visit(url,idx):
    url=f"{url}{idx}"
    try:
        w=bs(requests.get(url,headers=ua).text)
        e=requests.get(w.iframe["src"],headers=ua)
        if not e.status_code==200:
            return False,url,f"{e.status_code}"
        e=bs(e.text)
        vidname=e.select("meta")[ 7]["content"]
        vidurl =e.select("meta")[18]["content"]
        dn((vidname,vidurl,idx))
        return True,f"{idx}_{vidname}.mp4"
    except Exception as ng:
        return False,url,ng

def exec(url,mx,mn,max_workers=12):
    oks,ngs=[],[]
    #with with statement shutdown method is not needed
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers) as te:
        #submit future objects
        works={te.submit(visit,url,q):q for q in range(mn,mx,1)}
        #result collection: as_completed
        for work in concurrent.futures.as_completed(works):
            #get index by future
            q=works[work]
            #yielded result from the callable per future
            try:
                rslt=work.result(timeout=2048)
            except TimeoutError as ng:
                #idx+reason
                ngs.append((q,ng))
            else:
                if rslt[0] is True:
                    oks.append(rslt[1])
                    print(f"ok: {q}")
                elif rslt[0] is False:
                    #idx+reason
                    ngs.append((rslt[1],rslt[2]))
                    print(f"ng: {q} ({rslt[2]})")
    with open("d:/rslt.csv","w",encoding="utf-8",newline="") as csvfile:
        csv.writer(csvfile).writerows(ngs)
    print(f"done")
    return oks,ngs

def sanitize(oks=None,path="d:/"):
    q=[q.name for q in os.scandir(path) 
        if q.is_file and q.name.endswith(".mp4") and q.stat().st_size==0]
    print(f"zero-sized files: {len(q)}")
    for filename in q:
        os.remove(path+filename)
    if not oks is None:
        q=list(set([q.name for q in os.scandir(path) 
            if q.is_file and q.name.endswith(".mp4")])-set(oks))
        for filename in q:
            os.remove(path+filename)
        return q