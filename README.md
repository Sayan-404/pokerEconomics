# Simulation Model

## The model

Describe the model briefly.
Mention the formula along with parameters.

## Repo Components

| Folder | Function |
| ------ | -------- |
| analysis |  |
| checks |  |
| components |  |
| configs |  |
| data |  |
| engines |  |
| hand_evaluator |  |
| poker_metrics |  |
| strategies |  |

PS: Detailed READMEs for each folder will be added in the future.

## Misc

### To-Do

- [x] clean up repository
  - [x] Remove chen from private value
  - [x] Decide whether to keep the rational .py files
  - [x] Clean up the batch configs
  - [x] Refactor codebase
    - [x] Refactor engine components
    - [x] Refactor Strategy
    - [x] Refactor poker_metrics
- [x] Decide something for the seed
- [x] clean up requirements.txt
- [x] create an all encompassing setup script that compiles shared library, creates virtual python environment and installs all dependencies
- [x] finalise all parameters (for strategies and others)
- [x] final code review
- [x] documentation (comments and other documentation for strategies)
- [x] change preflop betting
- [x] integrate risk into mean shifting
- [x] observe river
- [x] create optimal testing grounds for a more comprehensive testing
- [x] parameter evaluation demo
- [x] Bluffer limit implementation

### System Checks Before Final Simulation

- [x] Aggression factor displaying after end of simulation
- [x] Maths of strategy verified

### Run docker

Run `docker-compose up -d` to build and start container.
Local storage bounded, no need to build image again on code change.
Only rebuild in case of fundamental changes like changes to init.sh, requirements.txt, Dockerfile, etc.

To build image: `docker build . -t image_name`
To delete image: `docker image rm image_name`.

To run container: `docker run -di image_name`

To stop container: `docker stop container_hash`.
Get container hash using `docker ps`.
To delete container: `docker rm container_hash`.

NOTE: the building process might time out at times due to faulty connection or problems with debian repositories, just restart the building process.
NOTE: new files to poker_metrics/ and ./ should be manually added to the bind in docker-compose.yaml for it to be able to track it.

For docker hub:
To push:
`docker tag <name of the image> <dockerhub username>/<name of your repo>:<version>`
`docker push <tagged image name>:<version name>`

To pull:
`docker pull <tagged image name>:<version>`
