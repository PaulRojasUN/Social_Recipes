FROM python:3

COPY ./app /home/socialrecipes/
COPY ./requirements.txt /home/socialrecipes/
COPY ./scripts /

RUN pip install -r /home/socialrecipes/requirements.txt
