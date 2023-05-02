#!/bin/bash
chmod ugo+x run.py
chmod ugo+x app.py
exec python3 ./run.py &
exec python3 ./app.py &