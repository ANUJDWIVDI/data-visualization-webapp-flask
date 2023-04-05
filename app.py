from flask import Flask, render_template

app = Flask(__name__)

# Home Page


@app.route('/')
def home():
    return render_template('home.html')
@app.route('/home')
def home1():
    return render_template('home.html')

# Age Page
@app.route('/age')
def age():
    return render_template('age.html')

# Gender Page
@app.route('/gender')
def gender():
    return render_template('gender.html')

# Zone Page
@app.route('/zone')
def zone():
    return render_template('zone.html')

# Device Used Page
@app.route('/deviceused')
def deviceused():
    return render_template('deviceused.html')

# Network Used Page
@app.route('/networkused')
def networkused():
    return render_template('networkused.html')

# Favorite Sport Page
@app.route('/favsport')
def favsport():
    return render_template('favsport.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)