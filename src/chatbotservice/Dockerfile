# Pull base image
FROM python:3

# Set environment variables
##ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Get GRPC Health Probe
RUN GRPC_HEALTH_PROBE_VERSION=v0.3.6 && \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64 && \
    chmod +x /bin/grpc_health_probe


# Set work directory
RUN mkdir /chatbotservice
WORKDIR /chatbotservice
#Copy project
COPY . /chatbotservice/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# set listen port
ENV PORT "9090"
EXPOSE 9090

#Start container with "python3 chatbot_server.py"
ENTRYPOINT ["python3", "chatbot_server.py"]
