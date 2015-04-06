@echo off

:start

start "" "Crawler.py"
ping -n 90 127.0>nul

start "" "classfy.py"
ping -n 5 127.0>nul

start "" "classification.py"
ping -n 7200 127.0>nul

goto start