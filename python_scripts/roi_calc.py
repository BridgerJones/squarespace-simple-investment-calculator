import csv

def calculate_monthly_payment(principal, annual_rate, total_months):
    """Calculate the borrower’s monthly payment."""
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0:
        return principal / total_months
    pmt = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -total_months)
    return pmt

def generate_schedule(principal, annual_rate, total_months):
    """Generate amortization schedule with additional fields for cash flow, YTD earnings, total return."""
    schedule = []
    remaining_principal = principal
    monthly_rate = annual_rate / 100 / 12
    monthly_payment = calculate_monthly_payment(principal, annual_rate, total_months)
    cumulative_cash_flow = 0  # Total received till date

    for month in range(1, total_months + 1):
        interest_payment = remaining_principal * monthly_rate
        principal_payment = monthly_payment - interest_payment
        remaining_principal -= principal_payment
        cumulative_cash_flow += monthly_payment
        total_return = cumulative_cash_flow  # sum of all payments received

        schedule.append({
            "Month": month,
            "Cash Flow": round(monthly_payment, 2),
            "Interest": round(interest_payment, 2),
            "Principal": round(principal_payment, 2),
            "Remaining Principal": round(remaining_principal, 2),
            "YTD Earnings": round(cumulative_cash_flow, 2),
            "Total Return": round(total_return, 2)
        })

    return schedule

# User input with default filenames
principal_amount = float(input("Enter the amount you lent (initial investment): "))
annual_interest_rate = float(input("Enter the annual interest rate (%): "))
total_months = int(input("Enter the loan term in months: "))
main_csv_filename = input("Enter main CSV filename (default: schedule.csv): ").strip()
return_csv_filename = input("Enter return tracking CSV filename (default: return_tracking.csv): ").strip()

if not main_csv_filename:
    main_csv_filename = "schedule.csv"
if not return_csv_filename:
    return_csv_filename = "return_tracking.csv"

# Generate schedule
schedule = generate_schedule(principal_amount, annual_interest_rate, total_months)

# Write the detailed schedule
with open(main_csv_filename, 'w', newline='') as csvfile:
    fieldnames = ["Month", "Cash Flow", "Interest", "Principal", "Remaining Principal", "YTD Earnings", "Total Return"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in schedule:
        writer.writerow(row)

# Write the return tracking (monthly cash flow + YTD)
with open(return_csv_filename, 'w', newline='') as retfile:
    ret_writer = csv.writer(retfile)
    ret_writer.writerow(["Month", "Cash Flow", "YTD Earnings", "Total Return"])
    for row in schedule:
        ret_writer.writerow([
            row["Month"],
            row["Cash Flow"],
            row["YTD Earnings"],
            row["Total Return"]
        ])

print(f"Schedule saved to {main_csv_filename}")
print(f"Return tracking saved to {return_csv_filename}")