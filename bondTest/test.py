import QuantLib as ql
import datetime

#P8
issue_date = ql.Date(30, 5, 1995)
end_date = ql.Date(30, 5, 2025)
coupon_rate = 0.0875
price = 102.788
settlement_days = 2
face_value = 100.0
bondCalendar = ql.Canada()
day_counter  = ql.ActualActual(ql.ActualActual.ISMA)

# day_counter = ql.Actual365Fixed(ql.Actual365Fixed.Standard)
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/daycounters/actualactual.hpp#L51
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/daycounters/thirty360.cpp
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/calendars/unitedstates.hpp

# Setup schedule and bond
today = datetime.date.today()
formatted_date = today.strftime('%Y-%m-%d')
todays_date = ql.DateParser.parseFormatted(formatted_date, '%Y-%m-%d')
print("Todays Date is: "+formatted_date)
ql.Settings.instance().evaluationDate = todays_date



#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/schedule.hpp
# schedule = ql.Schedule(issue_date, end_date, ql.Period(ql.Semiannual),
#                        bondCalendar , ql.Unadjusted, ql.Unadjusted,
#                        ql.DateGeneration.Backward, False)
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/businessdayconvention.hpp#L41
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/dategenerationrule.hpp#L39
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/compounding.hpp#L32
convention = ql.Unadjusted
terminationDateConvention = ql.Unadjusted
DateGeneration_Rule = ql.DateGeneration.Backward
endOfMonth = False
schedule = ql.Schedule(issue_date, end_date, ql.Period(ql.Semiannual),
                       bondCalendar , convention , terminationDateConvention ,
                       DateGeneration_Rule, endOfMonth)
# https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/instruments/bonds/fixedratebond.cpp
# https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/instruments/bond.cpp#L251
paymentConvention = ql.Unadjusted
bond = ql.FixedRateBond(settlement_days, face_value, schedule, [coupon_rate], day_counter, paymentConvention )  #added ql.Unadjusted

#debug_price = bond.dirtyPrice(coupon_rate,ql.ActualActual(ql.ActualActual.ISMA),ql.Compounded,ql.Annual)-bond.accruedAmount(todays_date)
#print("debug_price: "+str(debug_price))
#https://quant.stackexchange.com/questions/68450/quantlib-match-clean-price-with-bbg-clean-price
#print(round(fixedRateBond.dirtyPrice(0.025,ql.ActualActual(ql.ActualActual.ISMA),
#ql.Compounded,ql.Annual),6)-round(fixedRateBond.accruedAmount(ql.Date(15,10,2021)),3))

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
