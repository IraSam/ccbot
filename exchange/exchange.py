from abc import ABC, abstractmethod


class Exchange(ABC):
    @abstractmethod
    def get_pairs_universe(self):
        pass

    @abstractmethod
    def retrieve_market_data_all_universe(self, freq: str):
        pass
