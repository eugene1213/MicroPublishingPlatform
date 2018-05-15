# supervisord off
unlink /run/supervisor.sock

# nginx off
#service nginx stop

#nginx stop

fuser 80/tcp

# celery off
pkill -f "celery worker"

#supervisord on
supervisord -n