#include <iostream>
#include <stdio.h>
#include "LunarSolarConverter.h"
#include "lunar-xtelite.h"

int main()
{
    Solar s;
    Lunar l;

    int year= 2024, month = 11, day = 4;

    s.solarDay = day;
    s.solarMonth = month;
    s.solarYear = year;
    
    l = SolarToLunar(s);
    printf("%d %d %d %d\n", l.lunarDay, l.lunarMonth, l.lunarYear, l.isleap);

    lunar_t lunar;
    solar_t solar;

    SolarToLunar(year, month, day, lunar);
    cout << "음력 : " << lunar.year_lunar << " 년 " <<
            (int)lunar.month << " 월 " << (int)lunar.day << " 일" << endl;

    return 0;
}
