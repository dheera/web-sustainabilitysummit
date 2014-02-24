#!/bin/sh
rsync -r -u -v --delete --delete-after --exclude 'README.md' --exclude 'htaccess' --exclude '.git' --exclude '.htaccess' --exclude 'deploy.sh' . /mit/dheera/web_scripts/sustainabilitysummit-test/
