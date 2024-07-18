# Strategies

## Types

There are two types of strategies. Action based and rational strategies.

1. Action based strategies takes decision on a specific pattern, inspired from Axelrod's work.
2. Rational strategies considers the unknown or imperfect information available in the game and then takes decision.

## Action Based Strategies

These strategies takes decision without any consideration for information.

### alwaysFold

Just fold every single time.

### Cooperative

Always checks/calls.

### Defective

Always raises/bets.

### Grim

Starts by checking/calling. However, if opponent even raises/bets once, it always raises/bets after that.

#### Tit For Tat

Replicates the opponents last action else checks/calls.

#### Generous Tit For Tat

Replicates the opponents last action else checks/calls. However, if the opponent raised against it, it may randomly choose to pardon that and check.

#### Random (With Fold)

Takes a random valid move.

#### Random (No Fold)

Takes a random valid move apart from fold.

## Rational Strategies

Rational Strategies takes decision based upon the available imperfect information.

### Basic Setup

1. All the strategies are the child class of the `Strategy` parent class in `Strategy.py`.
2. They share the same rationality (determined by the signal function).
3. Point to note over here is that their decide function is different.

Basically, this setup helps us to study the decision taken by rational agents if they have the same intelligence or knowledge.

### The Strategies

#### Ideal

These strategies do not deviate from the overall rationality and takes the ideal decision given by the signal function in all scenarios. For example,

```algorithm
    SignalRange > 0.85:
        Bet/Raise
    SignalRange > 0.35:
        Check/Call
    Else:
        Fold
```

**Note:** This is just an overview of what happens inside the ideal strategy.

Now these strategies are itself divided into 5 strategies, indicative of their tightness, ranging from `very_loose` to `very_tight` with `balanced` being the one with moderate tightness.

In this scenario, the 5 strategies has different brackets for `signalRange` to make the decision.

#### Changing_Styles

This strategy, given that it is a scenario to not fold (surrender), takes random move.

It can take any of the following move,

1. Randomly make a prodigal (bet/raise) or a frugal (check/call) move.
2. Randomly overbet, underbet or equally bet.
3. Randomly changes it's tightness.

#### Bluff

The bluff has the following characteristics.

1. Given that it is not a scenario to fold, it plays as it should while semi-bluffing with a good hand.
2. If it is a scenario to fold, it bluffs.

**How does it makes the decision to bluff?** It calculates the probability that an opponent folds when the strategy has raised earlier. If the probability is greater than 0.55, then it bluffs aggressively. Otherwise it still bluffs but in a conservative fashion and randomly.

#### Check_Raise

This strategy has the following characteristics given that it has an exceptional hand.

1. If the probability that opponent raises is above than 0.55, it checks/calls.
2. When the opponent raises, it raises aggressively to stuck opponent bets.

However, if it does not have an exceptional hand, it will not deviate from the ideal behaviour.

#### Slowplaying

This strategy has the following characteristics given that it has an exceptional hand.

1. Plays the first round where the emergence of an exceptional hand occurred very weakly (check/call only).
2. If the hand is still exception in the next round (which it should be most of times), it plays according to the ideal behaviour (whish is to raise/bet) with the option to bet a bit aggresively.
3. Else it plays according to the ideal behaviour.

## Parameters
### non-bluffing strategies

| Name | r_shift | l_shift | risk |
| ---- | ---- | ---- | ---- |
| balanced | 0 | 0 | 0 |
| balanced_low_risk | 0 | 0 | 0.2 |
| balanced_medium_risk | 0 | 0 | 0.6 |
| belanced_high_risk | 0 | 0 | 1 |
| loose | 0.5 | 0 | 0 |
| loose_low_risk | 0.5 | 0 | 0.2 |
| loose_medium_risk | 0.5 | 0 | 0.6 |
| loose_high_risk | 0.5 | 0 | 1 |
| tight | 0 | 0.5 | 0 |
| tight_low_risk | 0 | 0.5 | 0.2 |
| tight_medium_risk | 0 | 0.5 | 0.6 |
| tight_high_risk | 0 | 0.5 | 1 |
| very_loose | 1 | 0 | 0 |
| very_loose_low_risk | 1 | 0 | 0.2 |
| very_loose_medium_risk | 1 | 0 | 0.6 |
| very_loose_high_risk | 1 | 0 | 1 |
| very_tight | 0 | 1 | 0 |
| very_tight_low_risk | 0 | 1 | 0.2 |
| very_tight_medium_risk | 0 | 1 | 0.6 |
| very_tight_high_risk | 0 | 1 | 1 |

### bluffing strategies (bluff == True)

| Name | r_shift | l_shift | risk |
| ---- | ---- | ---- | ---- |
| bluff | 0 | 0 | 0 |
| bluff_1 | 0.5 | 0 | 0.5 |
| bluff_2 | 1 | 0 | 1 |
