#!/bin/bash
python shell/manage.py collectstatic
mv shell/static static-new
git checkout gh-pages
rm -rf static
mv static-new static
java -jar ./scripts/compiler/closure-js.jar --output-file static/js/main.js static/js/*.js
java -jar ./scripts/compiler/closure-css.jar --output-file static/css/main.css static/css/*.css
#git add static
#git commit -am "updating static files"
#git push github gh-pages
#git checkout master
