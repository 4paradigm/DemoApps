# FEDB with SparkSQL demo

## 工程文件介绍

* data 目录，里面存放着相关训练数据
* get_deps.sh 用于下载依赖jar包
* train.sh 用于运行训练模型流程
* train_sql.py 被train.sh使用pyspark脚本
* predict_server.py 实时推理服务脚本
* import.py 用于创建数据库，表，导入数据工具
* predict.py 用于发送请求脚本

## 支持运行环境

目前只支持在第四范式官方镜像内部运行

### 安装镜像

本地机器cpu如果比较好可以下载高压缩比的包

```
wget https://storage.4paradigm.com/api/public/dl/ccDsyXV9/fedb_2.0.0_beta.zip
unzip fedb_2.0.0_beta.zip
docker load -i fedb_2.0.0_beta.tar
```

cpu差可以直接下载非压缩版本

```
wget https://storage.4paradigm.com/api/public/dl/Mur8vGqz/fedb_2.0.0_beta.tar
docker load -i fedb_2.0.0_beta.tar
```

## 执行demo

```
docker run -d develop-registry.4pd.io/fedb:2.0.0
```

找到容器id, 并进入
```
docker ps | grep fedb | awk '{print $1}' 
55275653a728
# 进行容器
docker exec -it 55275653a728 /bin/bash
# 运行fedb数据库命令
fedb --zk_cluster=127.0.0.1:2181 --zk_root_path=/fedb --role=sql_client 2>/dev/null
  ______   _____  ___
 |  ____|  |  __ \|  _ \
 | |__ ___ | |  | | |_) |
 |  __/ _  \ |  | |  _ <
 | | |  __ / |__| | |_) |
 |_|  \___||_____/|____/

v2.0.0.0
127.0.0.1:6527/>
```
看到如上信息说明镜像运行成功

运行例子

```
git clone https://github.com/4paradigm/SparkSQLWithFeDB.git
cd SparkSQLWithFeDB
# 下载llvm加速版本spark
sh get_deps.sh
# 训练模型, 看到如下信息说明训练成功
sh train.sh
[1]	valid_0's l1: 621.924	valid_0's l2: 1.1707e+07
Training until validation scores don't improve for 5 rounds
[2]	valid_0's l1: 623.901	valid_0's l2: 1.17068e+07
[3]	valid_0's l1: 625.088	valid_0's l2: 1.17101e+07
[4]	valid_0's l1: 626.609	valid_0's l2: 1.17146e+07
[5]	valid_0's l1: 628.498	valid_0's l2: 1.17201e+07
[6]	valid_0's l1: 628.743	valid_0's l2: 1.1722e+07
Early stopping, best iteration is:
[1]	valid_0's l1: 621.924	valid_0's l2: 1.1707e+07

# 创建数据库和表并导入数据到数据库
python3 import.py
# 启动推理服务
python3 predict_server.py >log 2>&1 &

# 发送推理请求 ,会看到如下输出
python3 predict.py
----------------ins---------------
[[ 2.       40.774097 40.774097 40.774097 40.774097 40.774097 40.774097
  40.774097 40.774097  1.        1.      ]]
---------------predict trip_duration -------------
859.3298781277192 s
```





