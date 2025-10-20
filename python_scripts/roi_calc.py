def generate_pmt_schedule(principal: float, annual_interest_rate: float, periods: int, periods_per_year: int = 12):
    schedule = []
    r = annual_interest_rate / periods_per_year

    if r == 0:
        pmt = principal / periods
    else:
        pmt = (principal * r) / (1 - (1 + r) ** -periods)

    remaining_balance = principal

    for period in range(1, periods + 1):
        interest_payment = remaining_balance * r
        principal_payment = pmt - interest_payment
        remaining_balance -= principal_payment
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


from typing import Callable, Optional, List, Dict

def generate_rolling_loans_schedule(
    principal: float,
    annual_interest_rate: float,
    total_periods: int,
    periods_per_year: int = 12,
    max_loans: Optional[int] = None,
    should_issue_loan: Optional[Callable[[int, int, int], bool]] = None
) -> List[Dict]:
    r = annual_interest_rate / periods_per_year

    if r == 0:
        pmt_single = principal / total_periods
    else:
        pmt_single = (principal * r) / (1 - (1 + r) ** -total_periods)

    active_loans = [{'start_period': 1, 'remaining_balance': principal}]
    total_loans_issued = 1

    schedule = []
    cumulative_payment_received = 0.0
    cumulative_interest_earned = 0.0
    ytd_payment_received = 0.0

    if should_issue_loan is None:
        def should_issue_loan(period, total_issued, active_count):
            if max_loans is None:
                return True
            else:
                return total_issued < max_loans

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

                if principal_payment > loan['remaining_balance']:
                    principal_payment = loan['remaining_balance']
                    pmt = principal_payment + interest
                else:
                    pmt = pmt_single

                loan['remaining_balance'] -= principal_payment

                period_payment += pmt
                period_interest += interest
                period_principal += principal_payment

                if loan['remaining_balance'] <= 1e-8:
                    loans_fully_paid.append(loan)

        for loan in loans_fully_paid:
            active_loans.remove(loan)

        cumulative_payment_received += period_payment
        cumulative_interest_earned += period_interest
        ytd_payment_received += period_payment

        while ytd_payment_received >= principal:
            if should_issue_loan(period, total_loans_issued, len(active_loans)):
                active_loans.append({'start_period': period, 'remaining_balance': principal})
                total_loans_issued += 1
                ytd_payment_received -= principal
            else:
                break

        schedule.append({
            'Period': period,
            'Payment Received': round(period_payment, 2),
            'Interest Income': round(period_interest, 2),
            'Principal Repaid': round(period_principal, 2),
            'Remaining Principal (All Loans)': round(sum(loan['remaining_balance'] for loan in active_loans), 2),
            'YTD Interest Income': round(cumulative_interest_earned, 2),
            'YTD Payment Received': round(cumulative_payment_received, 2),
            'Active Loans Count': len(active_loans),
            'Total Loans Issued': total_loans_issued
        })

    return schedule


def ask_float(prompt: str, default: Optional[float] = None) -> float:
    while True:
        inp = input(prompt + (f" [{default}]" if default is not None else "") + ": ")
        if not inp.strip() and default is not None:
            return default
        try:
            val = float(inp)
            if val < 0:
                print("Please enter a non-negative number.")
                continue
            return val
        except Exception:
            print("Invalid number. Please try again.")


def ask_int(prompt: str, default: Optional[int] = None) -> int:
    while True:
        inp = input(prompt + (f" [{default}]" if default is not None else "") + ": ")
        if not inp.strip() and default is not None:
            return default
        try:
            val = int(inp)
            if val < 1:
                print("Please enter an integer >= 1.")
                continue
            return val
        except Exception:
            print("Invalid integer. Please try again.")


def ask_yes_no(prompt: str, default: Optional[bool] = None) -> bool:
    yes = {'yes', 'y'}
    no = {'no', 'n'}
    default_str = {True: 'Y/n', False: 'y/N'}.get(default, 'y/n')
    while True:
        inp = input(f"{prompt} [{default_str}]: ").strip().lower()
        if not inp and default is not None:
            return default
        if inp in yes:
            return True
        elif inp in no:
            return False
        else:
            print("Please respond with yes or no (y/n).")

            
def main():
    print("Welcome to the loan schedule generator!")
    principal = ask_float("Enter loan principal amount", 30000)
    annual_rate = ask_float("Enter annual interest rate (e.g. 0.12 for 12%)", 0.12)
    periods = ask_int("Enter loan term (total number of periods)", 60)
    periods_per_year = ask_int("Enter number of periods per year (e.g. 12 for monthly)", 12)

    print("\nBorrower's Payment Schedule:")
    borrower_sched = generate_pmt_schedule(principal, annual_rate, periods, periods_per_year)
    for row in borrower_sched:
        print(row)

    print("\nLender's Income Schedule:")
    lender_sched = generate_lender_schedule(principal, annual_rate, periods, periods_per_year)
    for row in lender_sched:
        print(row)

    enable_rolling = ask_yes_no("\nEnable rolling loans (automatic issuance of new loans)?", False)

    if enable_rolling:
        max_loans = None
        use_max = ask_yes_no("Limit maximum number of loans?", False)
        if use_max:
            max_loans = ask_int("Enter maximum number of loans")

        max_active_loans = None
        use_limit_active = ask_yes_no("Limit max active loans for issuing new loans?", False)
        if use_limit_active:
            max_active_loans = ask_int("Enter max active loans")

        def issue_condition(period, total_issued, active_count):
            if max_loans is not None and total_issued >= max_loans:
                return False
            if max_active_loans is not None and active_count >= max_active_loans:
                return False
            return True

        rolling_sched = generate_rolling_loans_schedule(
            principal, annual_rate, periods, periods_per_year,
            max_loans=max_loans,
            should_issue_loan=issue_condition
        )

        print("\nRolling Loans Income Schedule:")
        for row in rolling_sched:
            print(row)

    else:
        print("\nRolling loans feature was not enabled.")


if __name__ == '__main__':
    main()