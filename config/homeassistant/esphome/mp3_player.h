#include "esphome.h"
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

using namespace esphome;

// Receive Pin: 14 (D5)
// Transmit Pin: 4 (D2)
SoftwareSerial softwareSerial(D5, D2);
DFRobotDFPlayerMini dfplayer;

class MP3PlayerOutput : public Component, public BinaryOutput {

 public:

  void setup() override {
    softwareSerial.begin(9600);
    if (!dfplayer.begin(softwareSerial)) {
      while(true){
        delay(0);
      }
    }
    dfplayer.volume(30);
  }

  void write_state(bool state) override {
    if(state) {
      // Loop playing mp3 number #1
      dfplayer.loop(1);
    } else {
      dfplayer.stop();
    }
  }
};
