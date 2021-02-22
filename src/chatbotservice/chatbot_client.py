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

def request(text):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.ChatbotServiceStub(channel)
        response = stub.getChatbotMessage(demo_pb2.chatbotRequest(message=text, user_id = "2cent"))
    return response

def get_rec(id, products = ["test"]):
    """Gets recommendation from the microservice 
    recommendation

    Args:
        id (str): Id of user
        products (list, optional): [description]. Defaults to ["test"].

    Returns:
        list: list of recommended producsts from user
    """
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = demo_pb2_grpc.RecommendationServiceStub(channel)
        request = demo_pb2.ListRecommendationsRequest(user_id=id, product_ids=products)
        response = stub.ListRecommendations(request)
    
    return response

if __name__ == "__main__":
    """used only for quick local testing
    """
    request("HI")
    print(request("Hi"))