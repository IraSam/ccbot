from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Tuple, Optional

from database.table_names import TableNames


class MariaDBTable(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def columns(self):
        pass


class DatabaseLinkException(Exception):
    def __init__(self, message="Database linking column exception"):
        self.message = message
        super().__init__(self.message)


class MariaDBTablesManager:
    __tables = {}
    __links = defaultdict(list)

    def register_table(self, cls: MariaDBTable) -> None:
        if cls.name in self.__tables:
            raise Exception(f'Table {cls.name} has already been registered')
        self.__tables[cls.name] = cls

    def register_links(self, from_table: TableNames, from_column: str, to_table: TableNames, to_column) -> None:
        if from_table not in self.__tables:
            raise DatabaseLinkException(f'{from_table} is not defined')
        if to_table not in self.__tables:
            raise DatabaseLinkException(f'{to_table} is not defined')
        if from_column not in self.__tables[from_table].columns:
            raise DatabaseLinkException(f'{from_column} does not exist in {from_table}')
        if to_column not in self.__tables[to_table].columns:
            raise DatabaseLinkException(f'{to_column} does not exist in {to_table}')
        self.__links[from_table].append((from_column, to_table, to_column))

    def is_valid_table(self, table_name: TableNames) -> bool:
        return table_name in self.__tables

    def needs_normalize(self, table_name: TableNames) -> bool:
        if not self.is_valid_table(table_name):
            raise Exception(f'Table {table_name} is not registered')
        return table_name in self.__links

    def normalizing_details(self, table_name: TableNames) -> Optional[List[Tuple[str, str, str]]]:
        if not self.needs_normalize(table_name):
            return None
        return self.__links[table_name]

    def table_column_names(self, table_name: TableNames) -> List[str]:
        if not self.is_valid_table(table_name):
            raise Exception(f'Table {table_name} is not registered')
        return self.__tables[table_name].columns
