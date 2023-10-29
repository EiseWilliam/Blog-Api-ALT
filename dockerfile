FROM python:3.11.2


WORKDIR /core


COPY ./requirements.txt /core
RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY . /core


RUN python3 run.py