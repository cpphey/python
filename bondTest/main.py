import QuantLib as ql
import datetime



#Input data
#559665AB0
#US559665AB08
# issue_date = ql.Date(26, 11, 2024)
# end_date = ql.Date(1, 12, 2032)
# coupon_rate = 0.06875
# price = 100.86951
# settlement_days = 2
# face_value = 100.0
#bondCalendar = ql.UnitedStates()

# issue_date = ql.Date(1, 11, 2024)
# end_date = ql.Date(3, 6, 2030)
# coupon_rate = 0.04513
# price = 100.171
# settlement_days = 2
# face_value = 100.0
#bondCalendar = ql.UnitedStates()

#https://treasurydirect.gov/auctions/announcements-data-results/
#https://treasurydirect.gov/auctions/auction-query/?cusip=912810UE6
# issue_date = ql.Date(1, 11, 2024)
# end_date = ql.Date(1, 11, 2031)
# coupon_rate = 0.06625
# price = 101.0625
# settlement_days = 2
# face_value = 100.0
bondCalendar = ql.Canada()

#https://treasurydirect.gov/auctions/auction-query/?cusip=912810UE6
issue_date = ql.Date(15, 11, 2024)
end_date = ql.Date(15, 11, 2054)
coupon_rate = 0.045
price = 98.253773
settlement_days = 2
face_value = 100.0
#bondCalendar = ql.UnitedStates()

# Setup schedule and bond
today = datetime.date.today()
formatted_date = today.strftime('%Y-%m-%d')
todays_date = ql.DateParser.parseFormatted(formatted_date, '%Y-%m-%d')
print("Todays Date is: "+formatted_date)
ql.Settings.instance().evaluationDate = todays_date

#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/schedule.hpp
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/schedule.cpp
# schedule = ql.Schedule(issue_date, end_date, ql.Period(ql.Semiannual),
#                        bondCalendar , ql.Unadjusted, ql.Unadjusted,
#                        ql.DateGeneration.Backward, False)
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/businessdayconvention.hpp#L41
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/dategenerationrule.hpp#L39
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/compounding.hpp#L32
schedule = ql.Schedule(issue_date, end_date, ql.Period(ql.Semiannual),
                       bondCalendar , ql.Following , ql.Following ,
                       ql.DateGeneration.Backward, False)

day_counter = ql.Thirty360(ql.Thirty360.USA)
bond = ql.FixedRateBond(settlement_days, face_value, schedule, [coupon_rate], day_counter)

# Yield to Maturity (YTM)
clean_price = price
ytm = bond.bondYield(clean_price, day_counter, ql.Compounded, ql.Semiannual) #SimpleThenCompounded
print(f"Yield to Maturity (YTM): {ytm * 100:.4f}%")
# bond.dirtyPrice()
# print(str())

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
