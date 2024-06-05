from flask import Flask, render_template, flash
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'eryh840tiwry48ouehrjg8yoeuhgye58ohrugd'

defs = {
        "user": {
            "name": "Tiago",
            "id": 1,
            "weather": {
                "city": "Sao Vicente",
                "country": "Cabo Verde",
                "icon": "sun",
                "degree": "27"
            }
        },
        "device_id": "1",
        "update_date": "26 JUL 23 (10:24)",
        "location": "localhost",
        "port": "5500",
        "notifications": [
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
            ],
        "system": {
            "overall": {
                "cpu": "53%",
                "disk_usage": "12%",
                "ram": "2%",
                "batery": "86%",
                "internet": "0",
                "status": "OK"
            },
            "data": {
                "process_exec_t": "1042",
                "comands_gt": "62",
                "net_com": "6236",
                "data_fls": "5235",
                "errors_t":"2",
                "chart": {
                    "cpu_usage": [19, 48, 70, 60, 63, 56, 33, 17, 59, 21, 36, 12, 39, 59, 62, 23, 12, 8, 9, 4, 6, 10, 2, 5, 19],
                    "internet_usage": [3, 16, 39, 50, 35, 48, 24, 0, 29, 1, 5, 0, 24, 34, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 3]
                },
                "plot": {
                        "datasets": [
                        {
                            "label": "Wake Up",
                            "data": [{
                                "x": 10,
                                "y": 0
                            },
                            {
                                "x": 2,
                                "y": 3
                            }],
                            "backgroundColor": "rgb(255, 9, 13)",
                            "borderColor": "rgba(255,19,12,1)",
                            "borderWidth": 1
                        },
                        {
                            "label": "Api Calls",
                            "data": [{
                                "x": 11,
                                "y": 53
                            },
                            {
                                "x": 12,
                                "y": 30
                            },
                            {
                                "x": 10,
                                "y": 5
                            }
                            ],
                            "backgroundColor": "rgb(54, 162, 235)",
                            "borderColor": "rgba(54, 192, 235, 1)",
                            "borderWidth": 1
                        }
                        ]
                }
            }
        },
        "nexus":[
            {
                "AI": "Main AI",
                "Acronym": "ALEX",
                "Status": "Open"
            },
            {
                "AI": "Pre Iniciator of Alex",
                "Acronym": "PRIA",
                "Status": "Open"
            },
            {
                "AI": "Api Micro Inteligence",
                "Acronym": "AMI",
                "Status": "Open"
            },
            {
                "AI": "Dictionary Inteligence System",
                "Acronym": "DIS",
                "Status": "Open"
            },
            {
                "AI": "Healty Inteligence System",
                "Acronym": "HIS",
                "Status": "Open"
            },
            {
                "AI": "Learn Inteligence System",
                "Acronym": "LIS",
                "Status": "Open"
            },
            {
                "AI": "Neural Artificial Tech",
                "Acronym": "NAT",
                "Status": "Open"
            },
            {
                "AI": "Strategy and Military Intelligence",
                "Acronym": "SAMI",
                "Status": "Closed"
            },
            {
                "AI": "System Integreated Design",
                "Acronym": "SID",
                "Status": "Error"
            },
            {
                "AI": "World External Communication",
                "Acronym": "WEC",
                "Status": "Open"
            }
        ]
    }
    

@app.route('/') 
def index():
    flash("Hithere")
    return render_template('index.html',len=len, **defs)

@app.route('/plugins.html') 
def plugins():
    return render_template('plugins.html', len=len, **defs)

@app.errorhandler(404) 
def page_not_found(e):
    return render_template('error.html' , errorcode=404, error_description="Page Not Found", error_link="./"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', errorcode=500, error_description="Server error", error_link="./"), 500

if __name__ == '__main__':
    app.run(debug=True)
