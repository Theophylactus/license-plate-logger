import cv2
import json
import time
import os
from openalpr import Alpr
from datetime import datetime

lastPlate = ""

def logPlate(plate, confidence):
	global lastPlate

	if lastPlate == plate:
		return

	now = datetime.now()
	formatted = now.strftime("%d/%m/%Y %H:%M:%S")

	message = "[" + formatted + "] " + plate + " (" + str(confidence) + "%)\n"
	print(message, end = '')
	
	dirname = os.path.dirname(__file__)
	filename = os.path.join(dirname, 'matriculas.txt')

	with open(filename, 'a') as platesLog:
		platesLog.write(message)

	lastPlate = plate
	

cap = cv2.VideoCapture(0)
alpr = Alpr('eu', '/etc/openalpr/openalpr.conf', '/usr/share/openalpr/runtime_data')

if not alpr.is_loaded():
	print("Error loading OpenALPR")
	sys.exit(1)

while True:
	ret, frame = cap.read()
	ret, enc = cv2.imencode("*.bmp", frame)
	results = alpr.recognize_array(bytes(bytearray(enc)))

	if len(results['results']) > 0:
		if results['results'][0]['confidence'] >= 90:
			logPlate(results['results'][0]['plate'], results['results'][0]['confidence'])
	#else:
		#print("Nothing found.")

	# Save some resources
	time.sleep(0.10)

alpr.unload()
cap.release()
