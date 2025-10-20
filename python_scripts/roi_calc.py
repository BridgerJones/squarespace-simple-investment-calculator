def generate_pmt_schedule(principal, annual_interest_rate, periods, periods_per_year=12):
    schedule = []

    # Calculate periodic interest rate
    r = annual_interest_rate / periods_per_year
    # Calculate the fixed payment using the amortization formula
    pmt = (principal * r) / (1 - (1 + r) ** -periods)

    remaining_balance = principal

    for period in range(1, periods + 1):
        interest_payment = remaining_balance * r
        principal_payment = pmt - interest_payment
        remaining_balance -= principal_payment
        # To handle floating point rounding error, set remaining balance to 0 if close
        if remaining_balance < 1e-8:
            remaining_balance = 0

        schedule.append({
            'Period': period,
            'Payment': round(pmt, 2),
            'Principal': round(principal_payment, 2),
            'Interest': round(interest_payment, 2),
            'Remaining Balance': round(remaining_balance, 2)
        })
    return schedule

if __name__ == '__main__':
    s = generate_pmt_schedule(30000, 0.12, 60)

    for schedule in s:
        print(schedule)