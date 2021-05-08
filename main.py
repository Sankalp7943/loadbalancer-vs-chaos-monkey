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

class LoadBalancer:

    task_types = {} # can be a global variable to prevent multiple reinitialisation of dic

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
        task.task_time = task_types[task.task_type]:
    
    def register_new_task(self, task):
        self.all_tasks[task.task_id] = task

    def schedule_task(self, task):
        if self.time_based:
            minimum_wait_server = float('inf')
            for server in self.all_servers.items():
                if server.status:
                    if minimum_wait_server < server.waiting_time:
                        target_server = server
                        minimum_wait_server = server.waiting_time
        else:
            minimum_jobs = float('inf')
            for server in self.all_servers.items():
                if server.status:
                    if minimum_jobs < len(server.jobs):
                        minimum_jobs = len(server.jobs)
                        target_server = server
        try:
            target_server.jobs.append(task)
            target_server.waiting_time+=task.task_time
            self.servers_jobs_list[target_server.id].append(task)
        except:
            raise Exception("No server online")


    def server_crashed():
        clear_all_data from the server object
        reschedule/reassign all tasks to other servers
    
    def server_gets_online():
        check if any old tasks is left or not
        balance jobs 

    def update()

    def update_all_tasks()

    def add_server(self, server):
        self.all_servers[server.id] = server
        self.

    def remove_server()

    def update_online_server()

    def update_offline_servers()


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


if __name__ == "__main__":
    
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