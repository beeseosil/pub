import datetime
import sqlite3
import pandas as pd

# 변수 모음
datetimeFormat="%y%m%d%H%M%S"
dbPath="c:/code/db.db"

# 클래스 모음
class db:
    def __init__(self,path): # 기본 정보
        self.datetime=datetime.datetime.now().strftime(datetimeFormat)
        self.path=path
        self.data=None
        self.note=None
        return None
    def __repr__(self): # 정보 레퍼
        __repr=f"{self.path} at {self.datetime}, "
        if self.data is None:
            __repr+="data: none"
        else:
            __repr+=f"data: {self.dataname} of {self.data.shape}"
        return __repr
    def init(self): # 디비 커넥션, 커셔 열기
        self.connection=sqlite3.connect(self.path)
        self.cursor=self.connection.cursor()
        __repr=f"cursor opened: {self.path} at {self.datetime}"
        print(__repr)
        return None
    def close(self): # 디비 커넥션 닫기
        self.connection.close()
        __repr=f"connection closed: {self.path}"
        print(__repr)
        return None
    def getdata(self,filename): # csv나 xls을 데이터로 로드하기
        if filename.endswith(".csv"):
            __data=pd.read_csv(filename)
        elif filename.endswith((".xlsx",".xls")):
            __data=pd.read_excel(filename)
        else:
            raise TypeError(f"unsupported filetype: {filename}")
        self.dataname=filename
        self.data=__data
        __repr=f"loaded: {filename} of {self.data.shape}"
        print(__repr)
        return None
    def save(self,tablename=None): # 로드된 데이터로 디비에 테이블 쓰기
        if self.data is None:
            raise IOError(f"data is none")
        if tablename is None:
            tablename=input("tablename: ")
            if tablename is None:
                __repr="did nothing"
                print(__repr)
                return None
        self.data.to_sql(tablename,con=self.connection)
        __repr=f"table initialised: {self.dataname} -> {self.path}:{tablename}"
        print(__repr)
        return None
    def todf(self,query): # db 내 테이블을 pd.DataFrame으로 내기
        return pd.read_sql(query,con=self.connection)
    def queryExec(self,query): # 커셔 쿼리 실행 랩어
        dt=datetime.datetime.now().strftime(datetimeFormat)
        try:
            return 0,dt,query,self.cursor.execute(query)
        except Exception as error:
            return 1,dt,query,error
    def queryNote(self,queryResults=None): # 쿼리 실행 랩어 결과 노트
        if queryResults is None:
            if self.note is None:
                __repr="note: none"
                print(__repr)
                return None
            else:
                print(self.note)
                return None
        else:
            if self.note is None:
                self.note={0:[],1:[]}
            if queryResults[0]==0:
                self.note[0].append([0,queryResults[1],queryResults[2],None])
            elif queryResults[0]==1:
                self.note[1].append([1,queryResults[1],queryResults[2],queryResults[3].args[0]])
            return None
    def query(self): # 쿼리 랩어
        maniWords=("insert","update","delete","replac")
        while True:
            query=input(f"query: ")
            if not query:
                continue
            elif query in ("exit","quit"):
                break
            elif query=="note":
                self.queryNote()
                query=None
                continue
            elif query=="commit":
                self.connection.commit()
                continue
            queryType=0 if not query[:6] in maniWords else 1
            queryResults=self.queryExec(query)
            self.queryNote(queryResults)
            if queryResults[0]==0:
                result=queryResults[3].fetchall()
                for row in result:
                    print(row)
                print(f"{len(result) if not queryType else self.cursor.rowcount}","rows")
            elif queryResults[0]==1:
                print("error: ",queryResults[3])
            query=None
        return self.connection.rollback()

# 명령 모음
q=db(dbPath)
q.init()
q.query()