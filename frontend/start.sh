#!/bin/bash
app="techdocs-frontend"
port=80
docker build -t ${app} .

docker run -d -p ${port}:80 \
  --name=${app} \
  -v $PWD:/app ${app}

echo "Serving on :${port}"
