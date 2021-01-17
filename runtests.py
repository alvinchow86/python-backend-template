#!/usr/bin/env python
import argparse
import os
import sys

import pytest


def main():
    os.environ['APP_ENV'] = 'testing'

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--debug-level', default='info', choices=('debug', 'info', 'warning', 'error'))
    parser.add_argument('--coverage', action='store_true', default=False)
    parser.add_argument('--coverage-html', '--cov-html', action='store_true', default=False)

    args, pytest_args = parser.parse_known_args()

    use_coverage = args.coverage or args.coverage_html

    if use_coverage:
        pytest_args.extend(['--cov', 'alvinchow_backend'])

        if args.coverage_html:
            pytest_args.extend(['--cov-report', 'html', '--cov-report', 'term'])

    print('--> Calling pytest with args: {}'.format(' '.join(pytest_args)))
    status = pytest.main(pytest_args)
    sys.exit(status)


if __name__ == '__main__':
    main()
