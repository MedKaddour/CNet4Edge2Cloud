from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def get_density_detection():
    densities = ['low', 'medium', 'high']
    return random.choice(densities)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)