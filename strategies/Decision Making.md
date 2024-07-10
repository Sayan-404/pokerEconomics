# Decision Making in Rational Strategies

## Decision Making factors

1. `x_private_value`: ...
1. `y_hand_equity`: ...
1. `z_pot_odds`: ...
1. `t_determiner`: ...
1. `range`: ...
1. `monetary_range`: ...
1. `strength`: This is x (private value) or y (hand equity) depending on the round.
1. `potShare`: Share of a player's total bet in pot. Formula, `(Player Total Amount Bet)/(Pot Size)`

## Algorithm (#1) for Calculating Decision Making Factors

```algortihm
strength = -1

// Determine x as it will be required for making an action
IF round != 0:
	x_private_value = privateValue(hole_cards, comm_cards)
ELSE:
	x_private_value = incomeRate(hole_cards)

// Determine the required strength dynamically
IF (round == 0) OR (round == 3):
	strength = x_private_value
ELSE:
	strength = y_hand_equity = potential(hole_cards, comm_cards)

IF (callValue > 0):
	z_pot_odds = (callValue/(potSize + callValue))
	t_determiner = strength - z_pot_odds
	range = [z_pot_odds, strength]
ELSE:
	// Call value is 0
	potShare = PlayerTotalBetAmt/PotSize
	t_determiner = strength - potShare
	range = [0, strength]
```

This algorithm is embodied in the reason() method of the strategy class.

## Algorithm (#2) for Calculating MonetaryRange and Appropriate Move

```algorithm
function strategicMove(r):
	// r is a number in range
	// It will be provided by individual strategies
	monetaryRange = floor((r*potSize)/(1-r))

	IF monetaryRange == callValue:
		// This will happen when strategy provided r as the lower limit of the range
		return frugalMove
	IF monetaryRange > callValue:
		return prodigalMove(betAmt = r)
	ELSE:
		// When monetary range is less than callvalue (which is not possible)
		return fold
```

This algorithm is embodied in the `strategicMoves()` method of the strategy class.

## Algorithm (#3) for Making a Decision

```algorithm
IF t_determiner >= 0:
	// In the money scenario
	IF x_private_value > strong_factor:
		r = higher value from range OR value above range upper limit
	else:
		r = lower value from range
ELSE:
	// t < 0 scenario
	// Out of money
	IF (x_private_value > strong_factor) AND ((round == 2) OR (round == 3)):
		r = higher value from range OR value above range upper limit
	ELSE:
		r = lower limit of the range 	// as this will give a frugalMove
```

This is the basis of all strategies, specifically a similar format can be expected in all the strategy's decide function. Each strategies are required to define their,

1. `strong_factor`: The floating point number above which their private value is considered to be strong as per the strategy's behaviour.
1. `r`: The specific `r` to select from the range is to be tweaked as per the strategy's behaviour.

## Overall Workflow of Strategies

```
[Run the initialise method before making decision]->
[Initialise method determines the decision factors with #1 by running reason method]->
[The Factors are saved as class attributes]->
[Determine the r with #3 in the strategy's decide method]->
[Determine the appropriate move with #2, i.e., by giving r to strategicMoves() method]
```

## Notes

1. All the decision factors are now attributes of the strategy such that children classes (actual strategies like bluff) can get access to the factors and determine their `r` and make decision based on their behaviour.
2. Signal function axed.
3. **Points to check,**
   1. Is it valid to consider income rate as a substitute for `x_private_value` in #1?
   1. Is the `t_determiner` from `strength - potShare` valid for making judgements when `callvalue == 0` in #1?
   1. Is it valid to fold when `monetaryRange < callValue` in #2?
