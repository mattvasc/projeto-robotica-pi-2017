#!/usr/bin/env python
# -*- coding: utf-8 -*-
# USAGE
# python projeto.py

# import the necessary packages
import skimage.measure
import os
import io
import matplotlib.pyplot as plt
import numpy as np
import cv2
from google.cloud import vision
from google.cloud.vision import types
import json
import sys
import datetime
import pygame
import pygame.camera
# import serial

# ser = serial.Serial('/dev/ttyACM0')
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
	retval,im = camera.read()
	return im

def tirar_foto(ramp_frames = 5):
	global camera
	camera = cv2.VideoCapture(camera_port)
	for i in range(ramp_frames):
		get_image()
	print("Tirando foto...")
	pygame.mixer.music.load("camera.mp3")
	pygame.mixer.music.play()
	camera_capture = get_image()
	del(camera)
	return camera_capture

def enviar_para_googlevision():

	# [START migration_client]
	client = vision.ImageAnnotatorClient()
	# [END migration_client]

	# The name of the image file to annotate
	file_name = os.path.join(os.path.dirname(__file__), 'atual.png')

	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()

	image = types.Image(content=content)

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations

	return labels
	# print('Labels:')
	# for label in labels:
	# 	print(label.description)
	# 	print(label.score)

def separar_material(labels):

	banco = open("banco.txt", "a")

	for l in labels:
		# print(l)

		banco.write(l.description + " " + str(l.score) + "\n")
		reconheceu = False

		if l.description in database['PAPER']:
			reconheceu = True
			print("PAPEL!")
			# ser.write('1')
			break
		elif l.description in database['PLASTIC']:
			reconheceu = True
			print("PLASTICO!")
			# ser.write('2')
			break
		elif l.description in database['METAL']:
			reconheceu = True
			print("METAL!")
			# ser.write('3')
			break
		elif l.description in database['GLASS']:
			reconheceu = True
			print("VIDRO!")
			# ser.write('4')
			break
		elif l.description in database['ORGANIC']:
			reconheceu = True
			print("ORGANICO!")
			# ser.write('5')
			break

	if not reconheceu:
		print("Não reconhecemos o objeto atual")
		now = datetime.datetime.now()
		nome_arquivo = "nreconhecido_" + str(now.hour) + "_" + str(now.minute) + ".png"
		os.rename("atual.png", nome_arquivo)
		print("Salvamos a imagem não reconhecida como " + nome_arquivo)
		img = cv2.imread(nome_arquivo, 1)
		cv2.imshow('Imagem nao reconhecida - hit any key to exit', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		resposta = raw_input("Gostaria de adicionar a classificação desse objeto para algum material? (s/n) ")

		while resposta != "s" and resposta != "n":
			print("Desculpa, não entendi, vamos tentar novamente")
			resposta = raw_input("Gostaria de adicionar a classificação desse objeto para algum material? (s/n) ")

		if(resposta=="s"):
			print("A qual material o objeto pertence?")
			resposta = raw_input("1 - Papel\n2 - Plástico\n3 - Metal\n4 - Vidro\n5 - Orgânico\n\nInforme a opção: ")

			while (resposta != "1" and resposta != "2" and resposta != "3" and resposta != "4" and resposta != "5") :
				print("Desculpa, não entendi, vamos tentar novamente")
				print("A qual material o objeto pertence?")
				resposta = raw_input("1 - Papel\n2 - Plástico\n3 - Metal\n4 - Vidro\n5 - Orgânico\n\nInforme a opção: ")
			
			if(resposta == "1"):
				selecionado = "PAPER"
			elif (resposta== "2"):
				selecionado = "PLASTIC"
			elif (resposta=="3"):
				selecionado = "METAL"
			elif (resposta == "4"):
				selecionado = "GLASS"
			else:
				selecionado = "ORGANIC"

			print("\nAgora precisamos que você selecione das tags retornadas,\nquais são importantes para a classificação!")
			print("\nPara cada tag, digite 's' para adicionar ao\nclassificador ou 'n' para ir a próxima.\n")
			
			for l in labels:
				resposta = raw_input("Deseja adicionar a categoria a tag: " +l.description+" (s/N): ")
				if(resposta.lower() == "s"  or resposta.lower() == "y"):
					database[selecionado].append(l.description)
			
			with open('DB.json', 'w') as outfile:
				json.dump(database, outfile, indent=2, sort_keys=True)

			print("\nPronto, tags adicionada a categoria com sucesso!")
				
		elif (resposta=="n"):
			print("Ok, então apagamos a imagem da pasta")
			os.unlink(nome_arquivo)

		print("Continuando a execução do programa!")
	banco.write("\n")
	banco.close()



if __name__ == "__main__":
	global camera_port
	print("Iniciando Módulos...")
	pygame.init()
	pygame.camera.init()
	print("Buscando câmeras disponíveis...")
	camlist = pygame.camera.list_cameras()
	camera_port = 0
	if( len(camlist) > 1):
		print("Temos as seguintes câmeras disponíveis:")
		print(camlist)
		camera_port = input("Digite o índice vetorial da qual deseja usar: ")
	camera_port = int(camera_port)

	with open('DB.json') as json_data:
		database = json.load(json_data)

	print("Capturando base:")
	
	base = tirar_foto()
	basegray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
	atual = tirar_foto()
	atualgray = cv2.cvtColor(atual, cv2.COLOR_BGR2GRAY)
	while 1:
		antiga = atual
		antigagray = atualgray
		atual = tirar_foto()
		atualgray = cv2.cvtColor(atual, cv2.COLOR_BGR2GRAY)
		print("Comparando foto com a base:")
		if(not comparar(basegray, atualgray)):
			print("Comparando a foto com a última:")
			if(comparar(atualgray,antigagray)):
				cv2.imwrite("atual.png", atual)
				print("ENVIANDO PARA O GOOGLE VISION...")
				labels = enviar_para_googlevision()
				separar_material(labels)

			else:
				print("NA PRÓXIMA EU ENVIO")
		else:
			print("NÃO MEXEU!")
