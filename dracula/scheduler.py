import collections

from .task import TaskProcess
from .worker import WorkerProcess, WorkerStatus

WORKER_STRING = 'worker'
LOG_DIRECTORY = 'log'
TASK_STRING = 'task'


class TaskMode(object):
    FILE = 0
    TEST = 1


def get_worker_string(index):
    return WORKER_STRING + '-' + str(index)


def get_task_string(index):
    return TASK_STRING + '-' + str(index)


class Scheduler(object):

    def __init__(
            self,
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

        self.worker_ips = worker_ips
        self.mode = mode
        self.test_to_ignore = test_to_ignore
        self.test_to_include = test_to_include
        self.shared_location = shared_location
        self.log_location = log_location
        self.timeout = timeout
        self.task_queue = collections.deque([])
        self.username = username
        self.password = password

        self.worker_string_to_ip_map = {get_worker_string(index): ip for index, ip in enumerate(self.worker_ips)}
        self.ip_to_worker_string_map = {ip: worker_string for worker_string, ip in self.worker_to_ip_map}
        self.worker_string = self.worker_string_to_ip_map.keys()

        # create worker string to worker object map
        for worker_string, worker_ip in self.worker_string_to_ip_map:
            self.worker_string_to_worker_object_map[worker_string] = WorkerProcess(worker_string, worker_ip, self.username, self.password)

        ## create Task queue
        for index, test_file in enumerate(self.test_to_include):
            task_obj = TaskProcess(get_task_string(index), test_file, self.test_to_ignore, self.timeout)
            self.task_queue.append(task_obj)

    def create_folder_structure(self, count_shards):
        # the function to create folder structure on shared location.
        # TODO
        pass

    def run_tasks(self, test_to_include):
        # TODO
        while self.task_queue:
            task = self.task_queue.popleft()
            workers = self.get_idle_workers()
            if not workers:
                # wait for idle worker
                pass
            else:
                worker = workers.popleft()
            # the assign task should update the status of the worker and the task.
            worker.assign_task(task)
            worker.execute()

    def get_running_workers(self):
        return self.get_workers_by_status(WorkerStatus.RUNNING)

    def get_idle_workers(self):
        return self.get_workers_by_status(WorkerStatus.IDLE)

    def get_workers_by_status(self, status):
        # check if status is instance of WorkerStatus
        result = []
        for worker_string in self.worker_string:
            if self.worker_string_to_worker_object_map[worker_string].get_status() == status:
                result.append(worker_string)
        return collections.deque(result)

    def wait_for_idle_worker(self):
        # TODO
        pass

    def check_workers_for_completion_and_update(self, running_worker):
        # TODO
        pass

    def __str__(self):
        return '<Scheduler: worker_ips: "%s"  mode:%d  test_to_include:%s ' \
               'test_to_ignore:%s shared_location:%s log location:%s timeout:%d>' % (
                   self.worker_ips,
                   self.mode,
                   self.test_to_include,
                   self.test_to_ignore,
                   self.shared_location,
                   self.log_location,
                   self.timeout
               )
