#include <Arduino.h>
#include <Wire.h>
#include "MPU9250.h"

#define MARG_SDA 2
#define MARG_SCL 3

#define WAIT_FOR_SERIAL true

MPU9250 IMU(Wire1,0x68);
int status;

MPU9250 bruteForce_imu(MPU9250 &IMU, int &status);
bool scan_I2C();

void setup() {
  Serial.begin(115200);
#if WAIT_FOR_SERIAL
  while(!Serial) {}
#endif
  Wire1.setSDA(MARG_SDA);
  Wire1.setSCL(MARG_SCL);
  Wire1.begin();

  scan_I2C();

  //bruteForce_imu(IMU, status);
  status = IMU.begin();
  IMU.disableDataReadyInterrupt();
  
  // setting the accelerometer full scale range to +/-8G 
  IMU.setAccelRange(MPU9250::ACCEL_RANGE_8G);
  // setting the gyroscope full scale range to +/-500 deg/s
  IMU.setGyroRange(MPU9250::GYRO_RANGE_500DPS);
  // setting DLPF bandwidth to 20 Hz
  IMU.setDlpfBandwidth(MPU9250::DLPF_BANDWIDTH_20HZ);
  // setting SRD to 19 for a 50 Hz update rate
  Serial.println(IMU.setSrd(19));
  delay(5000);
}

void loop() {
  IMU.readSensor();
  Serial.print(IMU.getGyroX_rads());
  Serial.print("\t");
  Serial.print(IMU.getGyroY_rads());
  Serial.print("\t");
  Serial.print(IMU.getGyroZ_rads());
  Serial.print("\t");
  Serial.print("\t");
  Serial.print(IMU.getAccelX_mss());
  Serial.print("\t");
  Serial.print(IMU.getAccelY_mss());
  Serial.print("\t");
  Serial.print(IMU.getAccelZ_mss());
  delay(100);

}

MPU9250 bruteForce_imu(MPU9250 &IMU, int &status) {
  while(true) {
    MPU9250 IMU(Wire1,0x69);
    status = IMU.begin();
    delay(100);
    Serial.print(status);
    if (status >= 0) {
      break;
    }
  }
  return IMU;
}

bool scan_I2C() {
  bool ret;
  Serial.println("\nI2C Scanner");
  while(true){
    byte error, address;
  int nDevices;
  Serial.println("Scanning...");
  nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    Wire1.beginTransmission(address);
    error = Wire1.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address<16) {

        
        Serial.print("0");
      }
      Serial.println(address,HEX);
      nDevices++;
    }
    else if (error==4) {
      Serial.print("Unknow error at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.println(address,HEX);
    }    
  }
  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
    ret = false;
  }
  else {
    Serial.println("done\n");
    ret = true;
    break;
  }
  delay(5000);    
  }
  return ret;
}