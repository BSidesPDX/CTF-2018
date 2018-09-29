# BSidesPDX CTF 2018

## WHAT

This is the development environment for the 2018 BSidesPDX CTF. We will reference the deployment and infra setup used in [BSidesPDX 2017 CTF](https://github.com/BSidesPDX/CTF-2017/tree/master/deployTemplate/src) for this years as well.

1. Write your challenge idea in `concepts.txt`
1. copy the `deployTemplate` dir structure for your challenge
1. Implement your challenge
1. If applicable, add your docker config to `docker-compose.yml` and add relevant information to `Makefile` to automate the process of deploying a local instance of the CTF
1. Provide a solution for your challenge

## Challenges

| Challenge Name | Category  | Points | Port |
|----------------|-----------|--------|------|
| capture        | forensics | 100    | N/A  |
| hidden         | forensics | 200    | N/A  |
|                | forensics | 300    | N/A  |
| goxor          | pwn/re        | 100    | N/A  |
|                | pwn/re        | 200    |   |
|                | pwn/re        | 300    |   |
|                | OSINT        | 100 | |
|                | OSINT        | 200 | |
|                | OSINT | 300 | |
| death_by_1000_curls | web | 100 | |
| Dodona           | web | 200 | |
| Trollsec         | web | 300 | |



## Local Deployment

To locally test, deploy or play challenges with Docker, run the following (Ubuntu)

1. `sudo apt install gcc-multilib gcc-mipsel-linux-gnu gcc-arm-linux-gnueabi g++-multilib linux-libc-dev:i386`
1. `make`
1. `docker-compose build && docker-compose up -d`
1. Containers are viewable at localhost:PORT (view with docker-compose ps)
1. `docker-compose kill` to stop the containers
1. `make clean` to clean the source folders
