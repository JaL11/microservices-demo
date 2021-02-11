'''

Author: Ming Yeh Oliver Cheung

Copyright (c) 2021 Wise CSE Group 1
'''

import os, logging
import random
import time
import traceback
import demo_pb2_grpc
import demo_pb2
import uvicorn
from concurrent import futures
from fastapi import FastAPI, HTTPException
from meta_engine import MetaEngine

import grpc


import demo_pb2
import demo_pb2_grpc


chatbot = MetaEngine()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """ set up application before start


    """
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename='loggerfile.log',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        filemode='w', level=logging.DEBUG)
    logging.info("Started Python API Server")


@app.get("/chat/{id}/{text}")
async def chat(id: str, text: str):
    """Gets an appropriate answer from the meta-engine

    Args:
        id (str): User identification
        text (str): message from User

    Returns:
        [dict]: [description]
    """

    return {"intentdetector": chatbot.handle_message(text, id)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
