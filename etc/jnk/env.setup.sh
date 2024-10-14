#!/usr/bin/env bash

test -d bin || mkdir -p bin

if [ -z "$REMOTE_WORKING_DIRECTORY" ]
then
    echo "Parametro REMOTE_WORKING_DIRECTORY no definido"
    exit 1
fi

if [ -z "$REMOTE_ASSETS_DIRECTORY" ]
then
    echo "Parametro REMOTE_ASSETS_DIRECTORY no definido"
    exit 1
fi

if [ -z "$REMOTE_USER" ]
then
    echo "Parametro REMOTE_USER no definido"
    exit 1
fi

if [ -z "$SSH_HOST" ]
then
    echo "Parametro SSH_HOST no definido"
    exit 1
fi

if [ -z "$SSH_KEY" ]
then
    echo "Parametro SSH_KEY no definido"
    exit 1
fi

if [ -z "$DOMAIN" ]
then
    echo "Parametro DOMAIN no definido"
    exit 1
fi

if [ -z "$WORKERS" ]
then
    echo "Parametro WORKERS no definido"
    exit 1
fi

if [ -z "$DOT_ENV" ]
then
    echo "Parametro DOT_ENV no definido"
    exit 1
else
    echo "${DOT_ENV}" > src/app/.env
fi

if [ -z "$ENV_PY" ]
then
    echo "Parametro ENV_PY no definido"
    exit 1
else
    echo "${ENV_PY}" > src/app/env.py
fi


if [ -z "$CONFIG_FILE" ]
then
    echo "Parametro CONFIG_FILE no definido"
    exit 1
else
    echo "${CONFIG_FILE}" > src/app/config.cfg
fi

cat > "bin/setup.sh" <<- EOM
#!/usr/bin/env bash

test -d "${REMOTE_WORKING_DIRECTORY}/tmp" || mkdir -p "${REMOTE_WORKING_DIRECTORY}/tmp"
test -d "${REMOTE_WORKING_DIRECTORY}/run" || mkdir -p "${REMOTE_WORKING_DIRECTORY}/run"
test -d "${REMOTE_WORKING_DIRECTORY}/bin" || mkdir -p "${REMOTE_WORKING_DIRECTORY}/bin"

if [ -d "${REMOTE_WORKING_DIRECTORY}/tmp/venv" ]
then
    echo "Python virtual environment exists."
else
    echo "Virtual enviroment created"
    python3 -m venv "${REMOTE_WORKING_DIRECTORY}/tmp/venv"
fi

if [ -d "${REMOTE_WORKING_DIRECTORY}/tmp/log" ]
then
    echo "Log folder exists."
else
    echo "Log folder created"
    mkdir "${REMOTE_WORKING_DIRECTORY}/tmp/log"
fi

touch "${REMOTE_WORKING_DIRECTORY}/tmp/log/nginx_error.log"
touch "${REMOTE_WORKING_DIRECTORY}/tmp/log/nginx_access.log"
touch "${REMOTE_WORKING_DIRECTORY}/tmp/log/gunicorn_supervisor.log"
EOM

cat > "bin/pip-update.sh" <<- EOM
#!/usr/bin/env bash
${REMOTE_WORKING_DIRECTORY}/tmp/venv/bin/pip install -r ${REMOTE_WORKING_DIRECTORY}/etc/requirements.txt

if [ -f "${REMOTE_WORKING_DIRECTORY}/etc/production.requirements.txt" ]
then
${REMOTE_WORKING_DIRECTORY}/tmp/venv/bin/pip install -r ${REMOTE_WORKING_DIRECTORY}/etc/production.requirements.txt
fi
EOM

cat > "bin/dj-migrate.sh" <<- EOM
#!/usr/bin/env bash
${REMOTE_WORKING_DIRECTORY}/tmp/venv/bin/python ${REMOTE_WORKING_DIRECTORY}/src/manage.py migrate
EOM

cat > "bin/dj-collectstatic.sh" <<- EOM
#!/usr/bin/env bash
${REMOTE_WORKING_DIRECTORY}/tmp/venv/bin/python ${REMOTE_WORKING_DIRECTORY}/src/manage.py collectstatic --noinput
EOM

cat > "bin/gunicorn_start.sh" <<- EOM
#!/usr/bin/env bash

NAME="${JOB_BASE_NAME}"                                  # Name of the application
REPODIR="${REMOTE_WORKING_DIRECTORY}"
NUM_WORKERS=${WORKERS};                                     # how many worker processes should Gunicorn spawn
USER="${REMOTE_USER}"

DJANGODIR="\$REPODIR/src"        # Django project directory
SOCKFILE="\$REPODIR/run/gunicorn.sock"  # we will communicte using this unix socket
USER="\$USER"	# the user to run as
GROUP="\$USER"                                  # the group to run as
DJANGO_SETTINGS_MODULE=app.settings
DJANGO_WSGI_MODULE=app.wsgi                     # WSGI module name

echo "Starting \$NAME as \`whoami\`"

# Activate the virtual environment
cd \$DJANGODIR
source ../tmp/venv/bin/activate
export DJANGO_SETTINGS_MODULE=\$DJANGO_SETTINGS_MODULE
export PYTHONPATH=\$DJANGODIR:\$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=\$(dirname \$SOCKFILE)
test -d \$RUNDIR || mkdir -p \$RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../tmp/venv/bin/gunicorn \${DJANGO_WSGI_MODULE}:application \
    --timeout 600 \
    --name \$NAME \
    --workers \$NUM_WORKERS \
    --user=\$USER --group=\$GROUP \
    --bind=unix:\$SOCKFILE \
    --log-level=debug \
    --log-file=-
EOM

cat > "bin/celery_start.sh" <<- EOM
#!/usr/bin/env bash

REPODIR="${REMOTE_WORKING_DIRECTORY}"
DJANGODIR="\$REPODIR/src"        # Django project directory

# Activate the virtual environment
cd \$DJANGODIR
source ../tmp/venv/bin/activate

# Start
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../tmp/venv/bin/celery --app=app.celery:app worker --loglevel=INFO -n worker.%%h
EOM

cat > "etc/${DOMAIN}-nginx" <<- EOM
upstream ${DOMAIN}_server{
    server unix:${REMOTE_WORKING_DIRECTORY}/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name ${DOMAIN};
    error_log ${REMOTE_WORKING_DIRECTORY}/tmp/log/nginx_error.log;
    access_log ${REMOTE_WORKING_DIRECTORY}/tmp/log/nginx_access.log;

    location /static/ {
        autoindex on;
        alias ${REMOTE_ASSETS_DIRECTORY}/static/;
    }

    location /media/ {
        autoindex on;
        alias ${REMOTE_ASSETS_DIRECTORY}/media/;
    }

    location / {
                proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                # proxy_set_header X-Forwarded-Proto https;
                proxy_set_header Host \$http_host;
                proxy_redirect off;
                # proxy_buffering off;

                if (!-f \$request_filename) {
                        proxy_pass http://${DOMAIN}_server;
                        break;
                }
        }
}
EOM

cat > "etc/supervisor.conf" <<- EOM
[program:${DOMAIN}]
command = ${REMOTE_WORKING_DIRECTORY}/bin/gunicorn_start.sh       ; Command to start app
user = ${REMOTE_USER} ; User to run as
stdout_logfile = ${REMOTE_WORKING_DIRECTORY}/tmp/log/gunicorn_supervisor.log   ; Where to write log messages
redirect_stderr = true                                                ; Save stderr in the same log
logfile_maxbytes = 64MB
logfile_backups = 8
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8                       ; Set UTF-8 as default encoding

[program:${DOMAIN}-celery]
command = ${REMOTE_WORKING_DIRECTORY}/bin/celery_start.sh       ; Command to start app
user = ia
stdout_logfile = ${REMOTE_WORKING_DIRECTORY}/tmp/log/celery_supervisor.log ; Where to write log messages
redirect_stderr = true                                                ; Save stderr in the same log
logfile_maxbytes = 64MB
logfile_backups = 8
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8                       ; Set UTF-8 as default encoding
EOM