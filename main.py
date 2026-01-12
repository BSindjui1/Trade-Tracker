from Calculate_stats import parse_trades,calculate_realized_pnl
from update_sheets import export_options_trades


# ---------- Shared helpers ----------
# Helper function to pause execution until user presses Enter
def pause():
    input("\nPress Enter to continue...")

# ---------- Display headers ----------
def print_option_header(include_amount=False):
    header = (
        f"|{'Symbol':<6}"

        f"|{'Type':<6}"
        f"|{'Strike':<8}"
        f"|{'Expiration':<12}"
    )
    # Add Amount column if specified
    if include_amount:
        header += f"|{'Amount':<10}"
    header += f"|{'Qty':>4}|"

    print(header)
    print("-" * len(header))


# ---------- Display functions ----------


def show_summary(trades, options_trades, open_positions, investments, cash_activity):
    print(f"\nOptions trades: {len(options_trades)}")
    print(f"Investments: {len(investments)}")
    print(f"Cash transactions: {len(cash_activity)}")
    print(f"Open positions: {len(open_positions)}")
    pause()


def show_options_trades(options_trades):
    if not options_trades:
        print("No options trades")
        pause()
        return

    show_options_menu(options_trades)


def show_investments(investments):
    if not investments:
        print("No investments")
        pause()
        return

    for inv in investments:
        #checks for quantity to display appropriate text
        qty_display = (
            "Cash Dividend"
            if inv["quantity"] == 0
            else f"{inv['quantity']} shares"
        )
# checks for share price to display appropriate text
        shr_display = (
            "N/A"
            if inv["quantity"] == 0
            else f"{inv['Share Price']}"
        )

        print(
            f"{inv['Date Bought']} | "
            f"{inv['instrument']} | "
            f"{qty_display} | "
            f"{shr_display} | "
            f"{inv['Amount Bought']}"
        )
    pause()


def show_cash_activity(cash_activity):
    if not cash_activity:
        print("No cash activity")
        pause()
        return

    for cash in cash_activity:
        print(
            f"{cash['Transaction date']} | "
            f"{cash['Description']} | "
            f"{cash['Amount']}"
        )
    pause()


def show_open_positions(open_positions):
    if not open_positions:
        print("No open positions")
        pause()
        return

    print_option_header()

    for (symbol, exp, strike, opt_type), qty in open_positions.items():
        print(
            f"|{symbol:<6}"
            f"|{opt_type:<6}"
            f"|{strike:<8}"
            f"|{exp:<12}"
            f"|{qty:>4}|"
        )
    pause()

def show_realized_pnl(options_trades):
    pnl = calculate_realized_pnl(options_trades)
    print(f"\nTotal Realized Options P&L: ${pnl}")
    pause()

# ---------- Options sub-menu ----------

def show_options_menu(options_trades):
    while True:
        print("\nOptions Trades")
        print("1. Calls")
        print("2. Puts")
        print("3. All contracts")
        print("4. Filter By Ticker")
        print("5. Back to Main Menu")

        try:
            choice = int(input("Enter your choice (1-5): "))
            if choice not in range(1, 6):
                print("Please enter a number between 1 and 5.")
                continue
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if choice == 5:
            return
    # Filter options trades based on user choice
        if choice == 1:
            filtered = [t for t in options_trades if t["option_type"].lower() == "call"]
        elif choice == 2:
            filtered = [t for t in options_trades if t["option_type"].lower() == "put"]
        elif choice == 3:
            filtered = options_trades
        elif choice == 4:
            ticker = input("Enter ticker symbol: ").strip().upper()
            filtered = [t for t in options_trades if t["instrument"].upper() == ticker]

        if not filtered:
            print("No matching contracts.")
            pause()
            continue

        


        print_option_header(include_amount=True)

        for trade in filtered:
            print(
                f"|{trade['instrument']:<6}"
                f"|{trade['option_type']:<6}"
                f"|{trade['strike']:<8}"
                f"|{trade['expiration']:<12}"
                f"|{trade['amount']:<10}"
                f"|{trade['quantity']:>4}|"
            )

        pause()


# ---------- Main menu ----------

def main():
    trades, options_trades, open_positions, investments, cash_activity = parse_trades()
# Define actions for main menu choices
    actions = {
        1: lambda: show_options_trades(options_trades),
        2: lambda: show_investments(investments),
        3: lambda: show_cash_activity(cash_activity),
        4: lambda: show_open_positions(open_positions),
        5: lambda: show_summary(trades, options_trades, open_positions, investments, cash_activity),
        6: lambda: show_realized_pnl(options_trades),
        7: lambda: export_open_positions(open_positions)
    }


    while True:
        print("\nMain Menu")
        print("1. Show Options Trades")
        print("2. Show Investments")
        print("3. Show Cash Activity")
        print("4. Show Open Positions")
        print("5. Show Summary")
        print("6. show Realized P&L")
        print("7. Export Open Positions to Excel")
        print("8. Exit")
# Get user choice and filters actions
        try:
            choice = int(input("Enter your choice (1-8): "))
            if choice not in range(1, 9):
                print("Please enter a number between 1 and 8.")
                continue
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if choice == 8:
            print("Goodbye!")
            break

        actions[choice]()

        


if __name__ == "__main__":
    main()
