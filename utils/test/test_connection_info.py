from utils.connection_info import get_connection_details


def test_get_connection_details():
    assert get_connection_details('db') == {'name': 'db', 'port': '3306', 'user': 'my_username', 'pwd': 'my_pwd'}
