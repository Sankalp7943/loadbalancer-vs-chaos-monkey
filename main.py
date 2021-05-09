# CODE IS IN DEVELOPMENT, DURING SERVER SWITCHING ONLINE OFFLINE, TWO INSTANCES OF TASKS ARE MADE

import logging
import random
import uuid
import time

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
TASK_TYPES = {0: 10, 1: 15, 2: 20} # can be a global variable to prevent multiple reinitialisation of dic

class Task:
    def __init__(self, description="default description", task_type=0):
        #task_id
        #task_description
        #task_type
        #task_time
        self.task_id = uuid.uuid1() #unique id
        self.description = description #string 
        self.task_type = task_type
        self.task_time = TASK_TYPES[self.task_type]
        print(
            f"\n####  Task Created  ####\nTask ID: {self.task_id}\
            \nTask type: {self.task_type}\nDescription: {self.description}\
            \nCompletion Time: {self.task_time}second(s)\n"
        )


class Server:
    def __init__(self, name="default_server_name", status=1):
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
    
    def get_status(self):
        if self.status:
            print(f"Server '{self.server_name}' is online")
        else:
            print(f"Server '{self.server_name}' is offline")   


class LoadBalancer:

    def __init__(self, time_based = 0):
        self.all_tasks = set()
        self.all_servers = {}
        self.servers_jobs_list = {}
        self.servers_online = {}
        self.servers_offline = {}
        self.time_based = time_based
    #   self.avg_task_time = {}
        print("\n####  LOADBALANCER CREATED  ####\n")
    
    #def add_avg_task_time(self, task):


    def get_task_time(self, task):
    # can be off other types, use try except or just go with limited types here
        task.task_time = TASK_TYPES[task.task_type]
        print("Fetched task time")
    
    def register_new_task(self, task):
        self.all_tasks.add(task)
        print(f"Task registered in loadbalancer {task.task_id} description {task.description}")

    def schedule_task(self, task):
        if self.time_based:
            minimum_wait_server = float('inf')
            for uid, server in self.all_servers.items():
                if server.status:
                    if minimum_wait_server > server.waiting_time:
                        target_server = server
                        minimum_wait_server = server.waiting_time
                        target_server.jobs.append(task)
                        target_server.waiting_time += task.task_time
                        self.servers_jobs_list[target_server.server_id].append(task)
                        print(f"Task {task.task_id} scheduled to server {server.server_name}")
        else:
            minimum_jobs = float('inf')
            for uid, server in self.all_servers.items():
                if server.status:
                    if minimum_jobs > len(server.jobs):
                        minimum_jobs = len(server.jobs)
                        target_server = server
                        target_server.jobs.append(task)
                        target_server.waiting_time += task.task_time
                        self.servers_jobs_list[target_server.server_id].append(task)
                        print(f"Task {task.task_id} scheduled to server {server.server_name}")

# chec where in dictionary key is server id and where it is server
    def balance(self):
        # all offline server task reassigned
        for uid, server in self.servers_offline.items():
            for task in server.jobs:
                self.schedule_task(task)
            server.jobs = []
            self.servers_jobs_list[uid] = [] #update in server job list
            print(f"Jobs from {server.server_name} reassigned")
        
        all_active_tasks = set()
        for uid, tasks in self.servers_jobs_list.items():
            all_active_tasks = all_active_tasks | set(tasks)
        
        to_be_rescheduled_tasks = self.all_tasks - all_active_tasks
        print(f"{len(to_be_rescheduled_tasks)} need(s) to be reassigned")
        for task in to_be_rescheduled_tasks:
            self.schedule_task(task)
        all_active_tasks.clear()

        pop_item = []
        #check for change in server status
        for uid, server in self.servers_offline.items():
            if server.status:
                self.servers_online[uid] = server
                pop_item.append(uid)
                print(f"Server {server.server_name} came online")
        for item in pop_item:
            self.servers_offline.pop(item)
        
        pop_item = []
        for uid, server in self.servers_online.items():
            if not server.status:
                self.servers_offline[uid] = server
                pop_item.append(uid)
                print(f"Server {server.server_name} went offline")
        for item in pop_item:
            self.servers_online.pop(item)
        #balance stuff whenever new servers are added or removed offline or online

    def update(self):
        #waiting time for job is finished or not etc
        for uid, server in self.servers_online.items():
            if server.jobs:
                server.jobs[0].task_time -= time_interval
                server.waiting_time -= time_interval
                if server.jobs[0].task_time <= 0:
                    completed_task = server.jobs.pop(0)
                    print(f"Task '{completed_task.task_id}' completed")
                    self.all_tasks.remove(completed_task)
                    self.servers_jobs_list[uid].pop(0)

    def add_server(self, server):
        self.all_servers[server.server_id] = server
        self.servers_jobs_list[server.server_id] = server.jobs
        if server.status:
            self.servers_online[server.server_id] = server
        else:
            self.servers_offline[server.server_id] = server
        print(f"Server '{server.server_name} added'")

    def take_server_offline(self, server):
        server.status = 0
        print(f"Server {server.server_name} is offline")


class ChaosMonkey:
    def __init__(self, loadbalancer):
        self.all_servers_info = loadbalancer

    def maybe(self):
        return random.getrandbits(1)

    def server_chaos(self):
        for uid, server in self.all_servers_info.all_servers.items():
            if self.maybe():
                print(f"Chaos Monkey attacked server '{server.server_name}'")
                server.status = self.maybe()
                if not server.status:
                    print(f"Server '{server.server_name}' went offline by the attack")



def run():
    print("######## SIMULATION CONFIGURATION ########")
    print(f"Total simulation time is {total_simulation_time//60} minute(s)")
    print(f"Interval between refresh cycles is {time_interval} second(s)")
    if number_of_servers == 1: print("Number of server is 1")
    else: print(f"Number of servers are {number_of_servers}")
    print(f"Number of tasks being created are {number_of_tasks}\n\n")

    print("##### Creating components #####\n")

    if loadbalancer_type:
        loadbalancer = LoadBalancer(1)
    else:
        loadbalancer = LoadBalancer()
    print("Creating servers")
    server_list = []
    for i in range(number_of_servers):
        server = Server("server_"+str(i),1)
        server_list.append(server)
    print("Servers Created\n")
    print("Creating ChaosMonkey")
    chaosmonkey = ChaosMonkey(loadbalancer)
    print("Created ChaosMonkey\n")
    print("Creating Tasks")
    tasks_list = []
    for i in range(number_of_tasks):
        task = Task("task_number_"+str(i),random.randint(0,2))
        tasks_list.append(task)
    print("Tasks Created\n")
    print("##### Components created #####\n\n")

    print("##### Registering components in loadbalancer #####\n")
    for server in server_list:
        loadbalancer.add_server(server)
    for task in tasks_list:
        loadbalancer.register_new_task(task)
    print("##### Registered Components #####\n\n")

    print("##### Beginning simulation #####")
    for _ in range(0, total_simulation_time, time_interval):
        print(f"At time {_}second(s):")
        loadbalancer.balance()
        loadbalancer.update()
        loadbalancer.balance()
        chaosmonkey.server_chaos()
        loadbalancer.balance()
        time.sleep(time_interval)
        print("----------------------\n")
        print("Tasks Remaining: ", len(loadbalancer.all_tasks))
        print("Servers Remaining: ", len(loadbalancer.servers_online.items()))
        if len(loadbalancer.all_tasks)==0:
            print("All tasks are complete, You won :D")
            break
        if len(loadbalancer.servers_online.items())==0:
            print("Chaos Monkey destroyed the system! You lost :(")
            break
        print("----------------------\n")  
    print("##### Simulation ended #####\n ")



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
    loadbalancer_type = bool(input("Enter 'True' for Time based loadbalancer, otherwise enter 'False': "))
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

