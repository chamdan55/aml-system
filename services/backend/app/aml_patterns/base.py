from abc import ABC, abstractmethod
from typing import List
from services.common.schemas.transaction import Transaction

class AMLPattern(ABC):
    @abstractmethod
    def generate(self) -> List[Transaction]:
        pass
