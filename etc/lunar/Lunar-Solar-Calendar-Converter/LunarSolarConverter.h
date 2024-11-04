//
//  LunarSolarConverter.h
//
//
//  Created by isee15 on 15/1/15.
//  Copyright (c) 2015年 isee15. All rights reserved.
//

#ifndef __ISEE15__LunarSolarConverter__
#define __ISEE15__LunarSolarConverter__

#include <stdio.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct Lunar
{
    bool isleap;
    int lunarDay;
    int lunarMonth;
    int lunarYear;
} Lunar;

typedef struct Solar
{
    int solarDay;
    int solarMonth;
    int solarYear;
} Solar;

Solar LunarToSolar(Lunar lunar);

Lunar SolarToLunar(Solar solar);

#ifdef __cplusplus
}
#endif


#endif /* defined(__ISEE15__LunarSolarConverter__) */
