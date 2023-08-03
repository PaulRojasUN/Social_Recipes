FROM debian
# RUN apk update
# RUN apk add python3
# RUN apk add py3-pip

# COPY ./app /home/socialrecipes/
COPY ./requirements.txt /home/socialrecipes/
COPY ./scripts /home/scripts/

#RUN pip3 install -r /home/socialrecipes/requirements.txt