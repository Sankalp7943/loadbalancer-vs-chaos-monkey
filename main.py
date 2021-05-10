# CODE IS IN DEVELOPMENT, TIME BASED TRUE IS TESTED
import random
import uuid
import time

TASK_TYPES = {0: 5, 1: 10, 2: 15} # can be edited manually for changing scenarios


class Task:
    """
    A single task created using this.

    task_id(uuid): Unique id for task
    desciption(str): Description of the task, used as task name in the program for simplicity
    task_type(int): Type of task (in order to assign an average wait time for task)
    task_time(int): Completion time of the task based on its type, check TASK_TYPES for the values
    """
    def __init__(self, description="default description", task_type=0):
        self.task_id = uuid.uuid1()
        self.description = description
        self.task_type = task_type
        self.task_time = TASK_TYPES[self.task_type]
        print(
            f"\n####  Task Created  ####\nTask ID: {self.task_id}\
            \nTask type: {self.task_type}\nDescription: {self.description}\
            \nCompletion Time: {self.task_time}second(s)\n"
        )


class Server:
    """
    A server is created using this class
    server_id(uuid): Unique id for each server
    server_name(str): Name of the server
    status(0 or 1): Online and offline status ( 0 and 1 respectively )
    waiting_time(int):  Total expected waiting time of the server to get idle
    jobs(list): List of tasks to be performed (contains task objects)
    """
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
    """
    Prints status of a server
    """
        if self.status:
            print(f"Server '{self.server_name}' is online")
        else:
            print(f"Server '{self.server_name}' is offline")   


class LoadBalancer:
    """
    LoadBalancer object created using this. It is the CHOSEN ONE. Enenmy of ChaosMonkey.

    all_tasks(set): All tasks universally in the program(including all servers)
    all_servers(dict): (key(uuid): server_id, value: server object) All servers universally in the program.
    servers_jobs_list(dic): (key(uuid): server_id, value(list): list of jobs assigned to that server)
    servers_online(dict): (key(uid): server_id, value: server object) Only the ones whose status is online
    servers_offline(dict): (key(uid): server_id, value: server object) Only the ones whose status is offline
    time_based(bool): True for scheduling jobs based on server waiting time, False for based on number of jobs
    """
    def __init__(self, time_based = 0):
        self.all_tasks = set()
        self.all_servers = {}
        self.servers_jobs_list = {}
        self.servers_online = {}
        self.servers_offline = {}
        self.time_based = time_based
        print("\n####  LOADBALANCER CREATED  ####\n")

    def get_task_time(self, task):
        """
        Assign the task time to a task based on its type
        task(object): task object
        """
        task.task_time = TASK_TYPES[task.task_type]
        print("Fetched task time")
    
    def register_new_task(self, task):
        """
        Registers a new task into knowledge of loadbalancer for later scheduling
        task(object): task object
        """
        self.all_tasks.add(task)
        print(f"Task registered in loadbalancer {task.task_id} description {task.description}")

    def schedule_task(self, task):
        """
        Schedules a task onto a server based on the loadbalance scheduling type(time_based or not)
        task(object): task object
        """
        if self.time_based:
            minimum_wait_server = float('inf')
            for uid, server in self.all_servers.items():
                if server.status:
                    if minimum_wait_server > server.waiting_time:
                        target_server = server
                        minimum_wait_server = server.waiting_time
            try:
                target_server.jobs.append(task)
                target_server.waiting_time += task.task_time
                self.servers_jobs_list[target_server.server_id].append(task)
            except Exception:
                print("There are no servers left to reassign")
                raise Exception("#################   CHAOS MONKEY WON    ####################")
        else:
            minimum_jobs = float('inf')
            for uid, server in self.all_servers.items():
                if server.status:
                    if minimum_jobs > len(server.jobs):
                        minimum_jobs = len(server.jobs)
                        target_server = server
            try:
                target_server.jobs.append(task)
                target_server.waiting_time += task.task_time
                self.servers_jobs_list[target_server.server_id].append(task)
            except Exception:
                print("There are no servers left to reassign")
                raise Exception("#################   CHAOS MONKEY WON    ####################")

    def populate_server(self, target_server):
        """
        Assigns a task to a newly came online server
        target_server(object): a server object which just changed status to online
        """
        for uid in self.servers_online:
            server = self.all_servers[uid]
            if server == target_server:
                pass
            else:
                if len(server.jobs)>1:
                    shifting_task = server.jobs.pop(-1)
                    self.servers_jobs_list[server.server_id].remove(shifting_task)
                    server.waiting_time-=shifting_task.task_time
                    self.schedule_task(shifting_task)

    def balance(self, printTrue = 0):
        """
        Reassigns the tasks from the server which went offline to other online servers
        Checks if any registered but unassigned tasks are present. If any, schedules them on a server
        Maintains and tracks info of servers which switched their status and their related info
        printTrue(bool): Used to reduce number of logs/output printed(as this function is being called a lot)
        """
        for uid, server in self.servers_offline.items():
            for task in server.jobs:
                self.schedule_task(task)
            server.jobs = []
            number_of_jobs_reschedule = len(self.servers_jobs_list[uid])
            self.servers_jobs_list[uid] = []
            if printTrue:
                print(f"{number_of_jobs_reschedule} jobs from {server.server_name} reassigned")
        
        all_active_tasks = set()
        for uid, tasks in self.servers_jobs_list.items():
            if self.all_servers[uid].status:
                all_active_tasks = all_active_tasks | set(tasks)
            if not self.all_servers[uid].status:
                self.all_servers[uid].jobs = []
                self.all_servers[uid].waiting_time = 0    
        to_be_rescheduled_tasks = self.all_tasks - all_active_tasks
        if printTrue:
            print(f"{len(to_be_rescheduled_tasks)} need(s) to be reassigned")
        to_be_rescheduled_tasks = list(to_be_rescheduled_tasks)
        while len(to_be_rescheduled_tasks):
            task = to_be_rescheduled_tasks.pop(0)
            self.schedule_task(task)
        all_active_tasks.clear()

        pop_item = []
        for uid, server in self.servers_offline.items():
            if server.status:
                self.servers_online[uid] = server
                pop_item.append(uid)
                print(f"Server {server.server_name} came online")
                self.populate_server(server)
        for item in pop_item:
            self.servers_offline.pop(item)
        
        pop_item = []
        for uid, server in self.servers_online.items():
            if not server.status:
                self.servers_offline[uid] = server
                pop_item.append(uid)
                print(f"Server {server.server_name} went offline")
                server.jobs = []
                server.waiting_time = 0
        for item in pop_item:
            self.servers_online.pop(item)

    def update(self):
        """
        Tracks and Updates tasks after every time step, removes finished tasks
        Assigns some task if any server is idle
        Prints the number of jobs on each server and which servers are offline
        """
        for uid, server in self.servers_online.items():
            if len(server.jobs):
                self.populate_server(server)
        for uid, server in self.servers_online.items():
            if server.jobs:
                server.jobs[0].task_time -= time_interval
                server.waiting_time -= time_interval
                if server.jobs[0].task_time <= 0:
                    completed_task = server.jobs.pop(0)
                    print(f"Task '{completed_task.description}' completed")
                    self.all_tasks.remove(completed_task)
                    self.servers_jobs_list[uid].pop(0)
        for uid, server in self.all_servers.items():
            if server.status:
                print(f"{server.server_name} has {len(set(server.jobs))} job(s)")
            else:
                print(f"{server.server_name} is offline")

    def add_server(self, server):
        """
        Registers a server onto a loadbalancer
        server(object): A server object which needs to get added to loadbalancer to be assigned tasks
        """
        self.all_servers[server.server_id] = server
        self.servers_jobs_list[server.server_id] = server.jobs
        if server.status:
            self.servers_online[server.server_id] = server
        else:
            self.servers_offline[server.server_id] = server
        print(f"Server '{server.server_name} added'")

    def take_server_offline(self, server):
        """
        Takes a server go offline manually
        server(object): A server object which needs to get offline
        """
        server.status = 0
        print(f"Server {server.server_name} is offline")


class ChaosMonkey:
    """
    Named after Netflix's Chaos Monkey system
    Inspired by Netflix's ChaosMonkey this is also randomly crash a server.
    But what do you know, sometimes while monkeying around it can turn on a crashed server as well
    loadbalancer(object): Object of LoadBalancer, Its arch-enemy the Chosen One
    """
    def __init__(self, loadbalancer):
        self.all_servers_info = loadbalancer

    def maybe(self):
        """
        Returns 0 or 1 randomly
        """
        return random.getrandbits(1)

    def server_chaos(self):
        """
        Attacks a server randomly and switches its power randomly
        """
        for uid, server in self.all_servers_info.all_servers.items():
            if self.maybe():
                print(f"Chaos Monkey attacked server '{server.server_name}'")
                after_attack_status = self.maybe()
                server.status = after_attack_status
                if not after_attack_status:
                    print(f"Server '{server.server_name}' went offline by the attack")


def run():
    """
    Sequence the complete simulation in a flow
    """
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
        loadbalancer.balance(1)
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
    """
    Takes all the user inputs
    """
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
    print("\n\n")
    run()
