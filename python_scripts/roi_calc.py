def generate_pmt_schedule(principal: float, annual_interest_rate: float, periods: int, periods_per_year: int = 12):
    """
    Generates a loan payment schedule (amortization table).

    Args:
        principal (float): The initial loan amount.
        annual_interest_rate (float): The annual interest rate as a decimal (e.g., 0.12 for 12%).
        periods (int): Total number of payment periods.
        periods_per_year (int): Number of payment periods per year (default is 12 for monthly).

    Returns:
        List[Dict]: A list of dictionaries, each representing a payment period with keys:
                    'Period', 'Payment', 'Principal', 'Interest', 'Remaining Balance'.
    """
    schedule = []

    # Calculate periodic interest rate
    r = annual_interest_rate / periods_per_year

    # Handle zero interest rate case
    if r == 0:
        pmt = principal / periods
    else:
        # Calculate the fixed payment using the amortization formula
        pmt = (principal * r) / (1 - (1 + r) ** -periods)

    remaining_balance = principal

    for period in range(1, periods + 1):
        interest_payment = remaining_balance * r
        principal_payment = pmt - interest_payment
        remaining_balance -= principal_payment
        # To handle floating point rounding error, set remaining balance to 0 if close
        if abs(remaining_balance) < 1e-8:
            remaining_balance = 0

        schedule.append({
            'Period': period,
            'Payment': round(pmt, 2),
            'Principal': round(principal_payment, 2),
            'Interest': round(interest_payment, 2),
            'Remaining Balance': round(remaining_balance, 2)
        })

    return schedule


def generate_lender_schedule(principal: float, annual_interest_rate: float, periods: int, periods_per_year: int = 12):
    """
    Generates the lender's income schedule for the loan with rolling YTD (Year-To-Date) interest.

    Args:
        principal (float): Initial loan amount.
        annual_interest_rate (float): Annual interest rate as a decimal (e.g., 0.12 for 12%).
        periods (int): Total number of payment periods.
        periods_per_year (int): Number of payment periods in a year (default 12 for monthly).

    Returns:
        List[Dict]: List where each dict contains:
                    'Period', 'Payment Received', 'Interest Income', 'Principal Repaid', 'Remaining Principal', 'YTD Interest Income'.
    """
    # Reuse the borrower schedule generator to get principal and interest per period
    borrower_schedule = generate_pmt_schedule(principal, annual_interest_rate, periods, periods_per_year)

    lender_schedule = []
    cumulative_interest = 0

    for entry in borrower_schedule:
        period = entry['Period']
        payment = entry['Payment']
        interest_income = entry['Interest']
        principal_repaid = entry['Principal']
        remaining_principal = entry['Remaining Balance']

        cumulative_interest += interest_income

        lender_schedule.append({
            'Period': period,
            'Payment Received': payment,
            'Interest Income': round(interest_income, 2),
            'Principal Repaid': round(principal_repaid, 2),
            'Remaining Principal': round(remaining_principal, 2),
            'YTD Interest Income': round(cumulative_interest, 2)
        })

    return lender_schedule


if __name__ == '__main__':
    # Borrower's payment schedule example
    print("Borrower's Payment Schedule:")
    borrower_sched = generate_pmt_schedule(30000, 0.12, 60)
    for row in borrower_sched:
        print(row)

    print("\nLender's Income Schedule:")
    # Lender's income schedule example
    lender_sched = generate_lender_schedule(30000, 0.12, 60)
    for row in lender_sched:
        print(row)