import pandas as pd
from Calculate_stats import parse_trades


def export_options_trades(options_trades, filename="options_trades.xlsx"):
    rows = []

    for trade in options_trades:
        rows.append({
            "Date": trade.get("date"),
            "Symbol": trade.get("instrument"),
            "Type": trade.get("option_type"),
            "Strike": trade.get("strike"),
            "Expiration": trade.get("expiration"),
            "Quantity": trade.get("quantity"),
            "Amount": trade.get("amount")
        })

    # Always create file
    if not rows:
        print("No options trades found. Creating empty Excel file.")
        df = pd.DataFrame(columns=[
            "Date", "Symbol", "Type", "Strike", "Expiration", "Quantity", "Amount"
        ])
    else:
        df = pd.DataFrame(rows)
        print(f"Exported {len(rows)} option trades.")

    df.to_excel(filename, index=False)
    print(f"File saved as '{filename}'")

    return filename


if __name__ == "__main__":
    # pull data the same way your main app does
    trades, options_trades, open_positions, investments, cash_activity = parse_trades()

    export_options_trades(options_trades)
