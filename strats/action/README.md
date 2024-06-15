# Action Based Strategies

This strategies only return actions based on a specific predictable pattern.

1. `alwaysFold`: Folds no matter what.
2. `cooperative`: Always cooperate with the opponent/system.
3. `defective`: Always defects the opponent/system.
4. `grim`: Starts by cooperating. But if opponent/system defects then it always defects.
5. `random`: Random moves.
6. `tit_for_tat`: Takes the opponent's last action.
7. `generous_tit_for_tat`: Takes the opponent's last action except it might be more lenient on being defective (i.e, it can sometimes cooperate when the opponent's last move was to defect).
