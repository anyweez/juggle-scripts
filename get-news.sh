#!/bin/sh

echo "Reading news stories."

while read line
do
	python fetch-rss.py $line
done
