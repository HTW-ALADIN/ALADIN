from abc import ABC, abstractmethod



class InputBase(ABC):
    
    @abstractmethod
    def find_pfad():
        pass
    
    @abstractmethod
    def ladeJson(self):
        pass

