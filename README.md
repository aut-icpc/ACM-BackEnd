# ACM-BackEnd
Backend for ACM-ICPC Registration Website

NOTE: This is a Django project, the only reason why GitHub thinks that it's in JavaScript is because the static files of its dependencies didn't work in production so I had to put them alongside the main files. :))))

# AUT ICPC Website documents

AUT ICPC website can be deployed with either docker swarm or a single docker compose file. This document will explain both methods. But before doing any actions these docker images should be existed on the server. (You should pull them from docker hub):

* postgres:11
* python:3.7

## Method1: Running with docker swarm

### Gitlab CI/CD Runners Configuration

In this method you can configure gitlab ci/cd runner. If you don't need to have continuous deployment or integration, you can safely skip this step.

1. Install gitlab runner on the server. Read documentations [here](https://docs.gitlab.com/runner/install/linux-repository.html).

2. Obtain runner token from our gitlab instance. It can be found in group's settings. Remind that just the owner of the group can have access to this part. You can read more [here](https://docs.gitlab.com/runner/register/). Remind that address of gitlab should have **https**.

3. Register a new **shell** runner on the server with the following command:

~~~
sudo gitlab-runner register
~~~

From now on, every changes you made on the master branch of the front end or back end repositories would be deployed on the server beacuse of having **.gitlab-ci.yml** file in them.

### Bring up other parts of the system in the swarm

1. First of all, a local docker registry should be initiated. It is needed for our swarm service deployment. Docker compose for deploy local registry and related documents can be found [here](https://git.ceit.aut.ac.ir/ssc/icpc/local-registry-compose).

2. Define 127.0.0.1 as a host with *acm-registry* name by:

~~~
sudo echo "127.0.1.1   acm-registry" >> /etc/hosts
~~~

3. Init docker swarm, create a network and push images to local registry:

~~~
docker swarm init
docker network create --scope=swarm --driver=overlay production-net
docker tag postgres:11 acm-registry:5000/postgres:11
docker push acm-registry:5000/postgres:11
~~~


4. Clone database repository and follow instructions to bring it up. Repo can be found [here](https://git.ceit.aut.ac.ir/ssc/icpc/database).

5. Clone application and follow instructions [here](https://git.ceit.aut.ac.ir/ssc/icpc/acm-backend).

6. Clone NGINGX repository and follow instrctions [here](https://git.ceit.aut.ac.ir/ssc/icpc/nginx).

## Method2: Running with single swarm file
Frankly I've skipped on doing this for so long I've forgotten what I was supposed to do, hopefully I'll remember.
