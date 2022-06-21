"""
This program is kind of a middleware responsible for handling web requests and providing sort of an API
It can serve template web pages
It can add requests to a queue and know if they are locked or not
It can read elevator status and display it in realtime on a webpage
"""
import socket

from flask import Flask, render_template, Response, request, redirect, url_for

app = Flask(__name__)


# rendering the HTML page which has the button
@app.route('/json')
def json():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return render_template('json.html', local_ip=local_ip)


# background process happening without any refreshing
@app.route('/background_process_test', methods=['GET', 'POST'])
def background_process_test():
    # if the user requests a post request check if the request is already in the queue and return a status
    # if the request is not currently in the queue then add it and return a status
    if request.method == "POST":
        floor = request.form['floor']
        try:
            with open("./queue/"+floor+".q", "r") as fo:
                fo.readlines()
            status = "Locked"
        except IOError:
            with open("./queue/"+floor+".q", "w") as fo:
                fo.write(floor)
            print("User requested floor %s" % floor)
            status = "User requested floor %s" % floor
    # if the user requests a get request check the current status of the elevator
    elif request.method == "GET":
        try:
            with open("./queue/elevator.log", "r") as fo:
                status = fo.readlines()
                status = "".join(status)
        except IOError:
            status = "The elevator is currently disabled"
    return status
