import requests

# logger used everywhere to log things to nodejs
def Log(stack, level, packageName, message):
    data = {
        "stack": stack,
        "level": level,
        "packageName": packageName,
        "message": message
    }

    try:
        # sends POST to localhost ie our  logs.js running on port 4000
        requests.post("http://localhost:4000/log", json=data)
    except:
        print("log server maybe not running?")  # optional debug
