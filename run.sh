#!/bin/bash

export PYTHONPATH=.
source venv/bin/activate

if [ $1 == poller ]
then
	python ./bot_long_poll/main.py
elif [ $1 == worker ]
then
	python ./bot/main.py
fi