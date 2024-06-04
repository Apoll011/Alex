from flask import Flask, render_template

app = Flask(__name__)

@app.route('/') 
def index():
    return render_template('index.html', user_name="Tiago Bernardo", date="4 tue Sat", climate = {"icon": "sun", "degree": "24", "city": "Mindelo", "country": "Cape Vert"})

@app.route('/plugins.html') 
def plugins():
    return render_template('plugins.html')

@app.errorhandler(404) 
def page_not_found(e):
    return render_template('error.html' , errorcode=404, error_description="Page Not Found", error_link="./"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', errorcode=500, error_description="Server error", error_link="./"), 500

if __name__ == '__main__':
    app.run(debug=True)
