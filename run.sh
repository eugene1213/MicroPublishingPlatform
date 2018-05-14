# supervisord off
unlink /run/supervisor.sock

# nginx off
service nginx stop

# celery off
pkill -f "celery worker"

#supervisord on
supervisord -n