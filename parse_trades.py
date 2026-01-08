import unittest
from Calculate_stats import parse_trades

class TestParseTrades(unittest.TestCase):
    def setUp(self):
      (  # This runs before every test
        self.trades, 
        self.options_trades, 
        self.open_positions, 
        self.investments, 
        self.cash_activity
      ) = parse_trades()


    def test_trades_not_empty(self):
        #makes sure trades list is not empty
        self.assertGreater(len(self.trades),0,"Trades Should not be empty")

    def test_options_trades_structure(self):
        #Make sure each option trade has required keys
        required_keys = {'instrument','expiration','strike', 'side', 'quantity', 'amount', 'date', 'option_type', 'trans_code'}
        for trade in self.options_trades:
            self.assertTrue(required_keys.issubset(trade.keys()), f"Missing keys in options trade: {trade}")

    def test_open_positions_values(self):
        #Test that there are open positions checks Quantity> 0
        for key,qty in self.open_positions.items():
            self.assertGreaterEqual(qty, 0, f"Quantity should >=0 for {key}")
    
    def test_investments_strucutre(self):
        #make sure each investment has required keys
        required_keys = {'Date Bought', 'instrument', 'quantity', 'Share Price', 'Amount Bought'}
        for inv in self.investments:
            self.assertTrue(required_keys.issubset(inv.keys()), f"Missing keys in investment: {inv}")

    def test_cash_activity_structure(self):
        # Make sure each cash transaction has required keys
        required_keys = {'Transaction date', 'Description', 'Amount'}
        for cash in self.cash_activity:
            self.assertTrue(required_keys.issubset(cash.keys()), f"Missing keys in cash activity: {cash}")


if __name__ == "__main__":
    unittest.main()                    