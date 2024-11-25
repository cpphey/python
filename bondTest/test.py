import QuantLib as ql
import datetime

#031162DR
issue_date = ql.Date(2, 3, 2023)
end_date = ql.Date(2, 3, 2033)
coupon_rate = 0.0525
price_mid = 100.0738
price_high = None
price_low = None
settlement_days = 1
face_value = 100.0
bondCalendar = ql.UnitedStates(ql.UnitedStates.Settlement)
day_counter = ql.Thirty360(ql.Thirty360.USA)
custom_date =  '2024-11-22'
#day_counter  = ql.ActualActual(ql.ActualActual.ISMA)

call_date = ql.Date(1, 5, 2023)  # Dummy call date
call_price = 100.0  # Call price_mid at par
spread = 0.01  # Dummy credit spread of 1%
shock_size = 0.01  # Dummy interest rate shock of 1%
benchmark_yield = 0.03  # Dummy benchmark yield of 3%


# Setup schedule and bond
today = datetime.date.today()
formatted_date = today.strftime('%Y-%m-%d') if custom_date is None else custom_date
todays_date = ql.DateParser.parseFormatted(formatted_date, '%Y-%m-%d')
print("Todays Date is: "+formatted_date)
ql.Settings.instance().evaluationDate = todays_date

#Schedule
tenor = ql.Period(ql.Semiannual)
convention = ql.Unadjusted
terminationDateConvention = ql.Unadjusted
DateGeneration_Rule = ql.DateGeneration.Backward
endOfMonth = False
schedule = ql.Schedule(issue_date, end_date, tenor,
                       bondCalendar , convention , terminationDateConvention ,
                       DateGeneration_Rule, endOfMonth)

#FixedRateBond
paymentConvention = ql.Unadjusted
bond = ql.FixedRateBond(settlement_days, face_value, schedule, [coupon_rate], day_counter, paymentConvention )  #added ql.Unadjusted

# Yield to Maturity (YTM)
clean_price = price_mid
ytm = bond.bondYield(clean_price, day_counter, ql.Compounded, ql.Semiannual) #SimpleThenCompounded
print(f"Yield to Maturity (YTM): {ytm * 100:.8f}%")

# Duration and Convexity
yield_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual)#SimpleThenCompounded
#yield_rate = ql.InterestRate(ytm, day_counter, ql.CompoundedThenSimple, ql.Semiannual)

# Calculate duration and convexity
duration_simple = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Simple)
#duration_Macaulay = ql.BondFunctions.duration(bond, yield_rate.compounding(), day_counter, ql.CompoundedThenSimple,  ql.Semiannual, ql.Duration.Macaulay)
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
effective_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual).equivalentRate(day_counter, ql.Compounded, ql.Annual, todays_date, end_date).rate()
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
delta = (ql.BondFunctions.cleanPrice(bond, yield_rate_shocked) - ql.BondFunctions.cleanPrice(bond, yield_rate)) / shock_size
print(f"Delta (with dummy shock of {shock_size * 100:.2f}%): {delta:.8f}")

# Spread to Curve with Dummy Numbers
spread_to_curve = ytm - benchmark_yield
print(f"Spread to Curve (with dummy benchmark yield of {benchmark_yield * 100:.2f}%): {spread_to_curve * 100:.8f}%")

# Spread to Worst with Dummy Numbers
spread_to_worst = ytw - benchmark_yield
print(f"Spread to Worst (with dummy benchmark yield of {benchmark_yield * 100:.2f}%): {spread_to_worst * 100:.8f}%")
