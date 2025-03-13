#include <iostream>
#include <stdio.h>
#include "LunarSolarConverter.h"
#include "lunar-xtelite.h"

int main()
{
    Solar s;
    Lunar l;

    int year= 2024, month = 11, day = 12;
    int day_in_month[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    s.solarDay = day;
    s.solarMonth = month;
    s.solarYear = year;
    
    l = SolarToLunar(s);
    printf("%d %d %d %d\n", l.lunarDay, l.lunarMonth, l.lunarYear, l.isleap);

    lunar_t lunar;
    solar_t solar;

    SolarToLunar(year, month, day, lunar);
    std::cout << "음력 : " << lunar.year_lunar << " 년 " <<
            (int)lunar.month << " 월 " << (int)lunar.day << " 일" << (int)lunar.isyoondal << std::endl;

    //for (year = 1841; year <= 2043; year++) {
    for (year = 2024; year <= 2026; year++) {
        day_in_month[2-1] = 28;
        if (year%4 == 0) day_in_month[2-1] = 29;
        if (year%100 == 0) day_in_month[2-1] = 28;
        if (year%400 == 0) day_in_month[2-1] = 29;
        for (month = 1; month <= 12; month++) {
            int days = day_in_month[month-1];
            for (day = 1; day <= days; day++) {
                s.solarDay = day;
                s.solarMonth = month;
                s.solarYear = year;
                l = SolarToLunar(s);
                SolarToLunar(year, month, day, lunar);
                if (lunar.year_lunar != l.lunarYear || lunar.month != l.lunarMonth || lunar.day != l.lunarDay || lunar.isyoondal != l.isleap) {
                    std::cout << year << month << day << std::endl;
                    printf("%d %d %d %d\n", l.lunarDay, l.lunarMonth, l.lunarYear, l.isleap);
                    std::cout << "음력 : " << lunar.year_lunar << " 년 " <<
                            (int)lunar.month << " 월 " << (int)lunar.day << " 일" << (int)lunar.isyoondal << std::endl;
                }
            }
        }
    }

    return 0;
}
