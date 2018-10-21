# BSidesPDX CTF 2018

## WHAT

This is the development environment for the 2018 BSidesPDX CTF. We will reference the deployment and infra setup used in [BSidesPDX 2017 CTF](https://github.com/BSidesPDX/CTF-2017/tree/master/deployTemplate/src) for this years as well.

1. Write your challenge idea in `concepts.txt`
1. copy the `deployTemplate` dir structure for your challenge (only commit the working parts. The deploy yamls should be changed before committing, for example)
1. Implement your challenge
1. If applicable, add your docker config to `docker-compose.yml` and add relevant information to `Makefile` to automate the process of deploying a local instance of the CTF
1. Provide a solution for your challenge

## Challenges

| Challenge Name | Category  | Points | Port |
|----------------|-----------|--------|------|
| capture        | forensics | 100    | N/A  |
| hidden         | forensics | 200    | N/A  |
| mic            | forensics | 300    | N/A  |
| goxor          | pwn/re        | 100    | N/A  |
| secureshell    | pwn/re        | 200    | 7100 |
| pwnclub        | pwn/re        | 300    | 31337 |
| leaky projects | OSINT        | 100 | |
| leaky secrets  | OSINT        | 200 | |
| leaky security | OSINT | 300 | |
| death_by_1000_curls | web | 100 | 43478|
| Dodona           | web | 200 | 4738 |
| Trollsec         | web | 300 | 10101|

## Local Deployment

To locally test, deploy or play challenges with Docker, run the following (Ubuntu)

1. `sudo apt install gcc-multilib gcc-mipsel-linux-gnu gcc-arm-linux-gnueabi g++-multilib linux-libc-dev:i386`
1. `make`
1. `docker-compose build && docker-compose up -d`
1. Containers are viewable at localhost:PORT (view with docker-compose ps)
1. `docker-compose kill` to stop the containers
1. `make clean` to clean the source folders

## BSidesPDX

CTF was ran during [BSidesPDX 2018](https://bsidespdx.org/events/2018/contests-events.html) on October 26th and 27th.

We used [CTFd](https://ctfd.io/) for the scoreboard hosted at [BSidesPDXCTF.party](https://bsidespdxctf.party/).
