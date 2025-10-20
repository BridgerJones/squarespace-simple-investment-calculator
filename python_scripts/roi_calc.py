class LoanPortfolio:
    def __init__(self, principal, annual_interest_rate, term_years=5, periods_per_year=12):
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.term_years = term_years
        self.periods_per_year = periods_per_year
        self.term_periods = term_years * periods_per_year
        
        self.r = annual_interest_rate / periods_per_year
        if self.r == 0:
            self.fixed_pmt = principal / self.term_periods
        else:
            self.fixed_pmt = (principal * self.r) / (1 - (1 + self.r) ** -self.term_periods)
        
        self.active_loans = [{'start_period': 1, 'remaining_balance': principal}]
        self.total_loans_issued = 1
        
        self.cash_balance = 0.0
        self.current_period = 0

    def step(self):
        self.current_period += 1
        
        period_payment_total = 0
        period_interest_total = 0
        period_principal_total = 0
        
        loans_to_remove = []
        for loan in self.active_loans:
            loan_age = self.current_period - loan['start_period'] + 1
            if loan_age <= 0 or loan['remaining_balance'] <= 0:
                continue
            
            interest = loan['remaining_balance'] * self.r
            principal_payment = self.fixed_pmt - interest
            
            if principal_payment > loan['remaining_balance']:
                principal_payment = loan['remaining_balance']
                payment = principal_payment + interest
            else:
                payment = self.fixed_pmt
            
            loan['remaining_balance'] -= principal_payment
            
            period_payment_total += payment
            period_interest_total += interest
            period_principal_total += principal_payment
            
            if loan['remaining_balance'] <= 1e-8:
                loans_to_remove.append(loan)
        
        for loan in loans_to_remove:
            self.active_loans.remove(loan)
        
        # Add payment to cash
        self.cash_balance += period_payment_total
        
        # Issue new loans as cash allows
        while self.cash_balance >= self.principal:
            self.active_loans.append({'start_period': self.current_period, 'remaining_balance': self.principal})
            self.cash_balance -= self.principal
            self.total_loans_issued += 1
        
        return {
            'Period': self.current_period,
            'Total Payment Received': round(period_payment_total, 2),
            'Interest Collected': round(period_interest_total, 2),
            'Principal Repaid': round(period_principal_total, 2),
            'Active Loans': len(self.active_loans),
            'Cash Available for Loans': round(self.cash_balance, 2),
            'Total Loans Issued': self.total_loans_issued
        }
    
    def run_full_investment(self, total_periods):
        """
        Simulate the investment for the given number of periods and return total earned.
        """
        total_earned = 0.0
        for _ in range(total_periods):
            info = self.step()
            total_earned += info['Total Payment Received']
        return total_earned


def main():
    principal = float(input("Enter initial loan principal amount: "))
    annual_rate = 0.12  # fixed 12%
    term_years = 5
    periods_per_year = 12
    term_periods = term_years * periods_per_year
    
    portfolio = LoanPortfolio(principal, annual_rate, term_years, periods_per_year)
    
    # Simulate for 3 full loan terms (15 years)
    total_periods_to_simulate = term_periods * 3
    total_earned = portfolio.run_full_investment(total_periods_to_simulate)
    
    print(f"\nTotal amount earned (all payments received) over {total_periods_to_simulate} periods: ${total_earned:,.2f}")

if __name__ == '__main__':
    main()