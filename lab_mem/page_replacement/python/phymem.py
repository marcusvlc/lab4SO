# coding: UTF-8
# This is the only file you must implement

# This file will be imported from the main code. The PhysicalMemory class
# will be instantiated with the algorithm received from the input. You may edit
# this file as you which

# NOTE: there may be methods you don't need to modify, you must decide what
# you need...

class PhysicalMemory:
  ALGORITHM_AGING_NBITS = 8
  """How many bits to use for the Aging algorithm"""

  def __init__(self, algorithm):
    assert algorithm in {"fifo", "nru", "aging", "second-chance","lru"}
    self.algorithm = algorithm
    self.strategy = Aging(self.ALGORITHM_AGING_NBITS)
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
    self.strategy.evict()

  def clock(self):
    """The amount of time we set for the clock has passed, so this is called"""
    # Clear the reference bits (and/or whatever else you think you must do...)
    self.strategy.clock()

  def access(self, frameId, isWrite):
    """A frameId was accessed for read/write (if write, isWrite=True)"""
    self.strategy.access(frameId,isWrite)

class Aging:
    def __init__(self, nbits):
      self.allocatedFrames = [] # Iniciando uma tabela de páginas vazia
      self.ALGORITHM_AGING_NBITS = nbits

    def put(self, frameId):
      self.allocatedFrames.append([frameId,0]) # Toda página inicia com um contador de valor 0

    def evict(self):
      smallerFrame = self.allocatedFrames[0] 
      smallerCounter = smallerFrame[1]

      for frame in self.allocatedFrames: # Varre a tabela de páginas em busca da página com menor contador
        if frame[1] < smallerCounter:
          smallerCounter = frame[1]
          smallerFrame = frame
         
      self.allocatedFrames.remove(smallerFrame) # Remove a página com menor contador
      return smallerFrame[0] # Retorna o ID da página removida

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