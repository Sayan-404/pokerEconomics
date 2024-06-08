import unittest
from unittest.mock import MagicMock, patch
from Game import Game
from Player import Player

import engines.engine as engine


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.test_player = Player(1, 1000)

    def test_package_state(self):
        state = self.test_player.package_state()

        self.assertDictEqual(
            {
                "id": 1,
                "hand": [],
                "bankroll": 1000,
                "betamt": 0,
                "ingame": 1,
                "strategy": "",
            },
            state,
        )

    def test_receive_card(self):
        self.test_player.receive_card()


# class TestEngine(unittest.TestCase):

#     def setUp(self):
#         players

# AI Generated Tests for reference

# class TestGame(unittest.TestCase):

#     def setUp(self):
#         self.players = [MagicMock(), MagicMock(), MagicMock()]
#         for i, player in enumerate(self.players):
#             player.id = f"Player{i}"
#             player.bankroll = 1000
#             player.ingame = 1
#             player.betamt = 0
#             player.package_state.return_value = {}

#         self.logger = MagicMock()
#         self.deck = MagicMock()
#         self.showdown = MagicMock()
#         self.game = Game(self.players, self.logger, simul=True)

#     def test_initial_setup(self):
#         self.assertEqual(self.game.pot, 0)
#         self.assertEqual(self.game.number_of_players, len(self.players))
#         self.assertEqual(self.game.community_cards, [])
#         self.assertEqual(self.game.round, 0)
#         self.assertEqual(self.game.hand_number, 0)
#         self.assertEqual(self.game.all_in, 0)
#         self.assertEqual(self.game.playing, len(self.players))

#     def test_get_max_bet(self):
#         self.players[0].bankroll = 500
#         self.players[1].bankroll = 800
#         self.players[2].bankroll = 300

#         max_bet = self.game.get_max_bet(0)
#         self.assertEqual(max_bet, 300)

#         max_bet = self.game.get_max_bet(1)
#         self.assertEqual(max_bet, 500)

#     def test_package_state(self):
#         self.players[0].package_state.return_value = {"player_state": "state0"}
#         self.players[1].package_state.return_value = {"player_state": "state1"}
#         self.players[2].package_state.return_value = {"player_state": "state2"}

#         state = self.game.package_state(0)
#         self.assertEqual(state["player"], {"player_state": "state0"})
#         self.assertEqual(state["call_value"], 0)
#         self.assertEqual(state["players_playing"], 3)
#         self.assertEqual(state["players"], self.players)
#         self.assertEqual(state["community_cards"], [])
#         self.assertEqual(state["pot"], 0)
#         self.assertEqual(state["round"], 0)
#         self.assertEqual(state["max_bet"], 300)

#     def test_flush(self):
#         self.game.community_cards = ["card1", "card2"]
#         self.game.round = 2
#         self.game.playing = 2
#         self.game.all_in = 1

#         self.game.flush()

#         self.game.deck.flush.assert_called_once()
#         for player in self.players:
#             player.flush.assert_called_once()
#         self.assertEqual(self.game.community_cards, [])
#         self.assertEqual(self.game.round, 0)
#         self.assertEqual(self.game.playing, 3)
#         self.assertEqual(self.game.all_in, 0)

#     def test_sub_play_insufficient_players(self):
#         self.players[0].bankroll = 0
#         self.players[1].bankroll = 0

#         with patch("builtins.print") as mocked_print:
#             result = self.game.sub_play(1)
#             mocked_print.assert_called_once_with("Insufficient players", hand_number=1)
#             self.assertEqual(result, 0)

#     def test_sub_play_sufficient_players(self):
#         self.players[0].bankroll = 100
#         self.players[1].bankroll = 100
#         self.players[2].bankroll = 0

#         self.game.preflop = MagicMock()
#         self.game.flush = MagicMock()

#         with patch("builtins.print") as mocked_print:
#             result = self.game.sub_play(1)
#             mocked_print.assert_any_call(f"Player0: 100", hand_number=1)
#             mocked_print.assert_any_call(f"Player1: 100", hand_number=1)
#             mocked_print.assert_any_call(f"Player2: 0", hand_number=1)
#             self.game.preflop.assert_called_once()
#             self.game.flush.assert_called_once()
#             self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
