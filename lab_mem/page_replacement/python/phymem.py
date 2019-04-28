# coding: UTF-8
# This is the only file you must implement

# This file will be imported from the main code. The PhysicalMemory class
# will be instantiated with the algorithm received from the input. You may edit
# this file as you which

# NOTE: there may be methods you don't need to modify, you must decide what
# you need...
from random import randint

class PhysicalMemory:
  ALGORITHM_AGING_NBITS = 8
  """How many bits to use for the Aging algorithm"""

  def __init__(self, algorithm):
    assert algorithm in {"fifo", "nru", "aging", "second-chance","lru"}
    self.algorithm = algorithm
    self.strategy = Nru()
    '''
    if (algorithm == "aging"):
      self.strategy = Aging(self.ALGORITHM_AGING_NBITS)
    elif (algorithm == "fifo"):
      pass
      #self.strategy = Fifo()
    elif (algorithm == "nru"):
      pass
      #self.strategy = Nru()
    elif (algorithm == "second-chance"):
      pass
      #self.strategy = SecondChance()
    elif (algorithm == "lru"):
      pass
      #self.strategy = Lru()
      '''

  def put(self, frameId):
    """Allocates this frameId for some page"""
    # Notice that in the physical memory we don't care about the pageId, we only
    # care about the fact we were requested to allocate a certain frameId
    self.strategy.put(frameId)

  def evict(self):
    """Deallocates a frame from the physical memory and returns its frameId"""
    # You may assume the physical memory is FULL so we need space!
    # Your code must decide which frame to return, according to the algorithm
    return self.strategy.evict()

  def clock(self):
    """The amount of time we set for the clock has passed, so this is called"""
    # Clear the reference bits (and/or whatever else you think you must do...)
    self.strategy.clock()

  def access(self, frameId, isWrite):
    """A frameId was accessed for read/write (if write, isWrite=True)"""
    self.strategy.access(frameId,isWrite)

class Nru:

  def __init__(self):
    self.allocatedFrames = {} ## Iniciando uma tabela de paginas vazia. Key = FrameID / Value = Valores dos bits
    self.POS_REFERENCE_BIT = 0 # Indice do array de bits que se encontra o bit de referencia
    self.POS_MODIFY_BIT = 1 # Indice do array de bits que se encontra o bit de modificacao
    self.INIT_REFERENCE_BIT = 0 ## Valor inicial do bit de referencia
    self.INIT_MODIFY_BIT = 0 ## Valor inicial do bit de modificacao
  
  def put(self, frameId):
    self.allocatedFrames[frameId] = [self.INIT_REFERENCE_BIT,self.INIT_MODIFY_BIT] # Coloca no dicionario de paginas um item cuja key eh o frameID e seu valor eh um array com os valores dos bits

  def evict(self):
    classes = {0:[0,0], 1:[0,1], 2:[1,0], 3:[1,1]} ## Dicionario com classes existentes no NRU
    actual_class = 0 ## Classe inicial para procurar alguem para desalocar
    deleted_frame = -1 ## Variavel que guarda o valor de retorno do elemento desalocado

    while(actual_class <= 3): ## Enquanto a classe for valida (entre 0 e 3)
      frames_from_class = [] ## Array para guardar todos os framesIDs da classe atual

      for key, value in self.allocatedFrames.items(): ## Itera sobre o dicionario de frames procurando os frameIDS da classe atual
        if(value == classes[actual_class]):
          frames_from_class.append(key)
      
      if(len(frames_from_class) > 0): ## Se tiver alguem daquela classe
        pos_to_kill = randint(0, len(frames_from_class)-1) ## Pega alguma pagina aleatoria daquela classe 
        deleted_frame = frames_from_class[pos_to_kill] ## Guarda o selecionado para retorno
        del self.allocatedFrames[frames_from_class[pos_to_kill]] ## Deleta o selecionado do dicionario de paginas
        break ## Obrigatoriamente sai do loop caso ache alguem
      
      actual_class += 1 ## Se nao tiver ninguem daquela classe, seguir adiante para a proxima


    return deleted_frame

  def clock(self):
    for _, value in self.allocatedFrames.items():
      value[self.POS_REFERENCE_BIT] = 0 # Colocando todos os bits de referencia como 0 a cada interrupcao de relogio


  def access(self, frameId, isWrite):
    if(frameId in self.allocatedFrames.keys()): ## Verifica se o frameID passado esta no dicionario de frames
      if(isWrite): 
        self.allocatedFrames[frameId] = [1,1] ## Se a op for de escrita, mudar os 2 bits (vira classe 3)
      else:
        self.allocatedFrames[frameId][self.POS_REFERENCE_BIT] = 1 ## Se nao for, mudar apenas o bit de referencia (vira classe 2)
    else:
      pass ## Se o frameID nao estiver, nao faz nada.

class Lru:
    def __init__(self):
      self.allocatedFrames = [] # Iniciando uma tabela de páginas vazia
      self.timer = 0

    def put(self, frameId):
      self.timer = self.timer + 1
      self.allocatedFrames.append([frameId,self.timer]) # Coloca na tabela de páginas a página e o tempo que foi acessada

    def evict(self): # Procura a página com tempo menor (menos utilizada) e remove
      if(len(self.allocatedFrames) > 0):
        smallerFrame = self.allocatedFrames[0]
        smallerTime = smallerFrame[1]
        for frame in self.allocatedFrames:
          if frame[1] < smallerTime:
            smallerTime = frame[1]
            smallerFrame = frame

        print("Smaller frame: ", smallerFrame)
        self.allocatedFrames.remove(smallerFrame)
        return int(smallerFrame[0])
      return -1

    def clock(self):
      pass
    
    def access(self, frameId, isWrite): # Atuaiza o tempo que a página foi acessada
      self.timer = self.timer + 1
      for frame in self.allocatedFrames:
        if frame[0] == frameId:
          self.allocatedFrames.remove(frame)
          self.allocatedFrames.append([frameId,self.timer])
          print("New pages: ")
          print(self.allocatedFrames)
          print("---------")

class Aging:
    def __init__(self, nbits):
      self.allocatedFrames = [] # Iniciando uma tabela de páginas vazia
      self.ALGORITHM_AGING_NBITS = nbits

    def put(self, frameId):
      self.allocatedFrames.append([frameId,0]) # Toda página inicia com um contador de valor 0

    def evict(self):
      if(len(self.allocatedFrames) > 0):
        smallerFrame = self.allocatedFrames[0] 
        smallerCounter = smallerFrame[1]

        for frame in self.allocatedFrames: # Varre a tabela de páginas em busca da página com menor contador
          if frame[1] < smallerCounter:
            smallerCounter = frame[1]
            smallerFrame = frame
          
        self.allocatedFrames.remove(smallerFrame) # Remove a página com menor contador

        print("New pages: ")
        print(self.allocatedFrames)
        print("---------")

        return int(smallerFrame[0]) # Retorna o ID da página removida

      return -1

    def clock(self):
      # A cada interrupção de clock, os contadores são deslocados à direita em um bit.
      for frame in self.allocatedFrames:
        frame[1] >>= 1 # Bits são movidos uma casa para a direita
      

    def access(self,frameId,isWrite):
      # Tem que aparecer um 1 no bit mais significativo (mais a esquerda)
      for frame in self.allocatedFrames:
        if(frameId == frame[0]): # Procura a página na tabela de páginas
          frame[1] |= 1 << (self.ALGORITHM_AGING_NBITS - 1) # Coloca 1 no bit mais significativo, aumentando assim o contador

class Fifo:
    def __init__(self):
      from Queue import Queue
      self.queue = Queue() # Inicializando fila vazia

    def put(self, frameId):
      self.queue.put(frameId) # Adicionando página no final

    def evict(self):
      return self.queue.get() # Removendo página do início
          
    def clock(self): # Não usa
      pass

    def access(self,frameId,isWrite): # Se a página for usada. O bit é setado para 1
      pass

class SecondChance:
    def __init__(self):
      from Queue import Queue
      self.queue = Queue() # Inicializando fila vazia

    def put(self, frameId):
      self.queue.put([frameId, 0]) # Adicionando página com bit 0

    def evict(self):
      
      while True:
        head = self.queue.get() 
        
        if node[1] == 1 : # Se a página tiver bit 1, significa que ela é velha e usada recentemente. Assim ela ganha uma nova chance como uma página nova         
          head[1] = 0
          self.queue.put(head)
        else: # Se a página tiver bit 0, significa que ela é velha e não foi usada recentemente. Assim ela é removida
          return head[0]
          
    def clock(self): # Não usa
      pass

    def access(self,frameId,isWrite): # Se a página for usada. O bit é setado para 1
      for node in self.queue:
        if(frameId == node[0]):
          node[1] = 1