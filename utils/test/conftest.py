import os


def pytest_generate_tests(metafunc):
    os.environ['db_port'] = '3306'
    os.environ['db_user'] = 'my_username'
    os.environ['db_pwd'] = 'my_pwd'
