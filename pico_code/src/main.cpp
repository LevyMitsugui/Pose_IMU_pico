#include <BMI160Gen.h>            //https://github.com/hanyazou/BMI160-Arduino
#include <Wire.h>

#define SDA_PIN 0
#define SCL_PIN 1
 
// I2C Configuration for ESP32
const int i2c_addr = 0x68;  // Default I2C address for BMI160

long pico_time = 0;
long prev_time = 0;
long cycle = 200;	// cycle period in milliseconds

int gx, gy, gz; // Raw gyroscope values
int ax, ay, az; // Raw accelerometer values

void setup() {
  Serial.begin(115200);
  while (!Serial);


  Wire.setSDA(SDA_PIN);
  Wire.setSCL(SCL_PIN);
  Wire.begin();
 

  if (!BMI160.begin(BMI160GenClass::I2C_MODE, i2c_addr)) {
    Serial.println("BMI160 initialization failed!");
    while (1); // Halt if initialization fails
  }
 
  //Serial.println("BMI160 initialized successfully in I2C mode!");
}
 
void loop() {
  pico_time = millis();
  if ((pico_time - prev_time) > cycle) {
    prev_time = pico_time;
  
    BMI160.readGyro(gx, gy, gz); 
    BMI160.readAccelerometer(ax, ay, az);
  
    Serial.print(((float)pico_time)/1000, 3);
    Serial.print("\t");
    Serial.print(gx);
    Serial.print("\t");
    Serial.print(gy);
    Serial.print("\t");
    Serial.print(gz);
    Serial.print("\t");
    Serial.print(ax);
    Serial.print("\t");
    Serial.print(ay);
    Serial.print("\t");
    Serial.println(az);
  }
}