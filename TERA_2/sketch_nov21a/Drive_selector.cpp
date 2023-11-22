#include "Drive_selector.h"
#include "Arduino.h"

Drive_selector_switch::Drive_selector_switch()
{

}

int Drive_selector_switch::Drive_mode(int value3, int value6)
{
  if(value6 == 1) //Honda
  {
    analogWrite(8, value3);
    return 1;
  }
  else if(value6 == 2) //Audi
  {
    analogWrite(7, value3);
    analogWrite(8, value3);
    return 2;
  }
  else if(value6 == 3) //BMW
  {
    analogWrite(7, value3);
    return 3;
  }
}