#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

for f in scripts/*.sql
do 
filename=$(basename "$f")
mysql -h qhmobile.ci9ey74meneu.us-east-1.rds.amazonaws.com -uqhmobile -pqhmobile < $f | sed 's/	/,/g' > reports/${filename%.*}.csv
done

zip -P qhmobile ../opt/qhmobile/static/report.zip reports/*
