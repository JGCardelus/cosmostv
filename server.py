from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import config
import io
import socket

#SERVER VARS
port = config.port

#CREATE SERVER
web = Flask("cosmostv")
web.config["SECRET_KEY"] = "cosmostv"

#CREATE WEBSOCKET
server = SocketIO(web)

#CONNECTION VALIDATION
@server.on("validate_connection")
def validate_connection():
    print("User connected, validating websocket connection")
    server.emit("connection_validated")

#SERVER ROUTING
@web.route('/')
def index():
    return render_template("main.html")

def change_frontend_connection():
    global port

    ip_addr = get_ip()

    client_server = open('static/framework.js', 'r')
    client_server_lines = client_server.readlines()
    for i, line in enumerate(client_server_lines):
        if line.rstrip().lstrip() == '//$SOCKET_IP':
            client_server_lines[i + 1] = '  socket = io.connect("http://' + ip_addr + ':'+ str(port) +'"); //This line was autogenerated.\n'
            break

    client_server = open('static/framework.js', 'w')
    client_server.writelines(client_server_lines)
    client_server.close()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

def start():
    global port
    change_frontend_connection()
    connection_url = 'http://' + get_ip() + ':'+ str(port)
    print("Server started at ip: %s" % (connection_url))
    server.run(web, host='0.0.0.0', port=port)