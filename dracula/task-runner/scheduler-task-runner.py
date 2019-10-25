import click
import re
# TODO improve logging mechanism
from dracula.scheduler import Scheduler

pat = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')


@click.command()
@click.option('--worker_ips', required=True, help="IP's of distributed worker machines")
@click.option('--mode', default='FILE', help='Test Mode: 1. FILE 2. TEST')
@click.option('--test_to_include', help='test files to execute on worker machines.')
@click.option('--test_to_ignore', help='tests to ignore')
@click.option('--shared_location', required=True, help='nfs to share between scheduler and workers')
@click.option('--log_location', required=True, help='location for log')
@click.option('--timeout', default=600, help='timeout for worker in seconds')
@click.option('--username', default='admin', help='common username for all workers')
@click.option('--password', default='th0ughtSp0t', help='common password for all workers')
def main(
    worker_ips,
    mode,
    test_to_include,
    test_to_ignore,
    shared_location,
    log_location,
    timeout,
    username,
    password
):
    worker_ips_addresses = []
    for ip in worker_ips.split(','):
        address = ip.strip()
        if validate_ip(address):
            worker_ips_addresses.append(address)
    if not len(worker_ips_addresses):
        print('no valid ip provided')
        # TODO exit program

    test_mode = 0
    if mode.upper() in ['FILE', 'TEST']:
        test_mode = ['FILE', 'TEST'].index(mode.upper())

    # assumes that the test name do not have comma
    test_to_include = [test.strip() for test in test_to_include.split(',') if len(test)]
    if not len(test_to_include):
        print('no tests provided')
        # TODO exit program

    # assumes that the test name do not have comma
    if not test_to_ignore:
        print('no tests to ignore')
        test_to_ignore = []
    else:
        test_to_ignore = [test.strip() for test in test_to_ignore.split(',') if len(test)]

    shared_location = shared_location.strip()

    log_location = log_location.strip()

    scheduler = Scheduler(
        worker_ips = worker_ips_addresses,
        mode = test_mode,
        test_to_include = test_to_include,
        test_to_ignore = test_to_ignore,
        shared_location = shared_location,
        log_location = log_location,
        timeout = timeout,
        username= username,
        password = password
    )

    # first run
    scheduler.run_tasks()
    # wait till timeout
    scheduler.check_workers_for_completion_and_update()

    # retry for failed tasks
    scheduler.run_tasks()
    scheduler.check_workers_for_completion_and_update()

    # methods to track logs

    print(scheduler)


def validate_ip(ip):
    # validates ipv4 address
    if re.match(ip):
        return True
    return False


if __name__ == "__main__":
    main()
