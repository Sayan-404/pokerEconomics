# Strategies

In the initial round (pre-flop), even if the call value is 0, by the rules of poker, one will have to raise if they are the BB or SB.

## State contents

```json
{
            "player": {
                "id": self.id,
                "hand": self.hand,
                "bankroll": self.bankroll,
                "betamt": self.betamt,
                "ingame": self.ingame,
            },
            "players": self.players,
            "call_value": call_value,
            "players_playing": len(self.players),
            "community_cards": self.community_cards,
            "pot": self.pot,
            "round": self.round,
            "max_bet": self.get_max_bet(player_index),
}
```
if max_bet <= bankroll go all in