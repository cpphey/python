import QuantLib as ql
import datetime

#https://pdfcoffee.com/bloomberg-per-security-manual-pdf-free.html
#http://aspenres.com/bbgupgrade/bbfields.tbl

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
# bondCalendar = ql.Canada()

#https://treasurydirect.gov/auctions/auction-query/?cusip=912810UE6
# issue_date = ql.Date(15, 11, 2024)
# end_date = ql.Date(15, 11, 2054)
# coupon_rate = 0.045
# price = 98.253773
# settlement_days = 2
# face_value = 100.0
# bondCalendar =  ql.UnitedStates(ql.UnitedStates.GovernmentBond)

#Y8
# issue_date = ql.Date(31, 12, 2008)
# end_date = ql.Date(1, 11, 2031)
# coupon_rate = 0.08
# price_mid = 111.361
# price_high = 99.704
# price_low = 99.704
# settlement_days = 1
# face_value = 100.0
# bondCalendar =  ql.UnitedStates(ql.UnitedStates.Settlement)
# day_counter = ql.Thirty360(ql.Thirty360.USA)

#B8
# issue_date = ql.Date(5, 2, 1996)
# end_date = ql.Date(5, 2, 2026)
# coupon_rate = 0.0845
# price = 106.0025
# settlement_days = 2
# face_value = 100.0
# bondCalendar = ql.Canada()
# day_counter  = ql.ActualActual(ql.ActualActual.ISMA)

#P8
# issue_date = ql.Date(30, 5, 1995)
# end_date = ql.Date(30, 5, 2025)
# coupon_rate = 0.0875
# price = 102.788
# settlement_days = 1
# face_value = 100.0
# bondCalendar = ql.Canada()
# day_counter  = ql.ActualActual(ql.ActualActual.ISMA)

#p4
# issue_date = ql.Date(28, 10, 2014)
# end_date = ql.Date(1, 5, 2025)
# coupon_rate = 0.05
# price = 99.704
# settlement_days = 0
# face_value = 100.0
# bondCalendar =  ql.UnitedStates(ql.UnitedStates.Settlement)
# day_counter = ql.Thirty360(ql.Thirty360.USA)


#g38
# issue_date = ql.Date(17, 11, 2014)
# end_date = ql.Date(15, 11, 2024)
# coupon_rate = 0.0225
# price = 100.185 #99.31
# settlement_days = 2
# face_value = 100.0
# bondCalendar =  ql.UnitedStates(ql.UnitedStates.GovernmentBond)
# day_counter = ql.Thirty360(ql.Thirty360.USA)

#W7
# issue_date = ql.Date(15, 1, 2016)
# end_date = ql.Date(15, 1, 2026)
# coupon_rate = 0.0571
# price = 99.8875
# settlement_days = 2
# face_value = 100.0
# bondCalendar =  ql.UnitedStates(ql.UnitedStates.Settlement)
# day_counter = ql.Thirty360(ql.Thirty360.USA)

#1AH2
# issue_date = ql.Date(28,4,2016)
# end_date = ql.Date(15,4,2026)
# coupon_rate = 0.05375
# price = 100.0115
# settlement_days = 1
# face_value = 100.0
# bondCalendar =  ql.UnitedStates(ql.UnitedStates.Settlement)
# day_counter = ql.Thirty360(ql.Thirty360.USA)

#GAE3
# issue_date = ql.Date(11,3,2014)
# end_date = ql.Date(15,3,2044)
# coupon_rate = 0.05375
# price = 93.117
# settlement_days = 1
# face_value = 100.0
# bondCalendar =  ql.UnitedStates(ql.UnitedStates.Settlement)
# day_counter = ql.Thirty360(ql.Thirty360.USA)

#2AS5
# issue_date = ql.Date(10,5,2017)
# end_date = ql.Date(15,3,2027)
# coupon_rate = 0.05
# price = 100.458
# settlement_days = 1
# face_value = 100.0
# bondCalendar = ql.UnitedStates(ql.UnitedStates.Settlement)
# day_counter = ql.Thirty360(ql.Thirty360.USA)

#VAB2
# issue_date = ql.Date(8,2,2017)
# end_date = ql.Date(15,8,2026)
# coupon_rate = 0.05125
# price = 99.9125
# settlement_days = 1
# face_value = 100.0
# bondCalendar =  ql.UnitedStates(ql.UnitedStates.Settlement)
# day_counter = ql.Thirty360(ql.Thirty360.USA)
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/daycounters/actualactual.hpp#L51
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/daycounters/thirty360.cpp
#https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/time/calendars/unitedstates.hpp

#00206RLJ
issue_date = ql.Date(3, 9, 2021)
end_date = ql.Date(15, 9, 2055)
coupon_rate = 0.0355
price_mid = 68.581
price_high = None
price_low = None
settlement_days = 1
face_value = 100.0
bondCalendar = ql.UnitedStates(ql.UnitedStates.Settlement)
day_counter = ql.Thirty360(ql.Thirty360.USA)

#002824BG
issue_date = ql.Date(22, 11, 2016)
end_date = ql.Date(30, 11, 2036)
coupon_rate = 0.0475
price_mid = 97.2848
price_high = None
price_low = None
settlement_days = 1
face_value = 100.0
bondCalendar = ql.UnitedStates(ql.UnitedStates.Settlement)
day_counter = ql.Thirty360(ql.Thirty360.USA)

#00440EAW
issue_date = ql.Date(3, 11, 2015)
end_date = ql.Date(3, 11, 2045)
coupon_rate = 0.0435
price_mid = 86.5435
price_high = None
price_low = None
settlement_days = 1
face_value = 100.0
bondCalendar = ql.UnitedStates(ql.UnitedStates.Settlement)
day_counter = ql.Thirty360(ql.Thirty360.USA)

#00817YAF
issue_date = ql.Date(9, 6, 2006)
end_date = ql.Date(15, 6, 2036)
coupon_rate = 0.06625
price_mid = 107.1281
price_high = None
price_low = None
settlement_days = 1
face_value = 100.0
bondCalendar = ql.UnitedStates(ql.UnitedStates.Settlement)
day_counter = ql.Thirty360(ql.Thirty360.USA)

#00817YAZ
issue_date = ql.Date(10, 8, 2017)
end_date = ql.Date(15, 8, 2047)
coupon_rate = 0.03875
price_mid = 73.0595
price_high = None
price_low = None
settlement_days = 1
face_value = 100.0
bondCalendar = ql.UnitedStates(ql.UnitedStates.Settlement)
day_counter = ql.Thirty360(ql.Thirty360.USA)

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
schedule = ql.Schedule(issue_date, end_date, ql.Period(ql.Semiannual),
                       bondCalendar , ql.Following , ql.Following ,
                       ql.DateGeneration.Backward, False)
# https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/instruments/bonds/fixedratebond.cpp
# https://github.com/lballabio/QuantLib/blob/1aae34679f0abd852b6dc90c72cd6deafbdb5c1e/ql/instruments/bond.cpp#L251
bond = ql.FixedRateBond(settlement_days, face_value, schedule, [coupon_rate], day_counter, ql.Unadjusted )  #added ql.Unadjusted

debug_price = bond.dirtyPrice(coupon_rate,ql.ActualActual(ql.ActualActual.ISMA),ql.Compounded,ql.Annual)-bond.accruedAmount(todays_date)

#https://quant.stackexchange.com/questions/68450/quantlib-match-clean-price-with-bbg-clean-price
#print(round(fixedRateBond.dirtyPrice(0.025,ql.ActualActual(ql.ActualActual.ISMA),
#ql.Compounded,ql.Annual),6)-round(fixedRateBond.accruedAmount(ql.Date(15,10,2021)),3))
print("debug")

# Yield to Maturity (YTM)
clean_price = price
ytm = bond.bondYield(clean_price, day_counter, ql.Compounded, ql.Semiannual) #SimpleThenCompounded
ytm = bond.bondYield(clean_price, day_counter, ql.Compounded, ql.Semiannual)
print(f"Yield to Maturity (YTM): {ytm * 100:.4f}%")


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
