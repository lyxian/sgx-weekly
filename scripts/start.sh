#!/bin/bash

cd app

# Remove existing data files
if [[ `ls data | grep "\.csv"` ]]; then
find data/*.csv | xargs -I % rm %
fi

if [ -f weekly.html ]; then
rm weekly.html
fi

# Run python app
python app.py