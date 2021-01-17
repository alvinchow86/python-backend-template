import pytest

from alvinchow_backend.test.factory import make_user
from alvinchow_backend.service.authentication.login import authenticate_user_with_credentials
from alvinchow_backend.service.authentication.exceptions import AuthenticationError


pytestmark = pytest.mark.usefixtures('db')


def test_login_flow():
    email = 'user1@alvinchow.com'
    password = 'alvintester'
    user = make_user(email, password)

    with pytest.raises(AuthenticationError):
        authenticate_user_with_credentials(email, 'badpw')

    user = authenticate_user_with_credentials(email, password)
    assert user == user
