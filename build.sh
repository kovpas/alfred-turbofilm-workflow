#!/bin/sh
find . -name '*.pyc' | xargs rm
rm -f turbofilm.alfredworkflow
find . -maxdepth 1 ! -name ".DS_Store" ! -name ".git*" ! -name ".turbofilm.*" ! -name "archive.zip" ! -name "build.sh" ! -name "." ! -name "debug.log" ! -name "README.md" | xargs zip -r turbofilm.alfredworkflow