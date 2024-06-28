FROM tiagosamaha/python-firefox:3.8.12
ENV PYTHONUNBUFFERED 1
# RUN pip install -qq -U pip poetry==1.1.15


# Libs necessarias para conexao com oracle
RUN apt-get update && apt-get install -y libaio1 libaio-dev

RUN mkdir /opt/oracle
RUN cd /opt/oracle && wget https://download.oracle.com/otn_software/linux/instantclient/19800/instantclient-basic-linux.x64-19.8.0.0.0dbru.zip && unzip instantclient-basic-linux.x64-19.8.0.0.0dbru.zip
ENV LD_LIBRARY_PATH "/opt/oracle/instantclient_19_8"
WORKDIR /opt/smartsub_web
RUN mkdir /opt/smartsub_web/static_root
RUN mkdir /opt/smartsub_web/media_root
COPY . .

RUN pip install -r requirements.txt


