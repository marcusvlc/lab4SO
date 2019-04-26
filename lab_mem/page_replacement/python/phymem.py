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
    if (algorithm == 'aging'):
      self.chosenAlgorithm = Aging(self.ALGORITHM_AGING_NBITS)
    elif (algorithm == 'fifo'):
      pass
      #self.chosenAlgorithm = Fifo()
    elif (algorithm == 'nru'):
      pass
      #self.chosenAlgorithm = Nru()
    elif (algorithm == 'second-chance'):
      pass
      #self.chosenAlgorithm = SecondChance()
    elif (algorithm == 'lru'):
      pass
      #self.chosenAlgorithm = Lru()

  def put(self, frameId):
    """Allocates this frameId for some page"""
    # Notice that in the physical memory we don't care about the pageId, we only
    # care about the fact we were requested to allocate a certain frameId
    self.chosenAlgorithm.put(frameId)

  def evict(self):
    """Deallocates a frame from the physical memory and returns its frameId"""
    # You may assume the physical memory is FULL so we need space!
    # Your code must decide which frame to return, according to the algorithm
    self.chosenAlgorithm.evict()

  def clock(self):
    """The amount of time we set for the clock has passed, so this is called"""
    # Clear the reference bits (and/or whatever else you think you must do...)
    self.chosenAlgorithm.clock()

  def access(self, frameId, isWrite):
    """A frameId was accessed for read/write (if write, isWrite=True)"""
    self.chosenAlgorithm.access(frameId,isWrite)

class Aging:
    def __init__(self, nbits):
      self.pageTable = [] # Iniciando uma tabela de páginas vazia
      self.ALGORITHM_AGING_NBITS = nbits

    def put(self, frameId):
      self.pageTable.append([frameId,0]) # Toda página inicia com um contador de valor 0

    def evict(self):
      smallerFrame = self.pageTable[0] 
      smallerCounter = smallerFrame[1]

      for frame in self.pageTable: # Varre a tabela de páginas em busca da página com menor contador
        if frame[1] < smallerCounter:
          smallerCounter = frame[1]
          smallerFrame = frame

      self.pageTable.remove(smallerFrame) # Remove a página com menor contador
      return smallerFrame[0] # Retorna o ID da página removida

    def clock(self):
      pass

    def access(self,frameId,isWrite):
      pass