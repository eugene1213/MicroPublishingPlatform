FROM        jhe702/basebuild:base
MAINTAINER  develop@octocolumn.com
# zsh
RUN apt-get install zsh
RUN chsh -s /usr/bin/zsh

RUN curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
# 파이썬 패키
#RUN apt-get install python3 && apt-get install python-pip



# pyenv
#RUN apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
#libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
#xz-utils tk-dev
#
#RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
#
## virtualevn
#RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
# nginx


ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

#RUN curl "https://github.com/gliderlabs/herokuish/releases/download/v0.4.0/herokuish_0.4.0_linux_x86_64.tgz" \
#    --silent -L | tar -xzC /bin
#RUN /bin/herokuish buildpack install \
#  && ln -s /bin/herokuish /build \
#  && ln -s /bin/herokuish /start \
#  && ln -s /bin/herokuish /exec

ENV         LANG C.UTF-8

# 현재경로의 모든 파일들을 컨테이너의 /srv/app폴더에 복사
COPY         .  /srv/app
# cd /srv/app와 같은 효과
WORKDIR     /srv/app

RUN         pyenv local app

# requirements설치
RUN         /root/.pyenv/versions/app/bin/pip install -r /srv/app/requirements/requirements.txt

## supervisor파일 복사
COPY        .config/supervisor/uwsgi.conf /etc/supervisor/conf.d/
COPY        .config/supervisor/nginx.conf /etc/supervisor/conf.d/
COPY        .config/supervisor/celery.conf /etc/supervisor/conf.d/

##
## nginx파일 복사
COPY        .config/nginx/nginx.conf /etc/nginx/nginx.conf
COPY        .config/nginx/app.conf /etc/nginx/sites-available/app.conf
RUN         rm -rf /etc/nginx/sites-enabled/default
RUN         rm -rf /etc/init/nginx.conf
RUN         ln -sf /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled/app.conf

# uWSGI
RUN         mkdir -p /var/log/uwsgi/app

# favicon
#COPY        octocolumn/static/images/favicon/favicon.ico /srv/app/favicon.ico

## front프로젝트 복사
#WORKDIR     /srv
#WORKDIR     /srv/front
#RUN         npm install
#RUN         npm run build



# collectstatic 실행
RUN         /root/.pyenv/versions/app/bin/python /srv/app/octocolumn/manage.py collectstatic --settings=config.settings.deploy --noinput
# manage.py
#WORKDIR     /srv/app/octocolumn

#RUN         /root/.pyenv/versions/app/bin/python manage.py collectstatic --noinput
#RUN         /root/.pyenv/versions/app/bin/python /srv/app/octocolumn/manage.py makemigrations --settings=config.settings.deploy --noinput
#RUN         /root/.pyenv/versions/app/bin/python /srv/app/octocolumn/manage.py migrate --settings=config.settings.deploy --noinput

# Azure
#RUN apt-get update \
#    && apt-get install -y --no-install-recommends openssh-server \
#    && echo "root:Docker!" | chpasswd
#
#COPY sshd_config /etc/ssh/
#
#EXPOSE 2222 80
#
#RUN service ssh start
##

#RUN wget http://download.redis.io/redis-stable.tar.gz
#RUN tar xvzf redis-stable.tar.gz
#RUN cd redis-stable
#RUN make
#
#RUN redis-server


# Certbot 설치
#RUN apt-get update
#RUN apt-get install -y software-properties-common
#RUN add-apt-repository -y ppa:certbot/certbot
#RUN apt-get update
#RUN apt-get install dialog apt-utils -y
#RUN apt-get install -y python-certbot-nginx
#
#RUN         cp /srv/app/.config/supervisor/* \
#                /etc/supervisor/conf.d/

RUN chmod +x run.sh

#CMD         supervisord -n
#EXPOSE      80
RUN ./run.sh
EXPOSE      80


# certbot --nginx -d www.octocolumn.com
#RUN certbot certonly -d www.octocolumn.com -d octocolumn.com
#
#RUN certbot renew
#
#RUN service nginx restart
# 실행시
# docker run --rm -it -p 9000:8000 eb /bin/zsh

# 1. 실행중인 컨테이너의 내부에서 uwsgi를 사용해서 8000번 포트로 외부와 연결해서 Django를 실행해보기
# 2. docker run실행시 곧바로 uWSGI에 의해서 서버가 작동되도록 Dockerfile을 수정 후 build, run해보기
#   supervisor사용
# 3. uwsgi설정을 ini파일로 작성(.config/uwsgi/uwsgi-app.ini)하고
#     작성한 파일로 실행되도록 supervisor/uwsgi.conf파일을 수정
# 4. nginx설정파일, nginx사이트파일 (nginx.conf, nginx-app.conf)을 각각
#     /etc/nginx/nginx.conf, /etc/nginx/sites-available/nginx-app.conf로 복사
#    이후 링크작성 (/etc/nginx/sites-enabled/app.conf로 /etc/nginx/sites-available/app.conf를 연결)
#     /etc/nginx/sites-enabled/default 삭제
# 4-1. supervisord실행부분을 주석처리하고 docker run으로 /bin/zsh을 2개 실행 (2번째는 docker exec사용)
#       직접 nginx와 uwsgi를 실행해서 외부에서 80번포트로 잘 연결되는지 확인
#       안되면 로그확인하기
#           uwsgi: /tmp/uwsgi.log
#           nginx: /var/log/nginx/error.log



# uwsgi실행경로
#    /root/.pyenv/versions/app/bin/uwsgi

# uwsgi를
#    http 8000포트,
#    chdir 프로젝트 django코드
#    home 가상환경 경로 적용 후 실행
#/root/.pyenv/versions/app/bin/uwsgi \
#--http :8000 \
#--chdir /srv/app/django_app \
#--home /root/.pyenv/versions/app -w config.wsgi.debug