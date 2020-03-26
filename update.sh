#!/bin/bash

. env.sh && \
  ./get_data.py && \
  git status
