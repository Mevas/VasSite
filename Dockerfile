FROM joyzoursky/python-chromedriver:3.7-selenium

# File Author / Maintainer
MAINTAINER Mevas

#add project files to the usr/src/app folder
ADD . /usr/src/app

#set directoty where CMD will execute
WORKDIR /usr/src/app
COPY requirements.txt ./

# Get pip to download and install requirements:
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 8000

# server
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]