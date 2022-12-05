#include <Servo.h>

int motorPin = 3;
int hallSensorPin = A0;
int servoPin = 5;

Servo arm;

int speed;
int arm_angle = 168;
double tolerance = 1;
int offset = 500;

double d = 1804/8; // bit delay of first ring, 225.5
int r = 2.73; // radius of first ring
int bit_rings[] = {8, 14, 20, 26, 32, 38, 44};
double rotations[] = {7, 4.5, 3.5, 4, 4.5, 5.5, 0};
double bit_delays[] = {d, 8*d/14, 8*d/20, 8*d/26, 8*d/32, 8*d/38, 8*d/44}; // each ring takes 8*d
int ring = 0;
int bit_num = 0;

int bits[182] = {};
int bit_avg[44] = {}; // init to 0, temporarily hold ring reading before average
int num_rev = 7; // num of cycles to take avg of
int bit_val;

void jostleMotor(){
  analogWrite(motorPin, 200);
  delay(100);
  analogWrite(motorPin, 100);
}

void setup() {
  pinMode(motorPin, OUTPUT);
  pinMode(hallSensorPin, INPUT);
  Serial.begin(9600);
  arm.attach(servoPin);
  arm.write(arm_angle);
  delay(1000); 
  jostleMotor();
}

void loop() {
//  speed = Serial.parseInt();
//  if (speed > 0) {
//      Serial.println(speed);
//      if (speed >= 0 && speed <= 255) {
//         Serial.println("setting speed to " + String(speed));
//         analogWrite(motorPin, speed);
//      }
//  }

    double delayTime = 0;

    for(int revo=0; revo<num_rev; revo++){
      for(int i=0; i<bit_rings[ring]; i++){
        double h_voltage = analogRead(hallSensorPin); // offset @ 500mV, low -
        
//        Serial.println("voltage: " + String(h_voltage)); 
        if(h_voltage > offset + tolerance) { bit_val = 1; }
        else if(h_voltage < offset - tolerance) { bit_val = 0; }
        else { bit_val = 0; } // freespace as 0
  
        bit_avg[i] += bit_val;
        delayTime += bit_delays[ring];
        delay(bit_delays[ring]);
      }
  
      for(int bval : bit_avg){
        Serial.print(String(bval) + " ");
      }
      Serial.println();
    }

    Serial.println("Writing ring " + String(ring) + " to bits array.");

    for(int i=0; i<bit_rings[ring]; i++){
      int avg = bit_avg[i] >= (num_rev+1)/2 ? 1 : 0;
      bits[bit_num] = avg;
      Serial.println("BIT: " + String(bit_num) + ", Value:" + String(avg));
      bit_num += 1;
    }

    memset(bit_avg,0,sizeof(bit_avg)); // reset bit_avg to 0s
    
    Serial.println("Ring " + String(ring) + "delay time: " + String(delayTime));
//    analogWrite(motorPin, 0);

    // update arm for next ring
    Serial.println("writing arm");
    arm_angle = (arm_angle > 141) ? arm_angle - rotations[ring] : arm_angle;
    Serial.println(arm_angle);
    arm.write(arm_angle);
    delay(8*d); // wait full revolution before reading 


    // update ring
    ring += 1;
    if(ring > 6){
       Serial.println("Read " + String(bit_num) + " bits.");
       for(int i=0; i<182; i++){
         Serial.print(String(bits[i]) + " ");
       }
       analogWrite(motorPin, 0);
       Serial.println();
       for( ; ; );
    }

}
