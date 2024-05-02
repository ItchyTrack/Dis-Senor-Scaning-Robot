from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
from robot import Robot

app = Flask(__name__)
app.use_reloader=False


robot:Robot = None

@app.route("/")
def index():
    # rendering webpage
    return render_template('index.html')

def gen():
    global robot
    while True:
        #get camera frame
        frame = robot.getImage()
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/keypress', methods=['POST'])
def keypress():
    data = request.json
    key = data.get('key')
    is_pressed = data.get('isPressed')

    if is_pressed:
        if key == "w":
            robot.moves.append("f")
        elif key == "s":
            robot.moves.append("b")
        elif key == "a":
            robot.moves.append("l")
        elif key == "d":
            robot.moves.append("r")
        # print(f'{key} pressed')
    else:
        if key == "w":
            robot.moves.remove("f")
        elif key == "s":
            robot.moves.remove("b")
        elif key == "a":
            robot.moves.remove("l")
        elif key == "d":
            robot.moves.remove("r")
        # print(f'{key} released')

    return jsonify({'status': 'success'})

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def startWebsite(imageGetter):
    global robot
    robot = imageGetter
    threading.Thread(target=lambda: app.run(host="0.0.0.0", debug=True, use_reloader=False)).start()