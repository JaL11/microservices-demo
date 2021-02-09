'''

Author: Ming Yeh Oliver Cheung

Copyright (c) 2021 Wise CSE Group 1
'''

import os
import random
import time
import traceback
import demo_pb2_grpc
import demo_pb2
from concurrent import futures

import grpc


import demo_pb2
import demo_pb2_grpc

def run(text):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.ChatbotServiceStub(channel)
        response = stub.getChatbotMessage(demo_pb2.chatbotRequest(message=text, user_id = "2cent"))
    print("Chatbot received: " + response.message)


if __name__ == '__main__':
    run("What can you recommend me")