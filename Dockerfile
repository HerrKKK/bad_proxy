FROM python:3.10

COPY ./ /usr/bad_proxy
WORKDIR /usr/bad_proxy

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo 'Asia/Shanghai' >/etc/timezone

CMD python3 src/main.py -c conf/blog_server.json

