FROM python:3.8

WORKDIR /app
ADD . /app
RUN pip3 install -r requirements.txt
# CMD [ "uwsgi", "app.ini" ]
# RUN apt-get update \
    # &&  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
    
# RUN TZ=Asia/Taipei \
#     && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
#     && echo $TZ > /etc/timezone \
#     && dpkg-reconfigure -f noninteractive tzdata 