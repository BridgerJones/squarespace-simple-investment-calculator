# Project Generated with ChatGPT 4.1-mini

# squarespace-simple-investment-calculator
A web calculator that computes fixed monthly payments on an initial investment (min $30,000) at a 12% annual return over 5 years. It breaks down payments into principal returned and profit earned, shows yearly summaries, and visualizes results with a chart. Calculates months until next investment.

# Investment Earnings Calculator

This is a simple interactive investment calculator implemented in HTML and JavaScript.  
It allows an investor to input an initial investment amount (minimum $30,000) and calculates the monthly payments received over 5 years based on a fixed 12% annual return rate.

## Features

- Calculates the fixed monthly payment based on the investment amount and return rate.
- Breaks down monthly payments into:
  - **Principal Returned**: The portion of the payment representing the payback of the initial investment.
  - **Profit Earned**: The earnings/profit portion of the payment.
- Displays a detailed year-by-year breakdown over 5 years:
  - Principal returned each year
  - Profit earned each year
  - Total earnings each year
- Summarizes total principal returned, profit earned, and total earnings over 5 years.
- Estimates the number of months until the investor can roll their earnings into a new investment opportunity based on a $30,000 minimum threshold.
- Visualizes the yearly breakdown with a responsive bar chart using [Chart.js](https://www.chartjs.org/).

## How It Works

The calculator uses the standard amortization formula (similar to Excel's `PMT` function) to determine the fixed monthly payment over 60 months (5 years) at a 12% fixed annual return rate.

Each monthly payment consists of a profit portion (computed on the remaining principal) and a returned principal portion. The monthly payment is constant over the investment term.

## Usage

1. Open the `index.html` file (or embed the code in your website).
2. Enter your initial investment amount (must be at least $30,000).
3. Click "Calculate" to see:
   - Your fixed monthly payment.
   - Year 1 and 5-year earnings breakdown.
   - A chart visualizing your principal returned and profit earned per year.
   - The month when you can roll the earnings into a new investment.

## Tech Stack

- HTML & CSS (for layout and styling)
- JavaScript (calculations and interactivity)
- [Chart.js](https://cdn.jsdelivr.net/npm/chart.js) for rendering charts

## Customization

- The annual return rate is fixed at 12%, but you can easily modify it in the script if required.
- The investment period is fixed at 5 years (60 months).
- The minimum investment amount is set to $30,000, changeable in the form validation.

## License

MIT License

---

*Feel free to clone, customize, or improve this calculator to suit your own investment analysis needs!*
