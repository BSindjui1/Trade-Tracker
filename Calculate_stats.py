from Read_Trades import all_trades
from datetime import datetime

# ---------- Helper Functions ----------


def parse_amount(text):
    # This handles amounts with quotations and parentheses and returns a float
    if not text:
        return 0.0
    text = text.replace('$', "").replace(',', '')
    if text.startswith('(') and text.endswith(')'):
        text = "-" + text[1:-1]
    return float(text)

def parse_quantity(text):
    # This handles quantities with quotations and returns a float
    if not text:
        return 0
    text = text.replace("'", "")
    return float(text)

def calculate_realized_pnl(options_trades):
    # Calculate realized P&L from options trades

    total = 0.0

    for trade in options_trades:
        total += trade["amount"]

    return round(total, 2)


def parse_trades():
    # Parse all trades and categorizes them into different lists
    trades = []
    options_trades = []
    open_positions = {}
    investments = []
    cash_activity = []

    # Iterate through all trades
    for trade in all_trades:
        # Uses the Parse amount and quantity to convert strings to numbers
        amount = parse_amount(trade['Amount'])
        quantity = parse_quantity(trade['Quantity'])

        # Skip trades with empty descriptions
        if not trade['Description']:
            continue
        # Parse the description to extract relevant details
        desc_parts = trade['Description'].split()
        if len(desc_parts) < 4:
            continue
            #splits the description into parts
        instrument = desc_parts[0]
        Expiration_date = desc_parts[1]
        side = desc_parts[2]
        strike_price = desc_parts[3]
        # This builds the trades list
        trades.append({
            'Expiration Date': Expiration_date,
            'instrument': instrument,
            'Strike Price': strike_price,
            'Type': side,
            'quantity': quantity,
            'amount': amount,
            'Date Bought': trade['Activity Date']
        })


        # This builds the options trades list by using to check transaction codes
        if trade['Trans Code'] in ('BTO', 'STC'):
            options_trades.append({
                'instrument': instrument,
                'expiration': Expiration_date,
                'strike': strike_price,
                'side': side,
                'quantity': int(quantity),
                'amount': amount,
                'date': trade['Activity Date'],
                'option_type': 'Call' if side == 'Call' else 'Put',
                'trans_code': trade['Trans Code']
            })
        # Build investments list
        if trade['Trans Code'] in ('INT', 'Buy', 'CDIV', 'SLIP'):
            investments.append({
                'Date Bought': trade['Activity Date'],
                'instrument': trade['Instrument'],
                'quantity': quantity,
                'Share Price': trade['Price'],
                'Amount Bought': amount
            })
        # Build cash activity list
        if trade['Trans Code'] in ('DCF', 'Gold', 'GMPC'):
            cash_activity.append({
                'Transaction date': trade['Activity Date'],
                'Description': trade['Description'],
                'Amount': amount
            })

    # Checks for open positions in options trades
    for trade in options_trades:
        key = (trade['instrument'], trade['expiration'], trade['strike'], trade['option_type'])
        if trade['trans_code'] == 'BTO':
            open_positions.setdefault(key, 0)
            open_positions[key] += trade['quantity']
        elif trade['trans_code'] == 'STC':
            open_positions.setdefault(key, 0)
            open_positions[key] -= trade['quantity']

    # Remove closed positions
    open_positions = {k: v for k, v in open_positions.items() if v != 0}

    # Return all parsed data
    return trades, options_trades, open_positions, investments, cash_activity
    
