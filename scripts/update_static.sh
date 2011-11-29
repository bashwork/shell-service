#!/bin/bash
source /home/devel/env/projects/bin/activate
python shell/manage.py collectstatic
mv shell/static static-new
java -jar ./scripts/compiler/closure-js.jar --warning_level QUIET --js_output_file static/js/main.js `ls static/js/*.js`
java -jar ./scripts/compiler/closure-css.jar --output-file static/css/main.css `ls static/css/*.css`
git checkout gh-pages
cp -r static-new static
git add static
git commit -am "updating static files"
git push github gh-pages
git checkout master
