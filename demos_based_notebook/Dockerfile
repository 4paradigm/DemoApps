from jupyter/all-spark-notebook:latest

RUN mkdir -p  /home/jovyan/work/system/
COPY zookeeper-3.4.14.tar.gz /home/jovyan/work/system/
COPY fedb-2.2.0-linux.tar.gz /home/jovyan/work/system/
COPY spark-3.0.0-bin-sparkfe.tgz /home/jovyan/work/system/
COPY fedb-2.2.0-py3-none-any.whl /home/jovyan/work/system/
COPY jdk-8u141-linux-x64.tar.gz /home/jovyan/work/system/

RUN cd /home/jovyan/work/system/ && tar -zxvf jdk-8u141-linux-x64.tar.gz && rm jdk-8u141-linux-x64.tar.gz 
ENV JAVA_HOME /home/jovyan/work/system/jdk1.8.0_141
ENV PATH $JAVA_HOME:$PATH

RUN cd /home/jovyan/work/system && tar -zxvf zookeeper-3.4.14.tar.gz && rm zookeeper-3.4.14.tar.gz  && cd zookeeper-3.4.14 && mv conf/zoo_sample.cfg conf/zoo.cfg
RUN cd /home/jovyan/work/system && tar -zxvf fedb-2.2.0-linux.tar.gz && rm fedb-2.2.0-linux.tar.gz
RUN cd /home/jovyan/work/system && tar -zxvf spark-3.0.0-bin-sparkfe.tgz && rm spark-3.0.0-bin-sparkfe.tgz && cd spark-3.0.0-bin-sparkfe/python && python3 setup.py install
ENV SPARK_HOME /home/jovyan/work/system/spark-3.0.0-bin-sparkfe/
RUN cd /home/jovyan/work/system && pip install fedb-2.2.0-py3-none-any.whl && rm fedb-2.2.0-py3-none-any.whl
RUN pip install lightgbm tornado requests
COPY rul /home/jovyan/work/rul
RUN pip install -r /home/jovyan/work/rul/requirements.txt
COPY taxi-trip /home/jovyan/work/taxi-trip
COPY develop_ml_application_tour_rul.ipynb /home/jovyan/work/
COPY develop_ml_application_tour_taxi.ipynb /home/jovyan/work/
WORKDIR /home/jovyan/work
