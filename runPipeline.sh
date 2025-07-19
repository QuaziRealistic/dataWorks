#!/bin/bash

echo "[1] python crowler..."
python3 python/runCrawl.py

echo "[2] r preprocessing..."
Rscript r/preprocessData.R

echo "[3] python scraper..."
python3 python/src/scraper.py

echo "[4] r digest downloaded files..."
Rscript r/processDownloads.R
