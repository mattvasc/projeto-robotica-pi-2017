import pygame
import pygame.camera

def tirar_foto(ramp_frames = 5):
	global cam
	cam.start()
	print("Tirando foto...")
	for i in range(5):
		cam.get_image()
	img = cam.get_image()
	cam.stop()
	return img

if __name__ == "__main__":	
	pygame.camera.init()
	camlist = pygame.camera.list_cameras()
	num = 0
	if( len(camlist) > 1):
		print("Temos as seguintes câmeras disponíveis:")
		print(camlist)
		num = input("Digite o índice vetorial da qual deseja usar: ")
	cam = pygame.camera.Camera(camlist[int(num)],(1280,720))
	print("Utilizando a câmera: " + camlist[0])
	img = tirar_foto()
	pygame.image.save(img,"filename.jpg")
	img = tirar_foto()
	pygame.image.save(img,"filename2.jpg")
	print("Salvei uma foto com o nome filename.jpg na pasta")