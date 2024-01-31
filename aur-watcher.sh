#/bin/sh
python aurwatcher.py "$@" | sudo python pager.py
