from enum import Enum

import pytest

from database.tables import MariaDBTable, MariaDBTablesManager


class TableNames(Enum):
    TestTableName = 1
    TestTableNameNotRegistered = 2


@pytest.fixture(scope='session')
def mariadb_manager():
    class TestTable(MariaDBTable):
        name = TableNames.TestTableName
        columns = ['colA', 'colB']

    mdb_manager = MariaDBTablesManager()
    mdb_manager.register_table(TestTable())
    return mdb_manager


def test_table_added(mariadb_manager):
    assert mariadb_manager.is_valid_table(TableNames.TestTableName)


def test_table_not_present(mariadb_manager):
    assert not mariadb_manager.is_valid_table(TableNames.TestTableNameNotRegistered)


if __name__ == '__main__':
    pytest.main()
