import os


def pytest_generate_tests(metafunc):
    os.environ['database_port'] = '3306'
    os.environ['database_user'] = 'my_username'
    os.environ['database_pwd'] = 'my_pwd'
