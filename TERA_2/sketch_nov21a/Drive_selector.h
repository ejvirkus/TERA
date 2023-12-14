#ifndef Drive_selector_h
#define Drive_selector_h
#include "Arduino.h"

class Drive_selector_switch
{
  public:
    Drive_selector_switch();
    int Drive_mode(int value3, int value6, int throttle, int value5);

  private:
    int _value3;
    int _value6;

};

#endif
