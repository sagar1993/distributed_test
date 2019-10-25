import abc
from subprocess import Popen, PIPE

BLINK_PATH = '~/thoughtspot/blink'


def setup_vnc_server():
    run('vncserver')
    run('export DISPLAY=:0')


def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line


class WorkerStatus(object):
    EXECUTING = 0
    EXECUTING_FINISHED = 1
    IDLE = 2
    DEAD = 3


class Worker(object):

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def assign_task(self):
        pass

    @abc.abstractmethod
    def update_task(self):
        pass

    @abc.abstractmethod
    def get_status(self):
        pass


class WorkerProcess(Worker):

    current_task = None

    def __init__(self, string_id, ip, username, password):
        self.string_id = string_id
        self.ip = ip
        self.status = WorkerStatus.IDLE
        self.username = username
        self.password = password
        # shared location

        # perform setup

    def setup(self):
        # check cluster status
        # tscli cluster status
        # if cluster is down change worker status to dead and return

        # Perform the setup required to perform the task
        # clean the environment for previous runs
        self.clean_environment()
        print('setting up environment for ' + self.string_id)

        # create required folder structure
        self.create_log_directory()
        pass

    def execute(self):
        # if the worker has an assigned task execute the task
        if not self.task:
            print('the worker ' + self.string_id + ' does not have any assigned task.')
        if self.status in [WorkerStatus.EXECUTING_FINISHED, WorkerStatus.IDLE]:
            self.status = WorkerStatus.EXECUTING
        else:
            pass

    def clean_environment(self):
        pass

    def create_log_directory(self):
        pass

    def assign_task(self, task):
        self.current_task = task
        pass

    def update_task(self, task):
        # can update task ?
        self.current_task = task
        pass

    def get_status(self):
        return self.status

    def is_success_file_exists(self, shard_number):
        pass

## stages
# 1. setup the vnc server