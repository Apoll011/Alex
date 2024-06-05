from flask import Flask, render_template, flash
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'eryh840tiwry48ouehrjg8yoeuhgye58ohrugd'
@app.route('/') 
def index():
    flash("Hithere")
    return render_template('index.html',len=len, user = {"name": "Tiago Bernardo"}, 
                           climate = {"icon": "sun", "degree": "24", "city": "Mindelo", "country": "Cape Vert", "date": datetime.now()},
                           notifications = [
                                {
                                    "title": "Aplication Error Fixed",
                                    "date": "26 JUL 23 (10:26)",
                                    "description": "The Error ID#4523624 of Type 2 has been fixed",
                                    "icon": "info-alt",
                                    "bg": "success"
                                },
                                {
                                    "title": "New user registration",
                                    "date": "26 JUL 23 (10:28)",
                                    "description": "User 524 was been learn",
                                    "icon": "user",
                                    "bg": "info"
                                },
                                {
                                    "title": "System Started",
                                    "date": "26 JUL 23 (10:30)",
                                    "description": "Alex System Have Started",
                                    "icon": "settings",
                                    "bg": "warning",
                                    "costume_class": "infinite-spin"
                                }
                            ]
                           )

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
