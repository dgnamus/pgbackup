from argparse import Action, ArgumentParser

class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        namespace.driver = driver.lower()
        namespace.destination = destination


def create_parser():
    parser = ArgumentParser(description="Backup postgresql locally or to aws s3")

    parser.add_argument("url", help="URL of the database to backup")
    parser.add_argument("--driver", "-d",
            help="how and where to store backup",
            nargs=2,
            metavar=("DRIVER", "DESTINATION"),
            action=DriverAction,
            required=True)

    return parser

def main():
    import boto3
    import time
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    if args.driver == 'remote':
        client = boto3.client('s3')
        timestamp = time.strftime("%Y-%m-%dT-%H:%M", time.localtime())
        file_name = pgdump.dump_file_name(args.url, timestamp)
        storage.remote(client, dump.stdout, args.destination, file_name)
    else:
        outfile = open(args.destination, 'wb')
        storage.local(dump.stdout, outfile)
