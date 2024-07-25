from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def get_air_quality_index():
    return str(random.randint(1, 100))  # Random air quality index between 1 and 100

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)