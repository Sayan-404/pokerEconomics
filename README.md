# Key Publications

**Code Repository**: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14840266.svg)](https://doi.org/10.5281/zenodo.14840266)

**Preprint Article**: [![DOI](https://zenodo.org/badge/DOI/10.21203/rs.3.rs-6015303/v1.svg)](https://doi.org/10.21203/rs.3.rs-6015303/v1)

> **Note:** This repository is no longer maintained. Active development and maintenance now take place in a different repository.
> Please visit [main repository](https://github.com/Rumis-Cube/pokerEconomics) or the DOI for the latest updates and contributions.

# Simulation Model

## Disclaimer

This repository is part of an academic research project. The source code for [PokerHandEvaluator](https://github.com/HenryRLee/PokerHandEvaluator) used in this repository is governed by its respective license.

---

## The Model

This repository implements a stochastic game-theoretic model of human behaviour in an incomplete information game (poker). The behaviour modeled is non-deterministic, yet not uniformly random; it tends to conform to specific trends over a long term. A truncated normal distribution is utilised to simulate this behaviour.

### Variables Involved

1. **$\bar{\mu}$**: A measure of how an entity perceives its current condition. It is calculated as:  
   $$\bar{\mu} = hs + shift$$  
   where:  
   - $hs$: Hand strength.  
   - $shift$: The self-proclaimed level of confidence the entity has on their current position.  

2. **$ps$**: The portion of the pot an entity is expected to win based on its equity in the current hand. It is calculated as:  
   $$ps = \frac{\text{callValue}}{\text{pot}}$$  

3. **$ll$**: The lower limit of the truncated normal distribution, fixed at $0$.

4. **$ul'$**: The upper limit of an entity's playing range, determined as:

  <p align="center">
    <img src="./docs/equations/ul_formulation.png" />
  </p>

   where:

- $sp$: Future potential.  
- $risk$: The entity's risk appetite.
- $round$: Poker game round (0 for pre-flop, 1 for flop, and so on).

5. **$ul$**: The actual upper limit of the truncated normal distribution, defined as:  
   $$ul = \max(\bar{\mu}, ul')$$  

### Truncated Normal Distribution

The truncated normal distribution is defined as:  
<p align="center">
  <img src="./docs/equations/normal_dist_formulation.png" />
</p>

where:  

- $\bar{\mu}$: Mean of the underlying normal distribution before truncation.  
- $\bar{\sigma}$: Standard deviation of the underlying normal distribution before truncation, calculated as $(ul - ll) / 3$.
- $ll$: Lower bound for truncation (fixed at $0$).
- $ul$: Upper bound for truncation.  
- $x$: The random variable being evaluated.  
- $\phi(\bar{\mu}, \bar{\sigma}^2; x)$: Probability density function (PDF) of the normal distribution.  
- $\Phi(\bar{\mu}, \bar{\sigma}^2; a)$: Cumulative distribution function (CDF) of the normal distribution at $a$.

The PDF of the normal distribution is:  
$$\phi(x) = \frac{1}{\sqrt{2 \pi \bar{\sigma}^2}} e^{-\frac{(x - \bar{\mu})^2}{2 \bar{\sigma}^2}}$$  

The CDF is:  
$$\Phi(x) = \int_{-\infty}^x \phi(t) \, dt$$  

### Workflow Summary

After calculating the parameters of an entity's decision-making process, a decision factor is sampled using the truncated normal distribution which is then used, along with `ps` to make a decision.

---

## Repository Components

| Folder         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `analysis`     | Scripts for analyzing the output of the simulation engine.                 |
| `checks`       | Tests for various components of the engine.                                |
| `components`   | Core components of the simulation engine.                                  |
| `configs`      | Configuration files and generators for different game profiles.            |
| `data`         | Stores the output data generated by the simulation engine.                 |
| `engines`      | Variations of the simulation engines.                                      |
| `hand_evaluator` | Poker hand evaluation using [PokerHandEvaluator](https://github.com/HenryRLee/PokerHandEvaluator). |
| `poker_metrics` | Metrics to evaluate an entity's position in the poker game.               |
| `strategies`   | Player or strategy profiles.                                               |

**Note**: Detailed README files for each folder will be added in the future.

---

## Miscellaneous

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

NOTE: The building process might time out at times due to faulty connection or problems with debian repositories, just restart the building process.
NOTE: New files to poker_metrics/ and ./ should be manually added to the bind in docker-compose.yaml for it to be able to track it.

For docker hub:
To push:
`docker tag <name of the image> <dockerhub username>/<name of your repo>:<version>`
`docker push <tagged image name>:<version name>`

To pull:
`docker pull <tagged image name>:<version>`
