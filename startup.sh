sudo docker run \
    -v `pwd`:/bad_proxy \
    -v /etc/letsencrypt:/etc/letsencrypt \
    -w /bad_proxy \
    --net=host --restart=always \
    --name bad_proxy -d python:3.10 \
    python3 src/main.py -c conf/blog_server.json
