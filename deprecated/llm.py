import os
from langchain import HuggingFaceHub
from langchain.embeddings import HuggingFaceEmbeddings

# 텟트
experimental:bool=False

# https://huggingface.co/settings/tokens
huggingFaceTokenFile:str="c:/code/huggingFaceToken.key"
with open(huggingFaceTokenFile) as fp:
    HuggingFaceToken=fp.readline()
    os.environ["HUGGINGFACEHUB_API_TOKEN"]=HuggingFaceToken

# 
modelId="google/flan-t5-xl"
model=HuggingFaceHub(repo_id=modelId,model_kwargs={"temperature":0,"max_length":64})

# get query
query:str=input(":::")
response=model(query)
print(response)

if experimental:
    modelEmbeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    responseEmbeddings=embeddings.embed_query(query)