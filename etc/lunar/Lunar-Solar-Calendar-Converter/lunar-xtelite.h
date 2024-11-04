//#include <iostream.h>
//#include <cstring.h>

//using namespace std;

enum BOOL { FALSE = 0, TRUE};

typedef struct _lunar_info
{
	unsigned short	year_lunar;		// 음력 변환후 년도 (양력과 다를 수 있음)
	unsigned short  year_dangi;		// 당해년도 단기
	unsigned char	month;			// 음력 변환후 달 
	unsigned char	day;			// 음력 변환후 일
	unsigned char	dayofweek;		// 주중 요일을 숫자로 ( 0:일, 1:월 ... 6:토)
	bool			isyoondal;		// 윤달 여부 0:평달/1:윤달
	char			h_year[5];		// 당해 년도 갑자표기 (한글)
	char			h_day1[3];		// 요일 (한글)
	char			h_day2[5];		// 당일 갑자표기 (한글)
	char			h_ddi[7];		// 당해 년도 띠 표기 (한글)
	char			c_year[5];		// 당해 년도 갑자표기 (한자)
	char			c_day1[3];		// 요일 (한자)
	char			c_day2[5];		// 당일 갑자표기 (한자)
} lunar_t;

typedef struct _solar_info
{
	unsigned short	year;			// 양력 변환후 년도 (음력과 다를 수 있음)
	unsigned char	month;			// 양력 변환후 달 
	unsigned char	day;			// 양력 변환후 일
	unsigned char	dayofweek;		// 주중 요일을 숫자로 ( 0:일, 1:월 ... 6:토)
} solar_t;


// 이 음력 계산은 1841 ~ 2043 년도 범위에서 정확도를 제공합니다.
// 만약 정확한지 검사해보고 싶다면 다음 사이트에서 비교해 보시오.
// http://www.koreamanse.com/hotservice/yangumch/yangumch.html?mode=2
// http://ruby.kisti.re.kr/~manse/ <= 한국 과학기술 연구원
BOOL SolarToLunar(int Year, int Month, int Day, lunar_t& lunar);
BOOL LunarToSolar(int Year, int Month, int Day, BOOL Leaf, solar_t& solar);
