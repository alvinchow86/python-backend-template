import pytest

from alvinchow_backend import app
from alvinchow_backend.db import base
from alvinchow_backend.db.session import get_session
from alvinchow_backend.app import config
from alvinchow_backend.lib.redis import get_redis_connection


app.initialize()


def pytest_addoption(parser):
    parser.addoption(
        '--integration', action="store_true", default=False, help="Also run the integration tests"
    )
    parser.addoption(
        '--integration-only', action="store_true", default=False, help="Only run the integration tests"
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
    run_integration_only = item.config.getoption("integration_only")

    is_integration_test = item.get_closest_marker('integration')

    if is_integration_test and not (allow_integration_tests or run_integration_only):
        # Integration tests can run either when --integration or --integration-only
        pytest.skip()

    if not is_integration_test and run_integration_only:
        # Skip other tests --integration-only
        pytest.skip()


@pytest.fixture(scope='session')
def testdatabase(testdatabase_factory):
    # testdatabase_factory comes from alvin-python-lib
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


@pytest.fixture(autouse=True)
def fast_password_hashing(mocker, request):
    from passlib.context import CryptContext

    fast_crypt_context = CryptContext(schemes=['md5_crypt'])
    mocker.patch('alvinchow_backend.service.authentication.password.crypt_context', fast_crypt_context)


@pytest.fixture(autouse=True)
def default_mocks(
    request,
):
    """
    Do specific things for unit-tests vs integration tests
    - Block socket cipfalls unless integration test
    - Allow socket API calls
    """
    is_integration_test = bool(request.node.get_closest_marker('integration'))

    # dynamically inject fixtures
    if not is_integration_test:
        request.getfixturevalue('socket_disabled')
