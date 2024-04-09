int cs_pin = 30;
int data_pin = 32;
int clock_pin = 28;

void setup() {
  Serial.begin(9600);
  pinMode(cs_pin, OUTPUT);
  pinMode(data_pin, INPUT);
  pinMode(clock_pin, OUTPUT);
  /*
  _cs_pin = cs_pin;
  _data_pin = data_pin;
  _clock_pin = clock_pin;
  */

}


void loop() {
  int reading = 0;
  // Pull CS low to select the encoder
  digitalWrite(cs_pin, LOW);
  // Read 12 bits from the encoder
  for (int i = 0; i < 12; i++) {
    // Toggle the clock
    digitalWrite(clock_pin, HIGH);
    delayMicroseconds(1); // Short delay for clock pulse
    digitalWrite(clock_pin, LOW);
    // Read a bit of data
    reading <<= 1;
    if (digitalRead(data_pin)) {
      reading |= 1;
    }
    delayMicroseconds(1);
  }
  // Pull CS high to deselect the encoder
  digitalWrite(cs_pin, HIGH);
  
  Serial.println(reading);
}
