#!/bin/bash

cd app

# Checkout new branch if not exists
branchName=`date +%Y-%b | tr A-Z a-z`
if [[ `git branch | grep $branchName` ]]; then
git checkout master
git branch -D $branchName
fi
git checkout -b $branchName

# Remove existing data files
if [[ `ls data | grep "\.csv"` ]]; then
find data/*.csv | xargs -I % rm %
fi

if [ -f weekly.html ]; then
rm weekly.html
fi

# Extract data
python weekly.py
python postWeekly.py

# Push branch
git add . ; git commit -m "$branchName"
git push

# Run dashboard
python app.py