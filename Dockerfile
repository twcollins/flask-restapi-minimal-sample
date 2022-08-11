FROM python:3.9-alpine
RUN addgroup -g 1000 pyuser && \
    adduser -D -u 1000 -G pyuser pyuser
WORKDIR /app
#COPY * .
COPY requirements.txt ./requirements.txt
COPY api_server.py ./api_server.py
COPY __init__.py ./__init__.py
RUN pip3 install --upgrade setuptools pip && \
    pip3 install -r ./requirements.txt
RUN chmod +x ./api_server.py
RUN chown -R pyuser:pyuser ./*
EXPOSE 5000
USER pyuser
ENTRYPOINT python3 ./api_server.py