#!/bin/bash
pkill -9 uwsgi
sleep 1
uwsgi /home/ubuntu/Site/Site/uwsgi.ini

sleep 5
uwsgi /home/ubuntu/Site/Site/uwsgi.ini

sleep 10
uwsgi /home/ubuntu/Site/Site/uwsgi.ini

