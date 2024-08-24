# pokerEconomics

## to-do

- [x] clean up repository
  - [x] Remove chen from private value
  - [x] Decide whether to keep the rational .py files
  - [x] Clean up the batch configs
  - [x] Refactor codebase
    - [x] Refactor engine components
    - [x] Refactor Strategy
    - [x] Refactor poker_metrics
- [ ] Decide something for the seed
- [x] clean up requirements.txt
- [x] create an all encompassing setup script that compiles shared library, creates virtual python environment and installs all dependencies
- [ ] finalise all parameters (for strategies and others)
- [x] final code review
- [ ] documentation (comments and other documentation for strategies)
- [x] change preflop betting
- [x] integrate risk into mean shifting
- [x] observe river
- [ ] create optimal testing grounds for a more comprehensive testing
- [ ] parameter evaluation demo
- [ ] Bluffer limit implementation

## System Checks Before Final Simulation

- [ ] Aggression factor showing after end of simulation
- [ ] Maths of strategy verified

## Run docker

```docker build . -t image_name
docker run -d image_name```
