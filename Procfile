web: python shell/manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 1
#web: python shell/manage.py streaming $PORT
worker: python shell/apps/serial/runner.py $PORT

