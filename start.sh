#!/usr/bin/env bash
source /home/webuser/virtualenvs/freeswitch/bin/activate
/home/webuser/virtualenvs/freeswitch/bin/uwsgi --ini /home/webuser/fs-curl-directory/uwsgi.ini
