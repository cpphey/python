import QuantLib as ql
import datetime

#p4
issue_date = ql.Date(28, 10, 2014)
end_date = ql.Date(1, 5, 2025)
coupon_rate = 0.05
price = 99.704
settlement_days = 0
face_value = 100.0
bondCalendar =  ql.UnitedStates(ql.UnitedStates.Settlement)
day_counter = ql.Thirty360(ql.Thirty360.USA)
#day_counter  = ql.ActualActual(ql.ActualActual.ISMA)@al

# Setup schedule and bond
custom_date = None #'2024-11-18'
today = datetime.date.today()
formatted_date = today.strftime('%Y-%m-%d') if custom_date is None else custom_date
todays_date = ql.DateParser.parseFormatted(formatted_date, '%Y-%m-%d')
print("Todays Date is: "+formatted_date)
ql.Settings.instance().evaluationDate = todays_date

#Schedule
convention = ql.Unadjusted
terminationDateConvention = ql.Unadjusted
DateGeneration_Rule = ql.DateGeneration.Backward
endOfMonth = False
schedule = ql.Schedule(issue_date, end_date, ql.Period(ql.Semiannual),
                       bondCalendar , convention , terminationDateConvention ,
                       DateGeneration_Rule, endOfMonth)
#FixedRateBond
paymentConvention = ql.Unadjusted
bond = ql.FixedRateBond(settlement_days, face_value, schedule, [coupon_rate], day_counter, paymentConvention )  #added ql.Unadjusted

# Yield to Maturity (YTM)
clean_price = price
ytm = bond.bondYield(clean_price, day_counter, ql.Compounded, ql.Semiannual) #SimpleThenCompounded
print(f"Yield to Maturity (YTM): {ytm * 100:.8f}%")

# Duration and Convexity
#yield_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual)#SimpleThenCompounded
yield_rate = ql.InterestRate(ytm, day_counter, ql.CompoundedThenSimple, ql.Semiannual)

# Calculate duration and convexity
duration_simple = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Simple)
duration_modified = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Modified)
convexity = ql.BondFunctions.convexity(bond, yield_rate) / 100

print(f"Simple Duration: {duration_simple:.8f}")
# print(f"Modified Duration: {duration_modified:.8f}")
print(f"Convexity: {convexity:.8f}")
