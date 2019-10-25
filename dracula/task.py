import abc


class TaskStatus(object):
    SUCCESS = 0
    FAILURE = 1
    NONE = 3
    RUNNING = 4


class Task(object):

    @abc.abstractmethod
    def get_task_execution_command(self):
        pass

    @abc.abstractmethod
    def status(self):
        pass

    @abc.abstractmethod
    def update_status(self):
        pass


class TaskProcess(Task):
    def __init__(self, string_id, tests_to_run, tests_to_exclude, mode, timeout, attempt=1):
        self.string_id = string_id
        self.tests_to_run = tests_to_run
        self.tests_to_exclude = tests_to_exclude
        self.mode = mode
        self.timeout = timeout
        self.attempt = attempt

        self.status = TaskStatus.NONE
        print('created task: ' + string_id + 'to run '+ self.tests_to_run)

    def get_task_execution_command(self):
        # generate task execution command depending upon mode : test file or test
        #
        # this can use functions from test rig.
        return ''

    def status(self):
        return self.status

    def update_status(self, status):
        self.status = status
        print('task: ' + self.string_id + ' ' + self.status)
