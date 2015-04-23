#!/bin/sh
ssh -o PreferredAuthentications=password athena.dialup.mit.edu 'cd /afs/athena.mit.edu/org/s/sustainability/web_scripts/summit;git pull'
