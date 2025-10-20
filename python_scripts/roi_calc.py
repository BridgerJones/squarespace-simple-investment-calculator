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
    Generates the lender's income schedule for the loan with rolling YTD (Year-To-Date) interest and payments.

    Args:
        principal (float): Initial loan amount.
        annual_interest_rate (float): Annual interest rate as a decimal (e.g., 0.12 for 12%).
        periods (int): Total number of payment periods.
        periods_per_year (int): Number of payment periods in a year (default 12 for monthly).

    Returns:
        List[Dict]: List where each dict contains:
                    'Period', 'Payment Received', 'Interest Income', 'Principal Repaid', 'Remaining Principal',
                    'YTD Interest Income', 'YTD Payment Received'.
    """
    borrower_schedule = generate_pmt_schedule(principal, annual_interest_rate, periods, periods_per_year)

    lender_schedule = []
    cumulative_interest = 0
    cumulative_payment = 0

    for entry in borrower_schedule:
        period = entry['Period']
        payment = entry['Payment']
        interest_income = entry['Interest']
        principal_repaid = entry['Principal']
        remaining_principal = entry['Remaining Balance']

        cumulative_interest += interest_income
        cumulative_payment += payment

        lender_schedule.append({
            'Period': period,
            'Payment Received': round(payment, 2),
            'Interest Income': round(interest_income, 2),
            'Principal Repaid': round(principal_repaid, 2),
            'Remaining Principal': round(remaining_principal, 2),
            'YTD Interest Income': round(cumulative_interest, 2),
            'YTD Payment Received': round(cumulative_payment, 2)
        })

    return lender_schedule


def generate_rolling_loans_schedule(principal: float, annual_interest_rate: float, total_periods: int, periods_per_year: int = 12):
    """
    Generate lender income schedule when re-investing principal immediately upon repayment within the year.

    Args:
        principal (float): Principal for each loan.
        annual_interest_rate (float): Annual interest rate as decimal.
        total_periods (int): Total periods to simulate.
        periods_per_year (int): Number of payment periods per year.

    Returns:
        List[Dict]: Aggregate payment info for each period including rolling YTD payment and interest.
    """
    r = annual_interest_rate / periods_per_year

    # Fixed payment per loan over full term
    if r == 0:
        pmt_single = principal / total_periods
    else:
        pmt_single = (principal * r) / (1 - (1 + r) ** -total_periods)

    # Active loans represented as dicts with 'start_period' and 'remaining_balance'
    active_loans = [{'start_period': 1, 'remaining_balance': principal}]

    schedule = []
    cumulative_payment_received = 0.0
    cumulative_interest_earned = 0.0

    # For tracking payments within the year for adding new loans
    ytd_payment_received = 0.0
    periods_in_year = periods_per_year

    for period in range(1, total_periods + 1):
        period_payment = 0.0
        period_interest = 0.0
        period_principal = 0.0

        loans_fully_paid = []

        for loan in active_loans:
            loan_age = period - loan['start_period'] + 1

            if loan['remaining_balance'] > 0 and loan_age > 0:
                interest = loan['remaining_balance'] * r
                principal_payment = pmt_single - interest

                # Correct last payment if principal_payment > remaining balance
                if principal_payment > loan['remaining_balance']:
                    principal_payment = loan['remaining_balance']
                    # Adjust payment accordingly
                    pmt = principal_payment + interest
                else:
                    pmt = pmt_single

                loan['remaining_balance'] -= principal_payment

                period_payment += pmt
                period_interest += interest
                period_principal += principal_payment

                if loan['remaining_balance'] <= 1e-8:
                    loans_fully_paid.append(loan)

        # Remove fully paid loans
        for loan in loans_fully_paid:
            active_loans.remove(loan)

        cumulative_payment_received += period_payment
        cumulative_interest_earned += period_interest

        ytd_payment_received += period_payment

        # Check if YTD payments exceed principal; add new loans as needed
        while ytd_payment_received >= principal:
            active_loans.append({'start_period': period, 'remaining_balance': principal})
            ytd_payment_received -= principal

        schedule.append({
            'Period': period,
            'Payment Received': round(period_payment, 2),
            'Interest Income': round(period_interest, 2),
            'Principal Repaid': round(period_principal, 2),
            'Remaining Principal (All Loans)': round(sum(loan['remaining_balance'] for loan in active_loans), 2),
            'YTD Interest Income': round(cumulative_interest_earned, 2),
            'YTD Payment Received': round(cumulative_payment_received, 2),
            'Active Loans Count': len(active_loans)
        })

    return schedule


if __name__ == '__main__':
    principal = 30000
    annual_interest_rate = 0.12
    periods = 60
    periods_per_year = 12

    print("=== Borrower's Payment Schedule ===")
    borrower_sched = generate_pmt_schedule(principal, annual_interest_rate, periods)
    for row in borrower_sched:
        print(row)

    print("\n=== Lender's Income Schedule ===")
    lender_sched = generate_lender_schedule(principal, annual_interest_rate, periods)
    for row in lender_sched:
        print(row)

    print("\n=== Rolling Loans Income Schedule ===")
    rolling_sched = generate_rolling_loans_schedule(principal, annual_interest_rate, periods, periods_per_year)
    for row in rolling_sched:
        print(row)