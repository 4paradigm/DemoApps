from jupyter/all-spark-notebook:latest

COPY zookeeper-3.4.14.tar.gz /home/jovyan/work
COPY fedb-2.2.0-linux.tar.gz /home/jovyan/work
COPY spark-3.0.0-bin-sparkfe.tgz /home/jovyan/work
COPY fedb-2.2.0-py3-none-any.whl /home/jovyan/work
COPY jdk-8u141-linux-x64.tar.gz /home/jovyan/work

RUN cd /home/jovyan/work && tar -zxvf jdk-8u141-linux-x64.tar.gz && rm jdk-8u141-linux-x64.tar.gz 
ENV JAVA_HOME /home/jovyan/work/jdk1.8.0_141
ENV PATH $JAVA_HOME:$PATH
RUN cd /home/jovyan/work && tar -zxvf zookeeper-3.4.14.tar.gz && rm zookeeper-3.4.14.tar.gz  && cd zookeeper-3.4.14 && mv conf/zoo_sample.cfg conf/zoo.cfg
RUN cd /home/jovyan/work && tar -zxvf fedb-2.2.0-linux.tar.gz && rm fedb-2.2.0-linux.tar.gz
RUN cd /home/jovyan/work && tar -zxvf spark-3.0.0-bin-sparkfe.tgz && rm spark-3.0.0-bin-sparkfe.tgz && cd spark-3.0.0-bin-sparkfe/python && python3 setup.py install
RUN cd /home/jovyan/work && pip install fedb-2.2.0-py3-none-any.whl && rm fedb-2.2.0-py3-none-any.whl
RUN pip install lightgbm tornado requests
COPY demo /home/jovyan/work/demo
COPY develop_ml_application_tour.ipynb /home/jovyan/work/
WORKDIR /home/jovyan/work
