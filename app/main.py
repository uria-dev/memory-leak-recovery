from anyio import sleep
from fastapi import FastAPI
from pydantic import BaseModel
from psutil import Process, virtual_memory
from .collectors import MemoryCollector


app = FastAPI()



@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/leak")
async def memory_leak():
    mem_leak_list = []
    interval = 0.5
    memcollector = MemoryCollector()
    while True:
        memcollector.collect_memory_metric()
        mem_leak_list.append(' ' * 10**7)  # Append 1MB of spaces repeatedly
        await sleep(interval)

        
    
    