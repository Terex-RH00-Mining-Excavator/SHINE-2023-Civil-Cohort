import cv2
import time
import RPi.GPIO as GPIO

def pulseIn(pin, timeout=1000):
	
	pulseStart, timeStart = 0, time.time()*1000;
	
	while GPIO.input(pin) == False:
		if(time.time()*1000 - timeStart > timeout):
			return 0
	pulseStart = time.time()
	
	while GPIO.input(pin) == True:
		if(time.time()*1000 - timeStart > timeout):
			return 0
	
	return (time.time() - pulseStart)

class basicOP:
	def __init__(self, TP, EP, D, R, G, B, VALUE):
		self.trigPin 		= TP
		self.echoPin 		= EP
		self.distance 		= D
		self.red 		= R
		self.green 		= G
		self.blue 		= B
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.trigPin, GPIO.OUT)
		GPIO.setup(self.echoPin, GPIO.IN)
		self.video = cv2.VideoCapture(VALUE)
	def getDistance(self, timeout=500):
		GPIO.output(self.trigPin, False)
		time.sleep(0.000002)
		GPIO.output(self.trigPin, True)
		time.sleep(0.00001)
		GPIO.output(self.trigPin, False)
		
		#self.distance = pulseIn(self.echoPin, timeout) * 171500
		self.distance = randint(0, 100)
		
		
		return self.distance
	def video_stream_contours(self):
		
		while True:
			
			self.getDistance();
			
			ret, img = self.video.read();
			if ret == True:
				
				(self.red, self.green, self.blue) = (0, 200, 100) if self.distance <= 6  else (255, 0, 0)
		 
				(height, width) = img.shape[:2]
				cv2.circle(img, (width//2, height//2), 50, (self.blue, self.green, self.red), 2)
				cv2.line(img, (width//2-50, height//2), (width//2+50, height//2), (self.blue, self.green, self.red), 2)
				cv2.line(img, (width//2, height//2-50), (width//2,height//2+50), (self.blue, self.green, self.red), 2)
				cv2.putText(img, "Distance: {0}cm".format(int(self.distance)), (width//2-110, height-20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255), 2)
				
				frame = cv2.imencode(".jpg", img)[1].tobytes()
				yield (b"--frame\r\n"b"Content-type: image/jpeg\r\n\r\n" + frame + b"\r\n")
				
			else:
				break
	def video_stream(self):
		
		while True:
			
			self.getDistance();
			
			ret, img = self.video.read();
			if ret == True:
				
				frame = cv2.imencode(".jpg", img)[1].tobytes()
				yield (b"--frame\r\n"b"Content-type: image/jpeg\r\n\r\n" + frame + b"\r\n")
				
			else:
				break
	def __del__(self):
		GPIO.cleanup()
		self.video.release()
		cv2.destroyAllWindows()
