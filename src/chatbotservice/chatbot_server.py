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
from meta_engine import MetaEngine
import demo_pb2_grpc
import demo_pb2
from monitor import Monitor
from concurrent import futures

import grpc


import demo_pb2
import demo_pb2_grpc


class ChatbotService(demo_pb2_grpc.ChatbotServiceServicer):
    def getChatbotMessage(self, request, context):
        response = demo_pb2.chatbotResponse(message = "", product_ids = [""])
        response.message = chatbot.handle_message(request.message, request.user_id)
        return response

if __name__ == "__main__":
    global chatbot

    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename='logs.txt',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        filemode='w', level=logging.DEBUG)
    monitor = Monitor(4)

    chatbot = MetaEngine()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    demo_pb2_grpc.add_ChatbotServiceServicer_to_server(ChatbotService(), server)
    port = "50051"
    logging.info("listening on port: " + port)
    server.add_insecure_port('[::]:'+port)
    server.start()

    # keep alive
    try:
         while True:
            time.sleep(10000)
    except KeyboardInterrupt:
            server.stop(0)
