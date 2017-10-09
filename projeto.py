#!/usr/bin/env python
# -*- coding: utf-8 -*-
# USAGE
# python compare.py

# import the necessary packages
import skimage.measure
import os
import io
import matplotlib.pyplot as plt
import numpy as np
import cv2

camera = ""
def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def comparar(imageA, imageB):
	valor_mse = mse(imageA, imageB)
	valor_ssim = skimage.measure.compare_ssim(imageA, imageB)
	print("mse: %.2f \t ssim:%0.2f" % (valor_mse, valor_ssim))
	if(valor_mse<400 and valor_ssim > 0.7):
		return True
	else:
		return False
def get_image():
	global camera
 	# read is the easiest way to get a full image out of a VideoCapture object.
 	retval, im = camera.read()
 	return im

def tirar_foto(ramp_frames = 30):
	global camera
	# Camera 0 is the integrated web cam on my netbook
	camera_port = 0
	#Number of frames to throw away while the camera adjusts to light levels
	# Now we can initialize the camera capture object with the cv2.VideoCapture class.
	# All it needs is the index to a camera port.
	camera = cv2.VideoCapture(camera_port)
	# Captures a single image from the camera and returns it in PIL format
	# Ramp the camera - these frames will be discarded and are only used to allow v4l2
	# to adjust light levels, if necessary
	for i in xrange(ramp_frames):
	 temp = get_image()
	print("Tirando foto...")
	# Take the actual image we want to keep
	camera_capture = get_image()
	file = "atual.png"
	# A nice feature of the imwrite method is that it will automatically choose the
	# correct format based on the file extension you provide. Convenient!
	#cv2.imwrite(file, camera_capture)
	# You'll want to release the camera, otherwise you won't be able to create a new
	# capture object until your script exits
	del(camera)
	return camera_capture

def run_quickstart():
	# [START vision_quickstart]
	# Imports the Google Cloud client library
	# [START migration_import]
	from google.cloud import vision
	from google.cloud.vision import types
	# [END migration_import]
	# Instantiates a client
	# [START migration_client]
	client = vision.ImageAnnotatorClient()
	# [END migration_client]
	# The name of the image file to annotate
	file_name = os.path.join(os.path.dirname(__file__), 'atual.jpg')

	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()

	image = types.Image(content=content)

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations

	print('Labels:')
	for label in labels:
		print(label.description)
		print(label.score)
	# [END vision_quickstart]

if __name__ == "__main__":
	print("Capturando base:")
	base = tirar_foto(50)
	basegray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
	atual = tirar_foto(30)
	atualgray = cv2.cvtColor(atual, cv2.COLOR_BGR2GRAY)
	while 1:
		antiga = atual
		antigagray = atualgray
		atual = tirar_foto(30)
		atualgray = cv2.cvtColor(atual, cv2.COLOR_BGR2GRAY)
		print("Comparando foto com a base:")
		if(not comparar(basegray, atualgray)):
			print("Comparando a foto com a última:")
			if(comparar(atualgray,antigagray)):
				cv2.imwrite("atual.jpg", atual)
				print("ENVIA PRO WATSUM")
				run_quickstart()

			else:
				print("NA PRÓXIMA EU ENVIO")
		else:
			print("NÃO MEXEU!")
