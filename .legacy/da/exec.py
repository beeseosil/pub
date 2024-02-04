from da import *
def exec(port=11115,path="c:/code/da/"):
    os.chdir(path)
    os.system(f"streamlit run app.py --server.port {port}")
try:
    f=getdata(save=True)
except:
    print(f"getdata error")
finally:
    if __name__=="__main__":
        exec()