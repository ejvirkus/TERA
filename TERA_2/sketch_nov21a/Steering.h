#ifndef Steering_h
#define Steering_h
#include "Arduino.h"

class Steering
{
  public:
    Steering();
    int Left_Right(int value1, int value5, int encoder, uint16_t wheel);

  private:

};

#endif
