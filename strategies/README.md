# Strategies

There are two types of strategies,

1. **Action:** These strategies are trivial in nature and are very basic & simple.
2. **Rational:** These strategies have a sense of rationality among them.

## Rational Strategies

### Strategy.py

This is the main object that gives the strategy a sense of rationality. Here's how it works.

1. **Factoring in basic information:**
   When the decide function is called before taking a decision (prodigal or frugal), if new information is present as a parameter (or not an empty dictionary), the following are internalised as class attributes.
   - `seed` for the random functions.
   - `holeCards` & `communityCards`.
   - Current `round`.
   - `bigBlind` required for setting initial pot limit.
   - `callValue` required for finding pot odds.
   - `playerBetAmt` is the amount player have bet till that point.
   - `pot` current pot size.
2. **Setting initial pot:**
   Initial pot is the amount of that pot which occurs in the beginning of a specific round (pre-flop/flop/turn/river). This is done by calling the `self.setInitialPot()` method. It is to be calculated in two ways.
   1. **If round == 0:**
      When `round == 0`, the initial pot means the 2BB or 2 big blinds (actually it is 1SB + 1BB but for simplicity we will consider the pot to be taken in multiple of big blinds).
   2. **If round != 0:**
      Ideally in this scenario it is the value `pot - callValue` converted to nearest big blind but however this code is commented as it will not be required and instead a default of -1 will be the value.
      Note that this is only applicable for heads-up games.
3. **Setting round limiter:**
   1. If `round == 0` and `iniLimitMultiplier` is an integer, then `limit` (the maximum a player can bet in a round) is capped at `iniLimitMultiplier * initialPot`.
   2. Otherwise, it will set the limit with the `defaultLimit`.
4. **Reason the decision:**
   After preparation of the information, the `reason` method will be called to actually figure out more about the given information. It calculates the followings:
   1. privateValue/hand_strength/hs (`self.hs`).
   2. Inverts the hand_strength if `bluff > 0` and `self.hs < 0.5`.
   3. potential/sp (0 if `round in [0, 3]`)
   4. pot_odds/po
   5. `self.ll = self.po/(1 - self.po)`.
   6. `self.ul = self.sp + self.hs + self.risk`
   7. `t_determiner = self.ul - self.ll`
5. **Figure out appropriate move & bet size:**
   The appropriate move will be determined with `t_determiner`. Here's how it works,
   1. **`t_determiner <= 0:`** Out of money scenario - explicitly check/fold by setting `self.betAmt` as -1.
   2. **`t_determiner == 0:`** In this point strategy is in balanced position. Only call/check by returning 0.
   3. **`t_determiner > 0:`** In the money scenario. Get the odds `r` by calling the `odds` function in the `math_utils.py` and set the monetary value `pot * r` as bet amount `self.betAmt`.
6. **Limit the bet amount:**
   Limit the bet amount to the value of `self.limit` if bet amount is greater than limit by calling the `limiter` method.
   - If the bet amount is explicitly -1 or 0 (check/fold/call), then the `limiter` method passes.
   - Else,
     - It calculates the total current bet `tcb = betAmt + playerBetAmt` which is the bet size that player raised/made till this point.
     - If the `tcb > limit`,
       - It calculates the required bet `req = callValue + playerBetAmt` to stay in the game.
       - If `req > limit` then limit has been passed and makes the player forcefully call by setting `betAmt` to 0.
       - Else it sets the `betAmt = limit - playerBetAmt`.
7. **Convert bet amount to to blinds:**
   The `toBlinds` method is then called to convert the bet amount to to the nearest multiple of big blind (if the bet amount is not equal to -1 or 0, indicating check/fold/call).
8. **Set the appropriate move:**
   Finally, an appropriate move is decided by calling the `setMove` method.
