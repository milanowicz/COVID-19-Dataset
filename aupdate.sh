#!/bin/bash

. env.sh && \
  ./get_data.py && \
  git status && \
  git commit -am 'Update data.' && \
  git push origin master
