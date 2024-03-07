#!/bin/bash

echo "Downloading market data (~200 MB)"

mkdir -p marketdata

for m in 0{1..9} 10 11 12; do
  for s in XRP OP MATIC; do
    wget -O marketdata/2023${m}01.$s.csv.gz https://datasets.tardis.dev/v1/bybit/trades/2023/${m}/01/${s}USDT.csv.gz
  done
done