# Humane Strategies

These are the strategies that are inspired from how humans play poker. (Section 3.6: Deception and Unpredictability of Master Thesis: Dealing with Imperfect Information in Poker).

## Changing Styles

This strategy will change playing style (tight/loose) sensibly (i.e, like how a human might play poker).

### Algorithm

```algorithm
# True for defective, false for cooperative.
STYLE = RANDOM(TRUE/FALSE)

IF SIGNAL:
    IF STYLE:
        RETURN defectiveMove
    RETURN cooperativeMove

RETURN fold
```

This in essence is the human version (and arguably the true version) of random.

## Slowplaying

"It is playing a hand weakly on one round of betting to suck people in for later bets".

### Algorithm

```algorithm
IF SIGNAL:
    IF Round == 0 (Or any other different round):
        RETURN cooperativeMove
    ELSE:
        RETURN defectiveMove
```

## Check-Raising

...

## Bluffing

Basic idea is to predict the probability that opponent will call-in in order to identify profitable opportunities and over-play weak hands.

### Algorithm

```algorithm
IF SIGNAL:
    RETURN defectiveMove
ELSE:
    IF opponentWillCall:
        RETURN defectiveMove

    RETURN fold
```

## Semi-Bluffing

Bet with a hand which is not likely to be the best hand at the moment but has a good chance of outdrawing calling hands.

### Algorithm

```algorithm
IF SIGNAL:
    IF HandPotential == "GOOD":
        RETURN defectiveMove

    RETURN cooperativeMove

RETURN fold
```
