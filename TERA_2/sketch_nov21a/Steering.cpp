#include "Steering.h"
#include "Arduino.h"
#define DIR 44      //suuna määramise pin
#define PUL 40      //steering pulse pin
#define TO_RIGHT 22   //teleop paremale keeramise pin
#define TO_LEFT 48    //teleop vasakule keeramise pin
#define STEERING_CYCLE 20 //keeramise kiirus
#define DELAY 100

Steering::Steering()
{
  pinMode(DIR, OUTPUT);
  pinMode(PUL, OUTPUT);
}

Steering::Left_Right(int value1, int value5, int encoder)
{
  if (value5 == 1)
  {
    encoder = encoder / 10;

//---------------------------------TELEOPIGA TAGASI KESKELE-----------------------------------------------------------------------------------------------------

    int difference = encoder - 267;
    //Serial.println(difference);
    if(digitalRead(TO_RIGHT) == 0 && digitalRead(TO_LEFT) == 0){

      if(difference < 0 &&  abs(difference) > 5){               //PAREMALE
      digitalWrite(DIR, LOW);   //PAREMALE

      for (int i = 0; i < STEERING_CYCLE; i++){    //ühe tsükli pikkus, mida suurem seda pikem ring
        //these 4 lines result in 1 step:
        digitalWrite(PUL, HIGH); //PIN 6 = stepPin
        delayMicroseconds(DELAY);
        digitalWrite(PUL, LOW);
        delayMicroseconds(DELAY);
      }
      }
      if(difference > 0 &&  abs(difference) > 5){               //VASAKULE
      digitalWrite(DIR, HIGH);   //VASAKULE

      for (int i = 0; i < STEERING_CYCLE; i++){    //ühe tsükli pikkus, mida suurem seda pikem ring
        //these 4 lines result in 1 step:
        digitalWrite(PUL, HIGH); //PIN 6 = stepPin
        delayMicroseconds(DELAY);
        digitalWrite(PUL, LOW);
        delayMicroseconds(DELAY);
      }
      }

    }
    
//-----------------------TELEOP KEERAMINE------------------------------------------------------------------------------------------------------------------

    //TULEB MUUTA PINID MILLELT SAAME INFOT KAS KEERAME VÕI EI (TO_RIGHT & TO_LEFT)

    if(digitalRead(TO_RIGHT) == 1){
      digitalWrite(DIR, LOW);   //PAREMALE

      for (int i = 0; i < STEERING_CYCLE; i++){    //ühe tsükli pikkus, mida suurem seda pikem ring
        //these 4 lines result in 1 step:
        digitalWrite(PUL, HIGH); //PIN 6 = stepPin
        delayMicroseconds(DELAY);
        digitalWrite(PUL, LOW);
        delayMicroseconds(DELAY);
      }
    }
    if(digitalRead(TO_LEFT) == 1){
      digitalWrite(DIR, HIGH);   //VASAKULE

      for (int i = 0; i < STEERING_CYCLE; i++){    //ühe tsükli pikkus, mida suurem seda pikem ring
        //these 4 lines result in 1 step:
        digitalWrite(PUL, HIGH); //PIN 6 = stepPin
        delayMicroseconds(DELAY);
        digitalWrite(PUL, LOW);
        delayMicroseconds(DELAY);
      }
    }
  }
  else if(value5 == 0)
  {
    encoder = encoder / 10;
    Serial.print(encoder);
    Serial.print("\n");

    int difference = encoder - value1;
    //Serial.println(difference);

    if(difference < 0 &&  abs(difference) > 5){
      digitalWrite(DIR, LOW);   //PAREMALE

      for (int i = 0; i < STEERING_CYCLE; i++){    //ühe tsükli pikkus, mida suurem seda pikem ring
        //these 4 lines result in 1 step:
        digitalWrite(PUL, HIGH); //PIN 6 = stepPin
        delayMicroseconds(DELAY);
        digitalWrite(PUL, LOW);
        delayMicroseconds(DELAY);
      }
    }
    if(difference > 0 && abs(difference) > 5){
      digitalWrite(DIR, HIGH);   //VASAKULE

      for (int i = 0; i < STEERING_CYCLE; i++){    //ühe tsükli pikkus, mida suurem seda pikem ring
        //these 4 lines result in 1 step:
        digitalWrite(PUL, HIGH); //PIN 6 = stepPin
        delayMicroseconds(DELAY);
        digitalWrite(PUL, LOW);
        delayMicroseconds(DELAY);
      }
    }
  }

}