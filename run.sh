# supervisord off
unlink /run/supervisor.sock
# nginx off
service nginx stop
# supervisord on
supervisord -n