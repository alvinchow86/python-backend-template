#!/usr/bin/env python
import argparse

from alvinchow_backend.api.grpc import server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', dest='port', type=int)
    parser.add_argument('-a', '--address', dest='address')
    parser.add_argument('--workers', '--max-workers', dest='num_workers', type=int, default=8)

    args = parser.parse_args()
    port = args.port
    address = args.address
    num_workers = args.num_workers

    args = dict(
        num_workers=num_workers
    )
    if address:
        args.update(address=address)
    if port:
        args.update(port=port)

    server.serve(**args)


if __name__ == '__main__':
    main()
