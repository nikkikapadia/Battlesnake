
FROM python:3.6.1
# define the present working directory
WORKDIR /docker-flask-test
# copy the contents into the working dir
ADD . /docker-flask-test
# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt
# define the command to start the container

EXPOSE 8080

CMD ["python","server.py"]
