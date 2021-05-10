# LoadBalancer VS ChaosMonkey
The ultimate showdown of 'the Chosen One' vs 'a Monkey' but not just any monkey, monkey descendent from Netflix's Chaos Monkey

## Loadbalancing
Load balancing refers to the process of distributing a set of tasks over a set of resources, with the aim of making their overall processing more efficient. Load balancing can optimize the response time and avoid unevenly overloading some compute nodes while other compute nodes are left idle. (obviously stolen from wikipedia )

## Netflix's Chaos Monkey
Chaos Monkey is responsible for randomly terminating instances in production to ensure that engineers implement their services to be resilient to instance failures.
[Link: https://netflix.github.io/chaosmonkey/]

## About the project
A small fight simulation between the two, LoadBalancer trying to assign/track/schedule/update tasks to servers while ChaosMonkey just monkeying around and toggling the server switch.
If all tasks are complete, LoadBalancer wins.
If all servers are down, ChaosMonkey wins.

