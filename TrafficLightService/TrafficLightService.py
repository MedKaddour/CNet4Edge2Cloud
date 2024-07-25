from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def get_traffic_light_status():
    traffic_lights = ['red', 'yellow', 'green']
    return random.choice(traffic_lights)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)