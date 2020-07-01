export JAVA_HOME=/work/jdk1.8.0_121
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_HOME=/work/spark-2.3.4-bin-hadoop2.7
export PATH=$SPARK_HOME/bin:$PATH
export FESQL_HOME=./libs
export FESQL_JAR_FILE=fesql-spark.jar
python3 train_sql.py

