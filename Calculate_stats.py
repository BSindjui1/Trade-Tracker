from Read_Trades import all_trades
from datetime import datetime

def parse_amount(text):
    if not text:
        return 0.0
    text = text.replace('$', "").replace(',', '')
    if text.startswith('(') and text.endswith(')'):
        text = "-" + text[1:-1]
    return float(text)

def parse_quantity(text):
    if not text:
        return 0
    text = text.replace("'", "")
    return float(text)

def calculate_realized_pnl(options_trades):
    total = 0.0

    for trade in options_trades:
        total += trade["amount"]

    return round(total, 2)


def parse_trades():
    trades = []
    options_trades = []
    open_positions = {}
    investments = []
    cash_activity = []


    for trade in all_trades:
        amount = parse_amount(trade['Amount'])
        quantity = parse_quantity(trade['Quantity'])

        if not trade['Description']:
            continue

        desc_parts = trade['Description'].split()
        if len(desc_parts) < 4:
            continue

        instrument = desc_parts[0]
        Expiration_date = desc_parts[1]
        side = desc_parts[2]
        strike_price = desc_parts[3]

        trades.append({
            'Expiration Date': Expiration_date,
            'instrument': instrument,
            'Strike Price': strike_price,
            'Type': side,
            'quantity': quantity,
            'amount': amount,
            'Date Bought': trade['Activity Date']
        })

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

        if trade['Trans Code'] in ('INT', 'Buy', 'CDIV', 'SLIP'):
            investments.append({
                'Date Bought': trade['Activity Date'],
                'instrument': trade['Instrument'],
                'quantity': quantity,
                'Share Price': trade['Price'],
                'Amount Bought': amount
            })

        if trade['Trans Code'] in ('DCF', 'Gold', 'GMPC'):
            cash_activity.append({
                'Transaction date': trade['Activity Date'],
                'Description': trade['Description'],
                'Amount': amount
            })

    # Build open positions
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
    

    return trades, options_trades, open_positions, investments, cash_activity
    
