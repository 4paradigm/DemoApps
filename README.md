# FEDB with SparkSQL demo

## 工程文件介绍

* data 目录，里面存放着相关训练数据
* get_deps.sh 用于下载依赖jar包
* train.sh 用于运行训练模型流程
* train_sql.py 被train.sh使用pyspark脚本
* predict.py 实时推理服务脚本
* import.py 用于创建数据库，表，导入数据工具


## 支持系统环境

* linux glibc > 2.12
* macos 10.15.5

目前只支持以上环境

## 下载Apache Spark包

spark包请到官网下载，目前支持版本为2.4.x，请下载对应版本，最后配置好SPARK_HOME环境变量，以及相应的JAVA_HOME

## 下载llvm加速版本的sparksql依赖库

```
sh get_deps.sh
```

## 安装python依赖

整个demo需要在python3环境运行

```
pip install -r requirements.txt
```

## 运行模型训练过程

```
sh train.sh
```

