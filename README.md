# BSidesPDX CTF 2018

## BSidesPDX

CTF was ran during [BSidesPDX 2018](https://bsidespdx.org/events/2018/contests-events.html) on October 26th and 27th.

We used [CTFd](https://ctfd.io/) for the scoreboard hosted at [BSidesPDXCTF.party](https://bsidespdxctf.party/).

Challenges built by: [TTimzen](https://twitter.com/TTimzen), [fdcarl](https://twitter.com/fdcarl), [aagallag](https://twitter.com/aagallag), [dade](https://twitter.com/0xdade) & [arinerron](https://twitter.com/arinerron)

Infrastructure support provided by Mozilla: Jeff Bryner, Andrew Krug and Daniel Hartnell

## Challenges

| Challenge Name | Category  | Points | Port |
|----------------|-----------|--------|------|
| capture        | forensics | 100    | N/A  |
| hidden         | forensics | 200    | N/A  |
| mic            | forensics | 300    | N/A  |
| goxor          | pwn/re        | 100    | N/A  |
| secureshell    | pwn/re        | 200    | 7100 |
| pwnclub        | pwn/re        | 300    | 31337 |
| leaky projects | OSINT        | 100 | N/A |
| leaky secrets  | OSINT        | 200 | N/A |
| leaky security | OSINT | 300 | N/A |
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

## Cloud Deployment

This year we ran all of our challenges in k8s using the `Makefile` and yamls in the `aws` directory of pwn-re 100, 200 and all web challenges.
