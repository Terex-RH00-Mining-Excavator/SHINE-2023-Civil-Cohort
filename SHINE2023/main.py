import cv2
import time
import numpy
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response, stream_with_context, request, jsonify
 
app = Flask(__name__)
trigPin = 3
echoPin = 5
distance = 0
r, g, b = 0, 0, 0
video =  cv2.VideoCapture(0)
 
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
 
time.sleep(0.1)
 
# Replicated function (by me) of Arduino's pulsein()
def pulseIn(pin, timeout=1000):
    
    pulseStart, timeStart = 0, time.time()*1000;
    
    while GPIO.input(pin) == False:                 # wait for sound
        if(time.time()*1000 - timeStart > timeout):
            return 0
    
    pulseStart = time.time()                        # start-Time
    
    while GPIO.input(pin) == True:                  # wait for final soundwave
        if(time.time()*1000 - timeStart > timeout):
            return 0
    
    return (time.time() - pulseStart)               # return time difference
 
# video src with contours using OpenCV
def video_stream_contours():
    global distance
    while True:
        
        ###################################### Ultrasonic Sensor Code
        GPIO.output(trigPin, False)
        time.sleep(0.000002)
        GPIO.output(trigPin, True)
        time.sleep(0.00001)
        GPIO.output(trigPin, False)
 
        distance = (pulseIn(echoPin, 500) * 17150) - 6
        distance = 0 if distance <= 0 else distance
 
        ###################################### Opencv Camera Code -> CONTOURS
        
        ret, img = video.read();
        if ret == True:
            
            (r, g, b) = (0, 200, 100) if distance <= 1  else (255, 0, 0)
     
            (height, width) = img.shape[:2]
            cv2.circle(img, (width//2, height//2), 50, (b, g, r), 2)
            cv2.line(img, (width//2-50, height//2), (width//2+50, height//2), (b, g, r), 2)
            cv2.line(img, (width//2, height//2-50), (width//2,height//2+50), (b, g, r), 2)
            cv2.putText(img, "Distance: {0}cm".format(int(distance)), (width//2-110, height-20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255), 2)
            
            frame = cv2.imencode(".jpg", img)[1].tobytes()
            yield (b"--frame\r\n"b"Content-type: image/jpeg\r\n\r\n" + frame + b"\r\n")
            
        else:
            break
 
# video src without contours using OpenCV
def video_stream():
    global distance
    while True:
        
        ###################################### Ultrasonic Sensor Code
        GPIO.output(trigPin, False)
        time.sleep(0.000002)
        GPIO.output(trigPin, True)
        time.sleep(0.00001)
        GPIO.output(trigPin, False)
 
        distance = pulseIn(echoPin, 500) * 17150
        
        ###################################### Opencv Camera Code
        
        ret, img = video.read();
        if ret == True:
            
            frame = cv2.imencode(".jpg", img)[1].tobytes()
            yield (b"--frame\r\n"b"Content-type: image/jpeg\r\n\r\n" + frame + b"\r\n")
            
        else:
            break
 
# render the HTML webpage
@app.route("/")
def index():
    return render_template("index.html")
 
# convert distance to json value and send
@app.route("/_getDist", methods=['GET'])
def getDist():
    return jsonify(d=distance)
 
# return image src for video with contours
@app.route("/video_feed_contours")
def video_feed_contours():
    return Response(video_stream_contours(), mimetype="multipart/x-mixed-replace; boundary=frame")
 
# return image src for video
@app.route("/video_feed")
def video_feed():
    return Response(video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")
 
# main() to keep with convention
def main():
    app.run(host="0.0.0.0", port="5000", threaded=True, debug=False)
    GPIO.cleanup()
    video.release()
    cv2.destroyAllWindows()
 
# python coding convention
if __name__ == "__main__":
    main();
    pass;
