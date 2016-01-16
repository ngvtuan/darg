#!/bin/bash
echo "merge-to-master: $1"

git checkout master && git merge develop --no-edit && ./gitversioning.sh $1 && git push && git checkout develop && git push
