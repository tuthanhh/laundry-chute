from abc import ABC, abstractmethod


class Bridge(ABC):
    def __init__(self, device_destination: str):
        self.device_destination = device_destination

    @abstractmethod
    def connect(self) -> bool: ...

    @abstractmethod
    def push_package(self, package_path: str) -> bool: ...
