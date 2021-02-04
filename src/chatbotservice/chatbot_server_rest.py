'''

Author: Ming Yeh Oliver Cheung

Copyright (c) 2021 Wise CSE Group 1
'''
#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


from logger import getJSONLogger
chatbot = MetaEngine()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """ set up application before start


    """
    SEP = os.path.sep
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename="logs" + SEP +'loggerfile.log',
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
