import os
import sys

try:
    if sys.argv[1] == "start-dev":
        os.system("uvicorn main:app --reload --reload --host 0.0.0.0 --port 80")
    elif sys.argv[1] == "start":
        os.system("gunicorn --workers=4 -b 0.0.0.0:80 -k uvicorn.workers.UvicornWorker main:app")
    else:
        print("Unknown script")
except KeyboardInterrupt as e:
    print("Stopped...")

