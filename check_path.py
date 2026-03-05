import sys
import os

print("Sys path:", sys.path)
print("CWD:", os.getcwd())

try:
    import werkzeug
    print("Werkzeug found at:", werkzeug.__file__)
except ImportError as e:
    print("Werkzeug not found:", e)

try:
    import flask
    print("Flask found at:", flask.__file__)
except ImportError as e:
    print("Flask not found:", e)
except Exception as e:
    print("Flask import error:", e)
