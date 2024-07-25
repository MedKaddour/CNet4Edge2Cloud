from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def get_noise_level():
    return str(random.uniform(50, 100)) + " dB"  # Random noise level between 50 and 100 dB

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
