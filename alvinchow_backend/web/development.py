from flask import request, render_template, redirect

from alvinchow_backend.app import config
from alvinchow_backend.web import web
from alvinchow_backend.lib.web.decorators import login_required
from alvinchow_backend.lib.web.user import get_current_user, login_user
from alvinchow_backend.lib.web.exceptions import BadRequestError
from alvinchow_backend.service.authentication import authenticate_user_with_credentials, AuthenticationError


if not config.PRODUCTION:
    @web.route('/dev/login', methods=['GET', 'POST'])
    def login(email=None):
        user = get_current_user()

        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']

            try:
                user = authenticate_user_with_credentials(email, password)
            except AuthenticationError:
                raise BadRequestError('Incorrect credentials')
            login_user(user)

            return redirect('/dev/home')

        return render_template('login.html', user=user)

    @web.route('/dev/home', methods=['GET'])
    @login_required
    def home():
        user = get_current_user()
        return render_template('home.html', user=user)
