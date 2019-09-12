from abc import ABCMeta, abstractmethod

class Analyzer(metaclass=ABCMeta):

    @abstractmethod
    def analyze(self):
        pass
