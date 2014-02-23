#!/bin/sh
rsync -r -u -v --delete --delete-after --exclude 'htaccess' --exclude '.htaccess' --exclude 'deploy.sh' . /mit/summit/new/
