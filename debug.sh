sudo docker run \
    -v `pwd`:/usr/bad_proxy \
    -v /etc/letsencrypt:/etc/letsencrypt \
    -w /usr/bad_proxy \
    --net=host --restart=always \
    --name bad_proxy -it python:3.10 \
    python3 src/main.py -c conf/blog_server.json