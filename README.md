# FEDB with SparkSQL demo

## 工程文件介绍

* data 目录，里面存放着相关训练数据
* get_deps.sh 用于下载依赖jar包
* train.sh 用于运行训练模型流程
* train_sql.py 被train.sh使用pyspark脚本
* predict.py 实时推理服务脚本
* import.py 用于创建数据库，表，导入数据工具

## 支持运行环境

目前只支持在第四范式官方镜像内部运行

## 运行模型训练过程

```
sh train.sh
```

