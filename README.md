# RollBot – Turning a Personal Discord Bot into a Cloud-Native SaaS
## Project Overview

RollBot is a Discord bot designed to assist tabletop roleplaying games by storing character sheets and performing dice rolls directly within Discord.

The goal of this project is not only to build a useful tool, but also to serve as a real-world DevOps learning platform. Over time, RollBot will evolve into a small cloud-hosted service built using modern DevOps practices such as:

- containerized deployment
- CI/CD pipelines
- infrastructure as code
- observability and monitoring
- automated testing

By iteratively improving both the application and the infrastructure that runs it, this project aims to simulate the lifecycle of a real software service.
## Background
### Dungeons and Dragons
Back in 2020, I was running a Dungeons and Dragons campaign with a group of friends. For anyone unfamiliar, Dungeons and Dragons (D&D for short) is a tabletop fantasy roleplaying game, usually for 5-7 players. One player acts as the Game Master (GM), describing the scenes playing out, while the rest of the players control their own characters interacting with the game world.

Most interactions in the game are handled by the **D20 Test**: a player attempting a challenge rolls a 20 sided die, adds some integer modifier to the result based on the nature of the challenge (skill modifier), and the result is compared to a target number set by the GM to reflect the difficulty of the task. If the player's number is equal to or higher than the target - their character succeeds the challenge, and fails otherwise. Each character's different skill modifiers are detailed in their **Character Sheets**, along with many other details of the character.
### The Problem
Like many other groups we moved our games to an online space; the Discord platform. However, a minor table problem now became a major issue: players who usually rely on others at the table suddenly have to interpret character sheets on their own, slowing the game down to a crawl if not halting it altogether.

As a recent Computer Science graduate, I decided to build a small tool to solve the problem. I designed a Discord bot user which holds each player's character sheet, and can perform D20 tests, as well as other dice rolls required by the game. It was barebones, ran locally on my laptop, and eventually ran into issues when a different bot was introduced into the server. It worked for its narrow purpose, and never ran again after that campaign came to an end.
## The DevOps Cycle
As of recently, I am expanding my portfolio of software design projects. A major goal of this expansion is to familiarize myself with modern software design paradigms, such as those outlined in the (poorly named) 12 Factor App. Moreover, I am aiming to gain practical experience with real Cloud infrastructure with a real application, as opposed to a simple "Hello World" project.

To that end, this project aims to implement a complete **DevOps Cycle** for an actual live service, and utilize this implementation to maintain and further develop this service. These stages are commonly summarized as:

>Plan → Code → Build → Test → Release → Deploy → Operate → Monitor

Let us expand on the components of that cycle:
### Plan
This refers to abstract problem solving, assessing the needs of the users, the scope of the application etc. In my example, this came down to mapping out the character sheet data structure and the actual commands to implement.
### Code
Implementing plans as code, and managing the resulting codebase. In my "hacky" solution, I just kept the javascript files locally on my PC, not even as a git repository (sidenote: it is MADNESS that git is not taught in a CS Bachelor's degree). With git and GitHub, I not only gain codebase management, but also gain access to tools which will be useful on following steps.
### Build
Compilation, packaging, and any other process that results in artifacts that can deploy our program on a host. Previously, since my own machine was also the deployment target, and javascript is not a compiler language, this step was invisible. With modern cloud servers as a deployment target, however, building becomes entirely different.

The main difference is that the development environment is no longer identical to the release environment. My development environment contains development tools, secrets such as service tokens, and specific computing resources and specs. These all need to be handled differently on different environments, which can be easily ensured via Docker Compose, building a docker image (or a set of such images) which ensures consistent environments across development and production.
### Test
As the complexity of the software rises, the likelier it is that bugs and errors arise. Ideally, we'd like to detect and eliminate any of them *before* users start using the product. To that end, we can implement automatic tests which detect a wide range of unexpected behaviors in the codebase.

GitHub provides a tool for such tests and more: GitHub Actions. It allows us to define workflows to be executed on certain triggers (such as pushes to main), which in this case is our test suites. Since the new bot is implemented in Python and not javascript, these tests will be implemented with PyTest.
### Release
Once a build has passed every test, it can be published and viewed by the user base. These releases are versioned, to maintain a clear history of the software and allow access to previous releases, some of which may not be supported.
### Deploy
Most modern applications are not run from the users' host directly, but are services with small scale client applications (mostly browsers) making requests to those services. Deployment refers to the process of setting up these servers with our application. This project is an example of such an application, as just one bot can serve any number of users in theory.

In practice, the deployed application must be designed to handle the load of requests sent its way. Modern applications are designed to be *Scalable*, often orchestrating multiple docker containers, spawning and pruning them as needed to handle any scale of requests at any given time.
### Operate
An application being released and deployed is never a smooth process. User transition may be rough, new bugs may be revealed, and conflict between already running components of the applications and the new deployment may arise. These are all part of the operations phase: maintaining a live service with actual clients, gathering input from them, etc.
### Monitor
Data should not only be collected from the user base, but from the application and its infrastructure. Tools like Grafana already offer a variety of implementations to monitor:
- Command latency
- API error rates
- CPU and memory utilization
- Command usage per Discord server

and other valuable metrics.

The collected data leads to further planning, coding etc., thus the term DevOps Cycle.
## Goals
1. Implement every step of the DevOps Cycle.
2. Further develop the capabilities of this bot:
	1. Attack and Damage rolls.
	2. Other tabletop systems.
	3. Out of session utilities: scheduling, reminders, etc.
3. Possible: Implement a web UI for character / campaign management.

## Current Architecture
At the moment, RollBot is a simple Python application consisting of:

- A Discord bot interface
- A rules engine implementing tabletop game systems
- Character sheet data structures

Future versions will introduce persistent storage, containerized deployment, and cloud infrastructure.

## Planned Architecture
As the project evolves, RollBot will transition from a simple local application to a small cloud-hosted service.

The planned architecture includes:

Discord Gateway  
↓  
Bot Service (containerized Python application)  
↓  
Redis (caching and background jobs)  
↓  
PostgreSQL (persistent character storage)

Supporting infrastructure will include:

- Docker for containerization
- GitHub Actions for CI/CD
- Terraform for infrastructure as code
- Kubernetes for container orchestration
- Prometheus and Grafana for monitoring

## Why This Project Exists
After several years working primarily with on-premise infrastructure, I wanted to gain hands-on experience with modern cloud-native development workflows.

Rather than build a trivial "hello world" project, RollBot provides a real application with evolving requirements, making it an ideal platform to explore topics such as:

- CI/CD pipelines
- container orchestration
- service monitoring
- infrastructure automation
