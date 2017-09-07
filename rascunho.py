metal = list("can", "soda")
plastico = list("water bottle", "")
vidro = list("glass", "google")
papel = list("document","paper")
#adicionar mais a cima conforme objetos a serem usados de input


while 1:
  # temos que ver se vamos realizar isso através de um acionamento mecanico ou de proc de imagem.
  if verifica_se_tem_objeto_no_foco_da_camera == True:
    chama api enviando a imagem como parametro e espera por resposta
    acende um led ou apita um barulho avisando que recebeu resposta # opcional, firula
    consulta no json o item de maior probabilidade.
    if deu match na procura por esse item nos arrays de reciclaveis:
      aciona_mecanico_para_X
    else:
      pisca led ou emite som.
  else:
    blinka led ou beep.
    
