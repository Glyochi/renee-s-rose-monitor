import os
from flask import Flask, request, send_from_directory, make_response, jsonify
from flask_socketio import SocketIO
import threading
from PIL import Image
import base64
import cv2
from io import BytesIO


class Realtime_Server:
    
    def __init__(self):
        self.__app = Flask(__name__, static_folder='../backend/ui_build')
        self.__socketio = SocketIO(self.__app, cors_allowed_origins="*", async_mode="threading")
        self.__server_thread = None
        
        # Call the setup functions
        self.__setup_routes()
        self.__setup_sockets()


    def __setup_routes(self):
        # Serve React App
        @self.__app.route('/', defaults={'path': ''})
        @self.__app.route('/<path:path>')
        def serve(path):
            # return "hi :)"
            if path != "" and os.path.exists(self.__app.static_folder + '/' + path):
                return send_from_directory(self.__app.static_folder, path)
            else:
                return send_from_directory(self.__app.static_folder, 'index.html')

        @self.__app.route('/health')
        def on_health():
            data = {
                'health': 'Server is up'
            }
            respone = jsonify(data)
            respone.headers.add("Access-Control-Allow-Origin", "*")
            return make_response(respone, 200)

    def __setup_sockets(self):
        # Websocket
        @self.__socketio.on('message')
        def handle_on_message(data):
            print('received message: ' + data)

        @self.__socketio.on('connect')
        def handle_on_connect():
            session_id = request.sid
            print('connecting ', session_id)
        
        
    def start_server(self):
        # self.__socketio.run(self.__app, port=5000, debug=False, use_reloader=True)
        self.__socketio.run(self.__app, host='0.0.0.0', port=5000)
    
    def start_server_in_new_thread(self):
        if self.__server_thread != None:
            return False
        
        t = threading.Thread(target=lambda: self.__socketio.run(self.__app, host='0.0.0.0', port=5000), daemon=True)
        self.__server_thread = t
        self.__server_thread.start()

        return True

    
    def emit_data(self, event_name, data):
        self.__socketio.emit(event_name, data)
            

    def stream_frame(self, data):
        image = Image.fromarray(cv2.cvtColor(data['frame'], cv2.COLOR_BGR2RGB))
        buff = BytesIO()
        image.save(buff, format="JPEG")
        base64_frame_str = base64.b64encode(buff.getvalue()).decode('utf-8')
        formatted_data = {"base64_frame": base64_frame_str}
        
        
        self.__socketio.emit("stream_frame", formatted_data)

# server = Server()
# server.start_server()
