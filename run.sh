# supervisord off
unlink /run/supervisor.sock

# nginx off
#service nginx stop

#nginx stop

fuser -k 80/tcp

# celery off
pkill -f "celery worker"

#supervisord on
supervisord -n