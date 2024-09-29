from abc import ABC, abstractmethod


class CardDriver(ABC):

    @abstractmethod
    def save():
        ...

    @abstractmethod
    def load():
        ...

    @abstractmethod
    def getCreators():
        ...

    @abstractmethod
    def getCreatorCards():
        ...