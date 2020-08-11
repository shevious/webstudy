#include <stdio.h>

int pow(int n)
{
  if (n >= 1)
    return 2*pow(n-1);
  else
    return 1;
}

int pow_sum(int n)
{
  int sum = 0;
  for (int i = 0; i < n; i++)
    sum += pow(i);
  return sum;
}

int main()
{
  printf("1: %d\n", pow_sum(1));
  printf("2: %d\n", pow_sum(2));
  printf("3: %d\n", pow_sum(3));
  printf("...\n");
  printf("30: %d\n", pow_sum(30));
  printf("31: %d\n", pow_sum(31));
  printf("32: %d\n", pow_sum(32));
}
