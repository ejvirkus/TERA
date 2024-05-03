#include "Odumetry.h"
#include "Arduino.h"
#include <string.h>

#define L1 5
#define L2 6
#define L3 7

#define R1 2
#define R2 3
#define R3 4

Odumetry_data::Odumetry_data()
{
  pinMode(L1, INPUT);
  pinMode(L2, INPUT);
  pinMode(L3, INPUT);

  pinMode(R1, INPUT);
  pinMode(R2, INPUT);
  pinMode(R3, INPUT);

}

int Odumetry_data::readOdumetryData() 
{
  int FL_ticks = 0;
  String FL = "";
  String prev_FL = "000";

  FL = String(digitalRead(R1)) + String(digitalRead(R2)) + String(digitalRead(R3));

  if(prev_FL != FL)
  {
    FL_ticks += 1;
    prev_FL = FL;
  }
  return FL_ticks;
}
