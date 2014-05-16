#!/bin/sh
rm summit/cache/*
sync
rsync -r -u -v --delete --delete-after --exclude 'dbbackup' --exclude 'README.md' --exclude 'htaccess' --exclude '.git' --exclude 'cache' --exclude '.htaccess' --exclude 'deploy.sh' . /mit/sustainability/web_scripts/summit/
