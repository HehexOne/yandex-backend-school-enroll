import os
import sys

try:
    if sys.argv[1] == "start-dev":
        os.system("uvicorn main:app --reload")
    elif sys.argv[1] == "start":
        os.system("uvicorn main:app")
    else:
        print("Unknown script")
except KeyboardInterrupt as e:
    print("Stopped...")

