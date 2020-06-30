mkdir -p libs && cd libs
wget https://storage.4paradigm.com/api/public/dl/JqXjDwS9/fesql-spark.jar
if [[ "$OSTYPE" == "darwin"* ]]; then
    wget https://storage.4paradigm.com/api/public/dl/kGmS8y_L/fedb_client_2.0.0.0-beta.tar.gz
    tar -zxvf fedb_client_2.0.0.0-beta.tar.gz
    pip install -U fedb_client_2.0.0.0-beta/fedb-2.0.0.0-cp37-cp37m-macosx_10_9_x86_64.whl
    wget https://storage.4paradigm.com/api/public/dl/T9bEk8ho/fesql-0.1.0.0-cp37-cp37m-macosx_10_9_x86_64.whl
    pip install -U fesql-0.1.0.0-cp37-cp37m-macosx_10_9_x86_64.whl
else
    wget https://storage.4paradigm.com/api/public/dl/hPOAsawT/fedb_client_linux_2.0.0.0-beta.tar.gz
    tar -zxvf fedb_client_linux_2.0.0.0-beta.tar.gz
    pip install -U fedb_client_linux_2.0.0.0-beta/fedb-2.0.0.0-cp37-cp37m-linux_x86_64.whl
    wget https://storage.4paradigm.com/api/public/dl/TtqSKBUu/fesql-0.1.0.0-cp37-cp37m-linux_x86_64.whl
    pip install -U fesql-0.1.0.0-cp37-cp37m-linux_x86_64.whl
fi

