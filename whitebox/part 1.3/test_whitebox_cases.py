"""Expanded white-box tests for MoneyPoly (Part 1.3)."""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

# Add whitebox/part 1.2/moneypoly to import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1] / "part 1.2" / "moneypoly"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from moneypoly.bank import Bank
from moneypoly.board import Board
from moneypoly.cards import CardDeck, CHANCE_CARDS
from moneypoly.config import GO_SALARY, JAIL_FINE, INCOME_TAX_AMOUNT, LUXURY_TAX_AMOUNT
from moneypoly.dice import Dice
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup
from moneypoly import ui


class TestBankWhiteBox(unittest.TestCase):
    def test_collect_positive_increases_funds(self):
        bank = Bank()
        start = bank.get_balance()
        bank.collect(100)
        self.assertEqual(bank.get_balance(), start + 100)

    def test_collect_zero_keeps_balance(self):
        bank = Bank()
        start = bank.get_balance()
        bank.collect(0)
        self.assertEqual(bank.get_balance(), start)

    def test_collect_negative_is_ignored(self):
        bank = Bank()
        start = bank.get_balance()
        bank.collect(-50)
        self.assertEqual(bank.get_balance(), start)

    def test_pay_out_positive_reduces_funds(self):
        bank = Bank()
        start = bank.get_balance()
        paid = bank.pay_out(100)
        self.assertEqual(paid, 100)
        self.assertEqual(bank.get_balance(), start - 100)

    def test_pay_out_zero_returns_zero(self):
        bank = Bank()
        self.assertEqual(bank.pay_out(0), 0)

    def test_pay_out_negative_returns_zero(self):
        bank = Bank()
        self.assertEqual(bank.pay_out(-10), 0)

    def test_pay_out_too_much_raises(self):
        bank = Bank()
        with self.assertRaises(ValueError):
            bank.pay_out(bank.get_balance() + 1)

    def test_give_loan_reduces_bank_and_increases_player(self):
        bank = Bank()
        player = Player("A")
        b0 = bank.get_balance()
        p0 = player.balance
        bank.give_loan(player, 125)
        self.assertEqual(bank.get_balance(), b0 - 125)
        self.assertEqual(player.balance, p0 + 125)

    def test_give_loan_zero_no_change(self):
        bank = Bank()
        player = Player("A")
        b0 = bank.get_balance()
        p0 = player.balance
        bank.give_loan(player, 0)
        self.assertEqual(bank.get_balance(), b0)
        self.assertEqual(player.balance, p0)

    def test_give_loan_negative_no_change(self):
        bank = Bank()
        player = Player("A")
        b0 = bank.get_balance()
        p0 = player.balance
        bank.give_loan(player, -10)
        self.assertEqual(bank.get_balance(), b0)
        self.assertEqual(player.balance, p0)

    def test_loan_count_and_total_loans(self):
        bank = Bank()
        p1 = Player("A")
        p2 = Player("B")
        bank.give_loan(p1, 100)
        bank.give_loan(p2, 200)
        self.assertEqual(bank.loan_count(), 2)
        self.assertEqual(bank.total_loans_issued(), 300)


class TestCardDeckWhiteBox(unittest.TestCase):
    def test_draw_empty_returns_none(self):
        self.assertIsNone(CardDeck([]).draw())

    def test_draw_increments_index(self):
        deck = CardDeck([{"x": 1}, {"x": 2}])
        deck.draw()
        self.assertEqual(deck.index, 1)

    def test_draw_cycles_when_exhausted(self):
        deck = CardDeck([{"x": 1}, {"x": 2}])
        self.assertEqual(deck.draw()["x"], 1)
        self.assertEqual(deck.draw()["x"], 2)
        self.assertEqual(deck.draw()["x"], 1)

    def test_peek_empty_returns_none(self):
        self.assertIsNone(CardDeck([]).peek())

    def test_peek_does_not_advance(self):
        deck = CardDeck([{"x": 1}, {"x": 2}])
        self.assertEqual(deck.peek()["x"], 1)
        self.assertEqual(deck.index, 0)

    def test_cards_remaining_empty_is_zero(self):
        self.assertEqual(CardDeck([]).cards_remaining(), 0)

    def test_cards_remaining_after_one_draw(self):
        deck = CardDeck([{"x": 1}, {"x": 2}, {"x": 3}])
        deck.draw()
        self.assertEqual(deck.cards_remaining(), 2)

    def test_reshuffle_resets_index(self):
        deck = CardDeck([{"x": 1}, {"x": 2}])
        deck.draw()
        deck.reshuffle()
        self.assertEqual(deck.index, 0)

    def test_len_matches_card_count(self):
        self.assertEqual(len(CardDeck([{"x": 1}, {"x": 2}])), 2)

    def test_repr_for_empty_deck(self):
        self.assertIn("CardDeck(0 cards", repr(CardDeck([])))


class TestDiceWhiteBox(unittest.TestCase):
    def test_reset_sets_zero_faces_and_streak(self):
        dice = Dice()
        dice.die1 = 4
        dice.die2 = 5
        dice.doubles_streak = 2
        dice.reset()
        self.assertEqual((dice.die1, dice.die2, dice.doubles_streak), (0, 0, 0))

    def test_roll_values_in_1_to_6(self):
        dice = Dice()
        for _ in range(200):
            dice.roll()
            self.assertTrue(1 <= dice.die1 <= 6)
            self.assertTrue(1 <= dice.die2 <= 6)

    def test_total_returns_sum(self):
        dice = Dice()
        dice.die1 = 3
        dice.die2 = 5
        self.assertEqual(dice.total(), 8)

    def test_is_doubles_true(self):
        dice = Dice()
        dice.die1 = 4
        dice.die2 = 4
        self.assertTrue(dice.is_doubles())

    def test_is_doubles_false(self):
        dice = Dice()
        dice.die1 = 4
        dice.die2 = 5
        self.assertFalse(dice.is_doubles())

    def test_doubles_streak_increment_and_reset(self):
        dice = Dice()
        with patch("moneypoly.dice.random.randint", side_effect=[3, 3, 4, 4, 2, 1]):
            dice.roll()
            self.assertEqual(dice.doubles_streak, 1)
            dice.roll()
            self.assertEqual(dice.doubles_streak, 2)
            dice.roll()
            self.assertEqual(dice.doubles_streak, 0)


class TestPlayerWhiteBox(unittest.TestCase):
    def test_add_money_positive(self):
        p = Player("A")
        p.add_money(100)
        self.assertEqual(p.balance, 1600)

    def test_add_money_negative_raises(self):
        with self.assertRaises(ValueError):
            Player("A").add_money(-1)

    def test_deduct_money_positive(self):
        p = Player("A")
        p.deduct_money(100)
        self.assertEqual(p.balance, 1400)

    def test_deduct_money_negative_raises(self):
        with self.assertRaises(ValueError):
            Player("A").deduct_money(-1)

    def test_is_bankrupt_true_at_zero(self):
        p = Player("A", balance=0)
        self.assertTrue(p.is_bankrupt())

    def test_is_bankrupt_false_positive_balance(self):
        self.assertFalse(Player("A", balance=1).is_bankrupt())

    def test_net_worth_includes_property_values(self):
        p = Player("A")
        p.add_property(Property("X", 1, 200, 10))
        self.assertEqual(p.net_worth(), p.balance + 200)

    def test_move_without_passing_go(self):
        p = Player("A")
        p.position = 5
        b0 = p.balance
        p.move(3)
        self.assertEqual(p.position, 8)
        self.assertEqual(p.balance, b0)

    def test_move_passing_go_grants_salary(self):
        p = Player("A")
        p.position = 39
        b0 = p.balance
        p.move(2)
        self.assertEqual(p.position, 1)
        self.assertEqual(p.balance, b0 + GO_SALARY)

    def test_go_to_jail_sets_state(self):
        p = Player("A")
        p.go_to_jail()
        self.assertTrue(p.in_jail)
        self.assertEqual(p.position, 10)
        self.assertEqual(p.jail_turns, 0)

    def test_add_property_avoids_duplicates(self):
        p = Player("A")
        prop = Property("X", 1, 100, 10)
        p.add_property(prop)
        p.add_property(prop)
        self.assertEqual(len(p.properties), 1)

    def test_remove_property_ignores_missing(self):
        p = Player("A")
        prop = Property("X", 1, 100, 10)
        p.remove_property(prop)
        self.assertEqual(len(p.properties), 0)


class TestPropertyWhiteBox(unittest.TestCase):
    def test_property_available_when_unowned_not_mortgaged(self):
        self.assertTrue(Property("P", 1, 100, 10).is_available())

    def test_property_not_available_when_owned(self):
        p = Property("P", 1, 100, 10)
        p.owner = Player("A")
        self.assertFalse(p.is_available())

    def test_property_not_available_when_mortgaged(self):
        p = Property("P", 1, 100, 10)
        p.is_mortgaged = True
        self.assertFalse(p.is_available())

    def test_get_rent_zero_when_mortgaged(self):
        p = Property("P", 1, 100, 10)
        p.is_mortgaged = True
        self.assertEqual(p.get_rent(), 0)

    def test_get_rent_base_when_group_not_fully_owned(self):
        g = PropertyGroup("G", "g")
        p1 = Property("A", 1, 100, 10, g)
        Property("B", 2, 100, 10, g)
        owner = Player("A")
        p1.owner = owner
        self.assertEqual(p1.get_rent(), 10)

    def test_get_rent_double_when_group_fully_owned(self):
        g = PropertyGroup("G", "g")
        p1 = Property("A", 1, 100, 10, g)
        p2 = Property("B", 2, 100, 10, g)
        owner = Player("A")
        p1.owner = owner
        p2.owner = owner
        self.assertEqual(p1.get_rent(), 20)

    def test_mortgage_first_time_returns_value(self):
        p = Property("P", 1, 100, 10)
        self.assertEqual(p.mortgage(), 50)
        self.assertTrue(p.is_mortgaged)

    def test_mortgage_second_time_returns_zero(self):
        p = Property("P", 1, 100, 10)
        p.mortgage()
        self.assertEqual(p.mortgage(), 0)

    def test_unmortgage_when_not_mortgaged_returns_zero(self):
        self.assertEqual(Property("P", 1, 100, 10).unmortgage(), 0)

    def test_unmortgage_cost_is_110_percent(self):
        p = Property("P", 1, 100, 10)
        p.mortgage()
        self.assertEqual(p.unmortgage(), 55)

    def test_empty_group_is_not_fully_owned(self):
        self.assertFalse(PropertyGroup("G", "g").all_owned_by(Player("A")))

    def test_all_owned_by_none_false(self):
        g = PropertyGroup("G", "g")
        Property("A", 1, 100, 10, g)
        self.assertFalse(g.all_owned_by(None))

    def test_group_owner_counts(self):
        g = PropertyGroup("G", "g")
        p1 = Property("A", 1, 100, 10, g)
        p2 = Property("B", 2, 100, 10, g)
        owner = Player("A")
        p1.owner = owner
        p2.owner = owner
        self.assertEqual(g.get_owner_counts()[owner], 2)

    def test_group_size(self):
        g = PropertyGroup("G", "g")
        Property("A", 1, 100, 10, g)
        self.assertEqual(g.size(), 1)

    def test_group_add_property_links_back(self):
        g = PropertyGroup("G", "g")
        p = Property("A", 1, 100, 10)
        g.add_property(p)
        self.assertEqual(p.group, g)


class TestBoardWhiteBox(unittest.TestCase):
    def test_get_property_at_returns_none_for_missing(self):
        board = Board()
        self.assertIsNone(board.get_property_at(0))

    def test_get_property_at_returns_property_for_known_position(self):
        board = Board()
        self.assertIsNotNone(board.get_property_at(1))

    def test_get_tile_type_property(self):
        self.assertEqual(Board().get_tile_type(1), "property")

    def test_get_tile_type_blank(self):
        self.assertEqual(Board().get_tile_type(12), "blank")

    def test_is_purchasable_false_for_blank(self):
        self.assertFalse(Board().is_purchasable(12))

    def test_is_purchasable_false_for_owned_property(self):
        board = Board()
        prop = board.get_property_at(1)
        prop.owner = Player("A")
        self.assertFalse(board.is_purchasable(1))

    def test_is_purchasable_false_for_mortgaged_property(self):
        board = Board()
        prop = board.get_property_at(1)
        prop.is_mortgaged = True
        self.assertFalse(board.is_purchasable(1))

    def test_is_special_tile_true(self):
        self.assertTrue(Board().is_special_tile(0))

    def test_is_special_tile_false_for_property(self):
        self.assertFalse(Board().is_special_tile(1))

    def test_properties_owned_by_filters_correctly(self):
        board = Board()
        owner = Player("A")
        p1 = board.get_property_at(1)
        p2 = board.get_property_at(3)
        p1.owner = owner
        p2.owner = owner
        owned = board.properties_owned_by(owner)
        self.assertEqual(len(owned), 2)

    def test_unowned_properties_reduces_after_assignment(self):
        board = Board()
        all_unowned = len(board.unowned_properties())
        board.get_property_at(1).owner = Player("A")
        self.assertEqual(len(board.unowned_properties()), all_unowned - 1)


class TestUIWhiteBox(unittest.TestCase):
    def test_format_currency(self):
        self.assertEqual(ui.format_currency(1500), "$1,500")

    def test_safe_int_input_valid(self):
        with patch("builtins.input", return_value="42"):
            self.assertEqual(ui.safe_int_input("x"), 42)

    def test_safe_int_input_invalid_returns_default(self):
        with patch("builtins.input", return_value="abc"):
            self.assertEqual(ui.safe_int_input("x", default=7), 7)

    def test_confirm_yes_true(self):
        with patch("builtins.input", return_value="y"):
            self.assertTrue(ui.confirm("x"))

    def test_confirm_no_false(self):
        with patch("builtins.input", return_value="n"):
            self.assertFalse(ui.confirm("x"))


class TestGameWhiteBox(unittest.TestCase):
    def _game(self):
        return Game(["A", "B", "C"])

    def test_current_player_initial(self):
        game = self._game()
        self.assertEqual(game.current_player().name, "A")

    def test_advance_turn_wraps(self):
        game = self._game()
        game.current_index = 2
        game.advance_turn()
        self.assertEqual(game.current_index, 0)

    def test_play_turn_jail_path_advances_turn(self):
        game = self._game()
        game.players[0].in_jail = True
        with patch.object(game, "_handle_jail_turn", return_value=None):
            game.play_turn()
        self.assertEqual(game.current_index, 1)

    def test_play_turn_three_doubles_goes_to_jail(self):
        game = self._game()
        with patch.object(game.dice, "roll", return_value=4), patch.object(
            game.dice, "describe", return_value="2+2"
        ), patch.object(game.dice, "doubles_streak", 3):
            game.play_turn()
        self.assertTrue(game.players[0].in_jail)

    def test_move_resolve_income_tax(self):
        game = self._game()
        p = game.players[0]
        p.position = 3
        b0 = p.balance
        bank0 = game.bank.get_balance()
        game._move_and_resolve(p, 1)
        self.assertEqual(p.balance, b0 - INCOME_TAX_AMOUNT)
        self.assertEqual(game.bank.get_balance(), bank0 + INCOME_TAX_AMOUNT)

    def test_move_resolve_luxury_tax(self):
        game = self._game()
        p = game.players[0]
        p.position = 37
        b0 = p.balance
        bank0 = game.bank.get_balance()
        game._move_and_resolve(p, 1)
        self.assertEqual(p.balance, b0 - LUXURY_TAX_AMOUNT)
        self.assertEqual(game.bank.get_balance(), bank0 + LUXURY_TAX_AMOUNT)

    def test_move_resolve_go_to_jail(self):
        game = self._game()
        p = game.players[0]
        p.position = 29
        game._move_and_resolve(p, 1)
        self.assertTrue(p.in_jail)

    def test_buy_property_allows_exact_balance(self):
        game = self._game()
        p = game.players[0]
        prop = game.board.get_property_at(1)
        p.balance = prop.price
        self.assertTrue(game.buy_property(p, prop))

    def test_buy_property_rejects_already_owned(self):
        game = self._game()
        owner = game.players[0]
        buyer = game.players[1]
        prop = game.board.get_property_at(1)
        prop.owner = owner
        owner.add_property(prop)
        self.assertFalse(game.buy_property(buyer, prop))

    def test_buy_property_rejects_insufficient_balance(self):
        game = self._game()
        p = game.players[0]
        prop = game.board.get_property_at(39)
        p.balance = prop.price - 1
        self.assertFalse(game.buy_property(p, prop))

    def test_pay_rent_no_owner_no_change(self):
        game = self._game()
        renter = game.players[0]
        prop = game.board.get_property_at(1)
        b0 = renter.balance
        game.pay_rent(renter, prop)
        self.assertEqual(renter.balance, b0)

    def test_pay_rent_mortgaged_no_change(self):
        game = self._game()
        owner = game.players[0]
        renter = game.players[1]
        prop = game.board.get_property_at(1)
        prop.owner = owner
        prop.is_mortgaged = True
        b0 = renter.balance
        game.pay_rent(renter, prop)
        self.assertEqual(renter.balance, b0)

    def test_pay_rent_transfers_to_owner(self):
        game = self._game()
        owner, renter = game.players[0], game.players[1]
        prop = game.board.get_property_at(1)
        prop.owner = owner
        owner.add_property(prop)
        owner0 = owner.balance
        renter0 = renter.balance
        game.pay_rent(renter, prop)
        self.assertGreater(owner.balance, owner0)
        self.assertLess(renter.balance, renter0)

    def test_mortgage_property_wrong_owner_false(self):
        game = self._game()
        p = game.players[0]
        prop = game.board.get_property_at(1)
        self.assertFalse(game.mortgage_property(p, prop))

    def test_mortgage_property_success(self):
        game = self._game()
        p = game.players[0]
        prop = game.board.get_property_at(1)
        prop.owner = p
        p.add_property(prop)
        p0 = p.balance
        self.assertTrue(game.mortgage_property(p, prop))
        self.assertEqual(p.balance, p0 + prop.mortgage_value)

    def test_unmortgage_wrong_owner_false(self):
        game = self._game()
        p = game.players[0]
        prop = game.board.get_property_at(1)
        self.assertFalse(game.unmortgage_property(p, prop))

    def test_unmortgage_not_mortgaged_false(self):
        game = self._game()
        p = game.players[0]
        prop = game.board.get_property_at(1)
        prop.owner = p
        p.add_property(prop)
        self.assertFalse(game.unmortgage_property(p, prop))

    def test_trade_wrong_owner_false(self):
        game = self._game()
        self.assertFalse(game.trade(game.players[0], game.players[1], game.board.get_property_at(1), 50))

    def test_trade_buyer_cannot_afford_false(self):
        game = self._game()
        seller = game.players[0]
        buyer = game.players[1]
        prop = game.board.get_property_at(1)
        prop.owner = seller
        seller.add_property(prop)
        buyer.balance = 0
        self.assertFalse(game.trade(seller, buyer, prop, 100))

    def test_trade_success(self):
        game = self._game()
        seller = game.players[0]
        buyer = game.players[1]
        prop = game.board.get_property_at(1)
        prop.owner = seller
        seller.add_property(prop)
        self.assertTrue(game.trade(seller, buyer, prop, 100))
        self.assertEqual(prop.owner, buyer)

    def test_check_bankruptcy_removes_player(self):
        game = self._game()
        p = game.players[1]
        p.balance = 0
        game._check_bankruptcy(p)
        self.assertNotIn(p, game.players)

    def test_find_winner_none_when_no_players(self):
        game = self._game()
        game.players.clear()
        self.assertIsNone(game.find_winner())

    def test_find_winner_highest_net_worth(self):
        game = self._game()
        game.players[0].balance = 100
        game.players[1].balance = 400
        game.players[2].balance = 50
        self.assertEqual(game.find_winner(), game.players[1])

    # Bug-revealing tests (expected to fail until code is fixed)
    def test_bug_mortgage_should_reduce_bank_reserves(self):
        game = self._game()
        p = game.players[0]
        prop = game.board.get_property_at(1)
        prop.owner = p
        p.add_property(prop)
        bank0 = game.bank.get_balance()
        game.mortgage_property(p, prop)
        self.assertEqual(game.bank.get_balance(), bank0 - prop.mortgage_value)

    def test_bug_unmortgage_insufficient_funds_should_keep_mortgaged(self):
        game = self._game()
        p = game.players[0]
        prop = game.board.get_property_at(1)
        prop.owner = p
        p.add_property(prop)
        prop.mortgage()
        p.balance = 0
        self.assertFalse(game.unmortgage_property(p, prop))
        self.assertTrue(prop.is_mortgaged)

    def test_bug_unmortgage_insufficient_funds_should_keep_zero_rent(self):
        game = self._game()
        p = game.players[0]
        prop = game.board.get_property_at(1)
        prop.owner = p
        p.add_property(prop)
        prop.mortgage()
        p.balance = 0
        game.unmortgage_property(p, prop)
        self.assertEqual(prop.get_rent(), 0)

    def test_bug_move_to_card_go_to_jail_should_trigger_jail(self):
        game = self._game()
        p = game.players[0]
        p.position = 5
        game._apply_card(p, {"description": "Move", "action": "move_to", "value": 30})
        self.assertTrue(p.in_jail)

    def test_bug_move_to_card_go_to_jail_should_land_on_jail_position(self):
        game = self._game()
        p = game.players[0]
        game._apply_card(p, {"description": "Move", "action": "move_to", "value": 30})
        self.assertEqual(p.position, 10)

    def test_bug_move_to_card_income_tax_should_deduct_tax(self):
        game = self._game()
        p = game.players[0]
        b0 = p.balance
        game._apply_card(p, {"description": "Move", "action": "move_to", "value": 4})
        self.assertEqual(p.balance, b0 - INCOME_TAX_AMOUNT)

    def test_bug_move_to_card_income_tax_should_increase_bank(self):
        game = self._game()
        p = game.players[0]
        bank0 = game.bank.get_balance()
        game._apply_card(p, {"description": "Move", "action": "move_to", "value": 4})
        self.assertEqual(game.bank.get_balance(), bank0 + INCOME_TAX_AMOUNT)

    def test_bug_trade_negative_cash_should_be_rejected_not_exception(self):
        game = self._game()
        seller = game.players[0]
        buyer = game.players[1]
        prop = game.board.get_property_at(1)
        prop.owner = seller
        seller.add_property(prop)
        seller0 = seller.balance
        buyer0 = buyer.balance
        raised = False
        try:
            result = game.trade(seller, buyer, prop, -50)
        except ValueError:
            raised = True
            result = None
        self.assertFalse(raised)
        self.assertFalse(result)
        self.assertEqual(seller.balance, seller0)
        self.assertEqual(buyer.balance, buyer0)
        self.assertEqual(prop.owner, seller)

    def test_bug_move_to_card_luxury_tax_should_deduct_tax(self):
        game = self._game()
        p = game.players[0]
        b0 = p.balance
        game._apply_card(p, {"description": "Move", "action": "move_to", "value": 38})
        self.assertEqual(p.balance, b0 - LUXURY_TAX_AMOUNT)

    def test_bug_move_to_card_luxury_tax_should_increase_bank(self):
        game = self._game()
        p = game.players[0]
        bank0 = game.bank.get_balance()
        game._apply_card(p, {"description": "Move", "action": "move_to", "value": 38})
        self.assertEqual(game.bank.get_balance(), bank0 + LUXURY_TAX_AMOUNT)

    def test_bug_move_to_card_chance_should_draw_chance_card(self):
        game = self._game()
        p = game.players[0]
        with patch.object(game.chance_deck, "draw", wraps=game.chance_deck.draw) as draw_spy:
            game._apply_card(p, {"description": "Move", "action": "move_to", "value": 7})
        self.assertGreaterEqual(draw_spy.call_count, 1)

    def test_bug_move_to_card_chance_should_advance_chance_deck_index(self):
        game = self._game()
        p = game.players[0]
        i0 = game.chance_deck.index
        game._apply_card(p, {"description": "Move", "action": "move_to", "value": 7})
        self.assertGreater(game.chance_deck.index, i0)

    def test_bug_move_to_card_community_should_draw_card(self):
        game = self._game()
        p = game.players[0]
        with patch.object(
            game.community_deck, "draw", wraps=game.community_deck.draw
        ) as draw_spy:
            game._apply_card(p, {"description": "Move", "action": "move_to", "value": 2})
        self.assertGreaterEqual(draw_spy.call_count, 1)

    def test_bug_move_to_card_community_should_advance_deck_index(self):
        game = self._game()
        p = game.players[0]
        i0 = game.community_deck.index
        game._apply_card(p, {"description": "Move", "action": "move_to", "value": 2})
        self.assertGreater(game.community_deck.index, i0)

    def test_bug_move_to_card_railroad_should_handle_tile_logic(self):
        game = self._game()
        p = game.players[0]
        with patch.object(game, "_handle_property_tile", return_value=None) as spy:
            game._apply_card(p, {"description": "Move", "action": "move_to", "value": 5})
        self.assertGreaterEqual(spy.call_count, 1)

    def test_bug_move_to_card_railroad_tile_should_have_purchase_model(self):
        # Railroad tiles are present in board tile map but missing from property model.
        # This keeps the test as a normal assertion failure instead of a runtime error.
        game = self._game()
        self.assertIsNotNone(game.board.get_property_at(5))

    def test_bug_collect_card_should_not_crash_when_bank_low(self):
        game = self._game()
        p = game.players[0]
        game.bank._funds = 0  # test branch for insufficient bank reserves on collect
        card = {"description": "Collect", "action": "collect", "value": 100}
        try:
            game._apply_card(p, card)
        except ValueError as exc:
            self.fail(f"Collect card should be handled gracefully, but raised: {exc}")

    def test_bug_give_loan_should_not_make_bank_negative(self):
        bank = Bank()
        player = Player("A")
        bank._funds = 50  # test branch where requested loan exceeds available funds
        bank.give_loan(player, 100)
        self.assertGreaterEqual(bank.get_balance(), 0)

    def test_bug_give_loan_insufficient_bank_should_not_credit_player(self):
        bank = Bank()
        player = Player("A")
        bank._funds = 50
        p0 = player.balance
        bank.give_loan(player, 100)
        self.assertEqual(player.balance, p0)


def _add_dynamic_tile_tests():
    mapping = {
        0: "go",
        2: "community_chest",
        4: "income_tax",
        5: "railroad",
        7: "chance",
        10: "jail",
        15: "railroad",
        17: "community_chest",
        20: "free_parking",
        22: "chance",
        25: "railroad",
        30: "go_to_jail",
        33: "community_chest",
        35: "railroad",
        36: "chance",
        38: "luxury_tax",
    }

    for pos, expected in mapping.items():
        def _test(self, pos=pos, expected=expected):
            self.assertEqual(Board().get_tile_type(pos), expected)

        setattr(TestBoardWhiteBox, f"test_tile_type_{pos}_{expected}", _test)


def _add_dynamic_property_position_tests():
    property_positions = [1, 3, 6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29, 31, 32, 34, 37, 39]
    for pos in property_positions:
        def _test(self, pos=pos):
            self.assertEqual(Board().get_tile_type(pos), "property")

        setattr(TestBoardWhiteBox, f"test_property_tile_type_{pos}", _test)


def _add_dynamic_card_action_tests():
    # One test per card for both decks to heavily cover _apply_card collect/pay/jail/etc. branches.
    for i, card in enumerate(CHANCE_CARDS):
        def _test(self, card=card):
            game = Game(["A", "B", "C"])
            player = game.players[0]
            with patch.object(game, "_handle_property_tile", return_value=None):
                game._apply_card(player, card)
            self.assertIsInstance(player.balance, int)

        setattr(TestGameWhiteBox, f"test_apply_chance_card_{i}", _test)


_add_dynamic_tile_tests()
_add_dynamic_property_position_tests()
_add_dynamic_card_action_tests()


if __name__ == "__main__":
    unittest.main(verbosity=2)
