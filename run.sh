#!/bin/bash

sourse env/bin/activate
pip install aiohttp binance-futures-connector
python3 main.py