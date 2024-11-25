import QuantLib as ql
import datetime
import pandas as pd

# Load data from CSV
csv_data = pd.read_csv('bond_data.csv')


def process_bond_data(row):
    # Assign inputs from CSV
    cusip = row['cusip']
    issue_date = ql.DateParser.parseFormatted(row['issue_date'], '%m/%d/%Y') if pd.notna(row['issue_date']) else None
    end_date = ql.DateParser.parseFormatted(row['end_date'], '%m/%d/%Y') if pd.notna(row['end_date']) else None
    coupon_rate = row['coupon_rate'] / 100 if pd.notna(row['coupon_rate']) else None
    price_mid = row['price_mid'] if pd.notna(row['price_mid']) else None
    price_high = row['price_high'] if pd.notna(row['price_high']) else None
    price_low = row['price_low'] if pd.notna(row['price_low']) else None
    settlement_days = row['settlement_days'] if pd.notna(row['settlement_days']) else None
    face_value = row['face_value'] if pd.notna(row['face_value']) else None
    bondCalendar = eval(row['bond_calendar']) if pd.notna(row['bond_calendar']) else None  # ql.UnitedStates.Settlement
    day_counter = eval(row['day_counter']) if pd.notna(row['day_counter']) else None  # ql.Thirty360.USA
    custom_date = row['custom_date'] if pd.notna(row['custom_date']) else None if pd.notna(row['custom_date']) else None

    call_date = ql.DateParser.parseFormatted(row['call_date'], '%m/%d/%Y') if pd.notna(
        row['call_date']) else None  # Dummy call date
    call_price = row['call_price'] if pd.notna(row['call_price']) else None
    spread = row['spread'] if pd.notna(row['spread']) else None
    shock_size = row['shock_size'] if pd.notna(row['shock_size']) else None  # Call price_mid at par
    benchmark_yield = row['benchmark_yield'] if pd.notna(row['benchmark_yield']) else None  # Dummy benchmark yield

    # Cusip
    print(f"Processing CUSIP: {cusip}")

    # Setup schedule and bond
    today = datetime.date.today()
    formatted_date = today.strftime('%Y-%m-%d') if custom_date is None else custom_date
    todays_date = ql.DateParser.parseFormatted(formatted_date, '%Y-%m-%d')
    print("Todays Date is: " + formatted_date)
    ql.Settings.instance().evaluationDate = todays_date

    # Schedule
    tenor = ql.Period(ql.Semiannual)
    convention = ql.Unadjusted
    terminationDateConvention = ql.Unadjusted
    DateGeneration_Rule = ql.DateGeneration.Backward
    endOfMonth = False
    schedule = ql.Schedule(issue_date, end_date, tenor,
                           bondCalendar, convention, terminationDateConvention,
                           DateGeneration_Rule, endOfMonth)

    # FixedRateBond
    paymentConvention = ql.Unadjusted
    bond = ql.FixedRateBond(settlement_days, face_value, schedule, [coupon_rate], day_counter,
                            paymentConvention)  # added ql.Unadjusted

    # Yield to Maturity (YTM)
    clean_price = price_mid
    ytm = bond.bondYield(clean_price, day_counter, ql.Compounded, ql.Semiannual)  # SimpleThenCompounded
    print(f"Yield to Maturity (YTM): {ytm * 100:.8f}%")

    # Duration and Convexity
    yield_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual)  # SimpleThenCompounded
    # yield_rate = ql.InterestRate(ytm, day_counter, ql.CompoundedThenSimple, ql.Semiannual)

    # Calculate duration and convexity
    duration_simple = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Simple)
    duration_Macaulay = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Macaulay)
    duration_modified = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Modified)
    effective_mod_duration = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Modified) / (1 + ytm / 2)
    effective_convexity = ql.BondFunctions.convexity(bond, yield_rate) / (1 + ytm / 2)
    convexity = ql.BondFunctions.convexity(bond, yield_rate) / 100

    print(f"Simple Duration: {duration_simple:.8f}")
    print(f"Macaulay Duration: {duration_Macaulay:.8f}")
    print(f"Modified Duration: {duration_modified:.8f}")
    print(f"Effective Modified Duration: {effective_mod_duration:.8f}")
    print(f"Effective Convexity: {effective_convexity:.8f}")
    print(f"Convexity: {convexity:.8f}")

    # Effective Yield using QuantLib
    effective_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual).equivalentRate(day_counter,
                                                                                                    ql.Compounded,
                                                                                                    ql.Annual,
                                                                                                    todays_date,
                                                                                                    end_date).rate()
    print(f"Effective Yield (using QuantLib): {effective_rate * 100:.8f}%")

    # Yield to Call (YTC) with Dummy Numbers
    ytc = bond.bondYield(call_price, day_counter, ql.Compounded, ql.Semiannual, call_date)
    print(f"Yield to Call with dummy (YTC) on {call_date}: {ytc * 100:.8f}%")

    # Yield to Worst (YTW) with Dummy Numbers
    ytw = min(ytm, ytc)  # Yield to worst is the minimum of YTM and YTC
    print(f"Yield to Worst (YTW): {ytw * 100:.8f}%")

    # Credit Duration with Dummy Numbers
    yield_rate_with_spread = ql.InterestRate(ytm + spread, day_counter, ql.Compounded, ql.Semiannual)
    credit_duration = ql.BondFunctions.duration(bond, yield_rate_with_spread, ql.Duration.Modified)
    print(f"Credit Duration (with dummy spread of {spread * 100:.2f}%): {credit_duration:.8f}")

    # Delta with Dummy Numbers
    yield_rate_shocked = ql.InterestRate(ytm + shock_size, day_counter, ql.Compounded, ql.Semiannual)
    delta = (ql.BondFunctions.cleanPrice(bond, yield_rate_shocked) - ql.BondFunctions.cleanPrice(bond,
                                                                                                 yield_rate)) / shock_size
    print(f"Delta (with dummy shock of {shock_size * 100:.2f}%): {delta:.8f}")

    # Spread to Curve with Dummy Numbers
    spread_to_curve = ytm - benchmark_yield
    print(f"Spread to Curve (with dummy benchmark yield of {benchmark_yield * 100:.2f}%): {spread_to_curve * 100:.8f}%")

    # Spread to Worst with Dummy Numbers
    spread_to_worst = ytw - benchmark_yield
    print(f"Spread to Worst (with dummy benchmark yield of {benchmark_yield * 100:.2f}%): {spread_to_worst * 100:.8f}%")

    # Subtract 10 days from January 1, 2024 using QuantLib Date
    initial_date = ql.Date(1, ql.January, 2024)
    new_date = initial_date - 10
    print(f"Initial Date: {initial_date}")
    print(f"New Date after subtracting 10 days: {new_date}")


# Iterate over each row in the CSV and process the bond data
for index, row in csv_data.iterrows():
    process_bond_data(row)
