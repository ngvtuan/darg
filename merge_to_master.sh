#!/bin/bash

git checkout master && git merge develop --no-edit && ./gitversioning.sh && git push && git checkout develop
