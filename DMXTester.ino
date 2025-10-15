/*
  DMXTester.ino

  Simple DMX transmitter sketch for Arduino Pro Mini (5V/16MHz).
  Drives a DMX/RS485 breakout (e.g., MAX485) to send a single channel burst
  that turns a fog machine on for 3 seconds, then off for 5 seconds, looping.

  Wiring (assuming MAX485 style board):
    Pro Mini TX (D1)  ->  RO (receive-out)  [unused, leave unconnected]
    Pro Mini RX (D0)  ->  DI (driver input)
    Pro Mini D2       ->  DE & /RE (tie pins together, digital enable)
    Pro Mini VCC      ->  VCC on module (5V)
    Pro Mini GND      ->  GND on module
    Module A/B screw terminals -> DMX line (A=Data+, B=Data-)

  Requires Conceptinetics DMX library:
    https://github.com/alfo/Conceptinetics

  Install through Arduino Library Manager: Sketch > Include Library > Manage Libraries > search "Conceptinetics".
*/

#include <Conceptinetics.h>

// DMX universe configuration
constexpr uint16_t DMX_CHANNELS = 4;  // keep small; we only use channel 1
constexpr uint8_t DMX_PIN = 2;        // controls DE + /RE on RS485 transceiver

// Fog channel setup
constexpr uint8_t FOG_CHANNEL = 1;
constexpr uint8_t FOG_ON_VALUE = 255;
constexpr uint8_t FOG_OFF_VALUE = 0;
constexpr uint16_t FOG_ON_TIME_MS = 3000;
constexpr uint16_t FOG_OFF_TIME_MS = 5000;

DMX_Master dmx_controller(DMX_CHANNELS, DMX_PIN);

void setup()
{
  // Initialize DMX controller; use auto refresh at ~44Hz default
  dmx_controller.enable();
  dmx_controller.setChannelRange(1, DMX_CHANNELS, 0); // blackout
}

void loop()
{
  dmx_controller.setChannelValue(FOG_CHANNEL, FOG_ON_VALUE);
  delay(FOG_ON_TIME_MS);

  dmx_controller.setChannelValue(FOG_CHANNEL, FOG_OFF_VALUE);
  delay(FOG_OFF_TIME_MS);
}

