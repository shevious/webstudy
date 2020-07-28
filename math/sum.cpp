#include <stdio.h>

int pow(int n)
{
  if (n >= 1)
    return 2*pow(n-1);
  else
    return 1;
}

int main()
{
  int sum = 0;
  for (int i = 0; i < 32; i++)
    sum += pow(i);

  printf("%d\n", sum);
}
