sudo docker run \
    -v `pwd`:/usr/bad_proxy \
    -v /etc/letsencrypt/live/wwr-blog.com:/usr/bad_proxy/certs \
    -w /usr/bad_proxy \
    --net=host --restart=always \
    --name bad_proxy -d python:3.10 \
    python3 src/main.py -c blog_config.json
