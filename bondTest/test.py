import QuantLib as ql
import datetime

#2AS5
issue_date = ql.Date(10,5,2017)
end_date = ql.Date(15,3,2027)
coupon_rate = 0.05 #0.049845
price = 100.129
settlement_days = 1
face_value = 100.0
bondCalendar =  ql.UnitedStates(ql.UnitedStates.Settlement)
day_counter = ql.Thirty360(ql.Thirty360.USA)
# day_counter  = ql.ActualActual(ql.ActualActual.ISMA)

# Setup schedule and bond
today = datetime.date.today()
formatted_date = today.strftime('%Y-%m-%d')
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
ytm = bond.bondYield(clean_price, day_counter, ql.Compounded, ql.Semiannual)
print(f"Yield to Maturity (YTM): {ytm * 100:.8f}%")


# Duration and Convexity
#yield_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual)#SimpleThenCompounded
yield_rate = ql.InterestRate(ytm, day_counter, ql.SimpleThenCompounded, ql.Semiannual)

# Calculate duration and convexity
duration_simple = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Simple)
duration_modified = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Modified)
convexity = ql.BondFunctions.convexity(bond, yield_rate) / 100

print(f"Simple Duration: {duration_simple:.8f}")
#print(f"Modified Duration: {duration_modified:.8f}")
print(f"Convexity: {convexity:.8f}")
