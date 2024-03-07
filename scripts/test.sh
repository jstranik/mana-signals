#!/bin/bash

diff -s \
  <(gunzip -c marketdata/20231101.OP.csv.gz | python3 example-inline.py 2>/dev/null) \
  <(gunzip -c marketdata/20231101.OP.csv.gz | python3 example-ops.py 2>/dev/null) 
