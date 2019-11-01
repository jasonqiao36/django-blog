#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

#sleep 3

celery -A django_blog.taskapp worker --loglevel INFO --workdir /code/django-blog
