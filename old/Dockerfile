FROM python:3.7

ARG tag
ENV tag=${tag:-blue}

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
COPY hello.py /app/
RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT python /app/hello.py ${tag}
