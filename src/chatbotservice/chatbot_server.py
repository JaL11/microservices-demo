'''

Author: Ming Yeh Oliver Cheung

Copyright (c) 2021 Wise CSE Group 1
'''


import os, logging
import random
import time

import traceback
from meta_engine import MetaEngine
import demo_pb2_grpc
import demo_pb2
from monitor import Monitor
from concurrent import futures

import grpc
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc


class ChatbotService(demo_pb2_grpc.ChatbotServiceServicer):
    """GRPC interface to access chatbot
    """
    def getChatbotMessage(self, request, context):
        """Gets the message from the chatbot
        also monitors time of handling the request

        Returns:
            str: response from chatbot
        """
        monitor.start_request()
        response = demo_pb2.chatbotResponse(message = "", product_ids = [""])
        response.message = chatbot.handle_message(request.message, request.user_id)
        monitor.stop_request()
        return response

    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING)

    def Watch(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.UNIMPLEMENTED)


if __name__ == "__main__":
    """ Starts a chatbot server over grpc at port 9090
    """
    global chatbot
    global monitor

    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename='logs.txt',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        filemode='w', level=logging.DEBUG)
    monitor = Monitor(4)


    chatbot = MetaEngine()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    port = "9090"
    
    service = ChatbotService()
    demo_pb2_grpc.add_ChatbotServiceServicer_to_server(service, server)
    health_pb2_grpc.add_HealthServicer_to_server(service, server)

    logging.info("listening on port: " +port)
    server.add_insecure_port('[::]:'+port)
    server.start()

    try:
         while True:
            time.sleep(10000)
    except KeyboardInterrupt:
            server.stop(0)
