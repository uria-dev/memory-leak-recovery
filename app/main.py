from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()



@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/leak")
async def memory_leak():
    mem_leak_list = []
    while True:
        mem_leak_list.append(' ' * 10**7)  # Append 1MB of spaces repeatedly
        
        
    
    