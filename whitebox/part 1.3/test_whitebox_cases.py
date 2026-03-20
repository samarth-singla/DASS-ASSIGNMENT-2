"""White-box tests for MoneyPoly (Part 1.3)."""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

# Add whitebox/part 1.2/moneypoly to import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1] / "part 1.2" / "moneypoly"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from moneypoly.bank import Bank
from moneypoly.cards import CardDeck
from moneypoly.config import GO_SALARY, JAIL_FINE
from moneypoly.dice import Dice
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup


class TestWhiteBoxCases(unittest.TestCase):
    """Branch, state, and edge-case tests derived from source control flow."""

    def test_bank_collect_negative_is_ignored(self):
        """Negative collection should not change reserves."""
        bank = Bank()
        start = bank.get_balance()
        bank.collect(-50)
        self.assertEqual(bank.get_balance(), start)

    def test_give_loan_reduces_bank_reserves(self):
        """Loan payout should increase player funds and decrease bank funds."""
        bank = Bank()
        player = Player("A")
        start_bank = bank.get_balance()
        start_player = player.balance

        bank.give_loan(player, 125)

        self.assertEqual(player.balance, start_player + 125)
        self.assertEqual(bank.get_balance(), start_bank - 125)

    def test_player_move_passing_go_grants_salary(self):
        """Wrapping around board should award Go salary."""
        player = Player("A")
        player.position = 39
        start_balance = player.balance

        player.move(2)

        self.assertEqual(player.position, 1)
        self.assertEqual(player.balance, start_balance + GO_SALARY)

    def test_jail_voluntary_fine_deducts_player_balance(self):
        """Choosing to pay jail fine should deduct player and credit bank."""
        game = Game(["A", "B"])
        player = game.players[0]
        player.in_jail = True
        player.jail_turns = 0
        start_balance = player.balance
        start_bank = game.bank.get_balance()

        with patch("moneypoly.ui.confirm", return_value=True), patch.object(
            game.dice, "roll", return_value=3
        ), patch.object(game, "_move_and_resolve", return_value=None):
            game._handle_jail_turn(player)

        self.assertEqual(player.balance, start_balance - JAIL_FINE)
        self.assertEqual(game.bank.get_balance(), start_bank + JAIL_FINE)
        self.assertFalse(player.in_jail)
        self.assertEqual(player.jail_turns, 0)

    def test_trade_credits_seller(self):
        """Trade cash should move from buyer to seller and transfer ownership."""
        game = Game(["A", "B"])
        seller, buyer = game.players[0], game.players[1]
        prop = game.board.properties[0]
        prop.owner = seller
        seller.add_property(prop)
        start_seller = seller.balance
        start_buyer = buyer.balance

        success = game.trade(seller, buyer, prop, 150)

        self.assertTrue(success)
        self.assertEqual(buyer.balance, start_buyer - 150)
        self.assertEqual(seller.balance, start_seller + 150)
        self.assertEqual(prop.owner, buyer)

    def test_empty_deck_cards_remaining_is_zero(self):
        """cards_remaining should be safe and return 0 for an empty deck."""
        deck = CardDeck([])
        self.assertEqual(deck.cards_remaining(), 0)

    def test_empty_deck_repr_does_not_crash(self):
        """Representing an empty deck should not raise exceptions."""
        deck = CardDeck([])
        repr_text = repr(deck)
        self.assertIn("CardDeck(0 cards", repr_text)

    def test_empty_property_group_is_not_fully_owned(self):
        """An empty property group should not count as fully owned."""
        group = PropertyGroup("Test", "test")
        player = Player("A")
        self.assertFalse(group.all_owned_by(player))

    def test_net_worth_includes_property_values(self):
        """Net worth should include both cash and owned property prices."""
        player = Player("A")
        prop = Property("Test", 1, 200, 10)
        player.add_property(prop)
        self.assertEqual(player.net_worth(), player.balance + 200)

    def test_buy_property_rejects_already_owned_tile(self):
        """Buying an already-owned property should fail and keep ownership."""
        game = Game(["A", "B"])
        owner = game.players[0]
        buyer = game.players[1]
        prop = game.board.properties[0]
        prop.owner = owner
        owner.add_property(prop)
        buyer_start_balance = buyer.balance

        success = game.buy_property(buyer, prop)

        self.assertFalse(success)
        self.assertEqual(prop.owner, owner)
        self.assertEqual(buyer.balance, buyer_start_balance)

    def test_dice_roll_values_are_between_1_and_6(self):
        """Every die face should always stay within the standard range 1..6."""
        dice = Dice()
        for _ in range(200):
            dice.roll()
            self.assertTrue(1 <= dice.die1 <= 6)
            self.assertTrue(1 <= dice.die2 <= 6)

    def test_find_winner_returns_highest_net_worth_player(self):
        """Winner selection should pick the maximum net-worth player."""
        game = Game(["A", "B"])
        game.players[0].balance = 100
        game.players[1].balance = 300
        winner = game.find_winner()
        self.assertEqual(winner, game.players[1])

    def test_buy_property_allows_exact_balance(self):
        """A player with exactly the property price should be able to buy it."""
        game = Game(["A", "B"])
        buyer = game.players[0]
        prop = game.board.properties[1]
        buyer.balance = prop.price

        success = game.buy_property(buyer, prop)

        self.assertTrue(success)
        self.assertEqual(prop.owner, buyer)
        self.assertEqual(buyer.balance, 0)

    def test_pay_rent_transfers_to_owner(self):
        """Rent payment should reduce renter cash and increase owner cash."""
        game = Game(["A", "B"])
        owner, renter = game.players[0], game.players[1]
        prop = game.board.properties[2]
        prop.owner = owner
        owner.add_property(prop)
        owner_start = owner.balance
        renter_start = renter.balance
        rent = prop.get_rent()

        game.pay_rent(renter, prop)

        self.assertEqual(renter.balance, renter_start - rent)
        self.assertEqual(owner.balance, owner_start + rent)


if __name__ == "__main__":
    unittest.main(verbosity=2)
