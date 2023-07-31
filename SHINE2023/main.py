import time
from src import src
from flask import Flask, render_template, Response, stream_with_context, request, jsonify

app = Flask(__name__)
utils = src.basicOP(3, 5, 74, 0, 0, 0, 0)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/_getDist", methods=['GET'])
def getDist():
	return jsonify(d=utils.distance)

@app.route("/video_feed_contours")
def video_feed_contours():
	return Response(utils.video_stream_contours(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/video_feed")
def video_feed():
	return Response(utils.video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
	time.sleep(0.1)
	app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
	app.run(host="192.168.99.144", port="5000", threaded=True, debug=False)
