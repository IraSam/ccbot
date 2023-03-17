from enum import Enum

import pytest

from database.tables import MariaDBTable, MariaDBTablesManager, DatabaseLinkException


class TableNames(Enum):
    TestTableName = 1
    TestTableNameNotRegistered = 2
    TestTableForNormalization = 3


@pytest.fixture(scope='session')
def mariadb_manager():
    class TestTable(MariaDBTable):
        name = TableNames.TestTableName
        columns = ['colA', 'colB']

    class TestTable2(MariaDBTable):
        name = TableNames.TestTableForNormalization
        columns = ['colC', 'colD']

    mdb_manager = MariaDBTablesManager()
    mdb_manager.register_table(TestTable())
    mdb_manager.register_table(TestTable2())
    mdb_manager.register_links(TableNames.TestTableName, 'colA', TableNames.TestTableForNormalization, 'colC')
    mdb_manager.register_links(TableNames.TestTableName, 'colB', TableNames.TestTableForNormalization, 'colD')
    return mdb_manager


def test_table_added(mariadb_manager):
    assert mariadb_manager.is_valid_table(TableNames.TestTableName)


def test_table_not_present(mariadb_manager):
    assert not mariadb_manager.is_valid_table(TableNames.TestTableNameNotRegistered)


def test_tables_columns(mariadb_manager):
    assert mariadb_manager.table_column_names(TableNames.TestTableName) == ['colA', 'colB']


def test_needs_normalize(mariadb_manager):
    assert mariadb_manager.needs_normalize(TableNames.TestTableName)
    assert not mariadb_manager.needs_normalize(TableNames.TestTableForNormalization)


def test_tables_normalizing(mariadb_manager):
    assert mariadb_manager.normalizing_details(TableNames.TestTableName) == [
        ('colA', TableNames.TestTableForNormalization, 'colC'),
        ('colB', TableNames.TestTableForNormalization, 'colD')]


def test_tables_link_throws_col(mariadb_manager):
    with pytest.raises(DatabaseLinkException):
        mariadb_manager.register_links(TableNames.TestTableName, 'colNotExists',
                                       TableNames.TestTableForNormalization, 'colC')


def test_tables_link_throws_table(mariadb_manager):
    with pytest.raises(DatabaseLinkException):
        mariadb_manager.register_links(TableNames.TestTableNameNotRegistered, 'colA',
                                       TableNames.TestTableForNormalization, 'colC')


if __name__ == '__main__':
    pytest.main()
