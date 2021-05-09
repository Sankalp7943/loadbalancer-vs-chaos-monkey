# CODE IS IN DEVELOPMENT

import logging
import random
import uuid

"""
Flow
takes inputs from users (later)
start servers
update loadbalancer
create a task with some time bound loops
call loadbalancer class object to assign the tasks
start chaos monkey and observe

run functions to take all inputs of the simulation

same scenario on time based scheduling 
"""

class Task:
    def __init__(self, description="default description", task_type=0):
        #task_id
        #task_description
        #task_type
        #task_time
        print("programming running")
        self.task_id = uuid.uuid1() #unique id
        self.description = description #string 
        self.task_type = task_type
        self.task_time = 10
        print(
            f"\n####  Task Created  ####\nTask ID: {self.task_id}\
            \nTask type: {self.task_type}\nDescription: {self.description}\
            \nCompletion Time: {self.task_time}second(s)\n"
        )


class Server:
    def __init__(self, name, status=1):
        self.server_id = uuid.uuid1() #unique id
        self.server_name = str(name)
        self.status = status
        self.waiting_time = 0
        self.jobs = []
        print(
            f"\n####  Server Created  ####\nServer ID: {self.server_id}\
            \nServer Name: {self.server_name}\nServer status: {self.status} (0: Offline, 1: Online)\
            \nWaiting Time: {self.waiting_time}second(s)\nJobs on the server: {len(self.jobs)}\n"
        )


class LoadBalancer:

    TASK_TYPES = {0: 10, 1: 15, 2: 20} # can be a global variable to prevent multiple reinitialisation of dic

    def __init__(self, time_based = 0):
        self.all_tasks = {}
        self.all_servers = {}
        self.servers_jobs_list = {}
        self.servers_online = {}
        self.servers_offline = {}
        self.time_based = time_based
    #   self.avg_task_time = {}
        print("\n####  LOAD BALANCER CREATED  ####\n")
    
    #def add_avg_task_time(self, task):


    def get_task_time(self, task):
    # can be off other types, use try except or just go with limited types here
        task.task_time = TASK_TYPES[task.task_type]
    
    def register_new_task(self, task):
        self.all_tasks[task.task_id] = task

    def schedule_task(self, task):
        if self.time_based:
            minimum_wait_server = float('inf')
            for uid, server in self.all_servers.items():
                if server.status:
                    if minimum_wait_server < server.waiting_time:
                        target_server = server
                        minimum_wait_server = server.waiting_time
        else:
            minimum_jobs = float('inf')
            for uid, server in self.all_servers.items():
                if server.status:
                    if minimum_jobs < len(server.jobs):
                        minimum_jobs = len(server.jobs)
                        target_server = server
        try:
            target_server.jobs.append(task)
            target_server.waiting_time+=task.task_time
            self.servers_jobs_list[target_server.server_id].append(task)
        except:
            raise Exception("No server online")

# chec where in dictionary key is server id and where it is server
    def balance(self):
        # all offline server task reassigned
        for uid, server in self.servers_offline.items():
            for task in server.jobs:
                self.schedule_task(task)
            server.jobs = []
            self.servers_jobs_list[uid] = [] #update in server job list
        
        all_active_tasks = set()
        for uid, tasks in self.servers_jobs_list.items():
            all_active_tasks = all_active_tasks | set(tasks)
        
        to_be_rescheduled_tasks = set(self.all_tasks) - all_active_tasks
        for task in to_be_rescheduled_tasks:
            self.schedule_task(task)
        all_active_tasks.clear()

        #check for change in server status
        for uid, server in self.servers_offline.items():
            if server.status:
                self.servers_online[uid] = server
                self.servers_offline.pop(uid)
        
        for uid, server in self.servers_online.items():
            if not server.status:
                self.servers_offline[uid] = server
                self.servers_online.pop(uid)
        #balance stuff whenever new servers are added or removed offline or online

    def update(self):
        #waiting time for job is finished or not etc
        for uid, server in self.servers_online.items():
            server.jobs[0].task_time -= time_interval
            server.waiting_time -= time_interval
            if server.jobs[0].task_time <= 0:
               completed_task = server.jobs[0].task_time.pop(0)
            self.all_tasks.pop(completed_task.task_id)
            self.servers_jobs_list[uid].pop(0)

    def add_server(self, server):
        self.all_servers[server.server_id] = server
        self.servers_jobs_list[server.server_id] = server.jobs
        if server.status:
            self.servers_online[server.server_id] = server
        else:
            self.servers_offline[server.server_id] = server

    def take_server_offline(self, server):
        server.status = 0


class ChaosMonkey:
    def __init__(self, loadbalancer):
        self.all_servers_info = loadbalancer

    def maybe(self):
        return random.getrandbits(1)

    def server_chaos(self):
        time.sleep(10)
        for uid, servers in self.all_servers_info.all_servers.items():
            time.sleep(5)
            servers.status = self.maybe()


def run():
    print(f"Total simulation time is {total_simulation_time//60} minute(s)")
    print(f"Internal between ")


if __name__ == "__main__":
    total_simulation_time = int(input("How long you want the simulation to run (in minute(s))? "))
    total_simulation_time *= 60 
    time_interval = 2
    number_of_servers = 0
    while number_of_servers <= 0:
        number_of_servers = int(input("Enter number of servers: "))
        if number_of_servers<=0:
            print("Invalid! Must be atleast '1'")
    number_of_tasks = number_of_servers*5
    run()


"""
class LoadBalancer:
    #all tasks
    #servers
    #server to task
    #avg task type
    #servers offline

class ChaosMonkey:
    #servers_online
    #servers_offline
"""

