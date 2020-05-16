import pytest

from alvinchow_service import app
from alvinchow_service.db import base
from alvinchow_service.db.session import get_session
from alvinchow_service.app import config
from alvinchow_service.lib.redis import get_redis_connection


app.initialize()


def pytest_addoption(parser):
    parser.addoption(
        '--integration', action="store_true", default=False, help="Also run the integration tests"
    )


@pytest.yield_fixture(autouse=True)
def common():
    """
    Run this for all tests
    """
    conn = get_redis_connection()
    yield

    # This is cheap enough to do that we can just do it for all tests
    conn.flushdb()


def pytest_runtest_setup(item):
    # Skip integration tests by default
    allow_integration_tests = item.config.getoption("integration")
    if item.get_closest_marker('integration') and not allow_integration_tests:
        pytest.skip("integration test requires --integration option")


@pytest.fixture(autouse=True)
def socket_check(request):
    """
    Block socket cipfalls unless integration test
    """
    is_integration_test = request.node.get_closest_marker('integration')
    if not is_integration_test:
        # dynamically inject fixture
        request.getfixturevalue('socket_disabled')


@pytest.fixture(scope='session')
def testdatabase(testdatabase_factory):
    _testdatabase = testdatabase_factory(base, config.DATABASE_URL)
    yield from _testdatabase


@pytest.yield_fixture(scope='function')
def db(testdatabase):
    connection = testdatabase['connection']
    session = testdatabase['session']

    # Start a transaction for the test
    transaction = connection.begin()
    session.begin_nested()

    yield

    base.Session.remove()
    transaction.rollback()


@pytest.fixture
def session(db):
    return get_session()


@pytest.fixture(name='config')
def config_override():
    """ Write to app.config in tests safely """
    orig_values = config._values

    yield config

    for k, v in orig_values.items():
        setattr(config, k, v)
    config._values = orig_values
