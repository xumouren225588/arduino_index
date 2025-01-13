// 引入 Arduino 核心库
#include <Arduino.h>

// 定义 LED 引脚，假设 LED 连接到数字引脚 13
const int ledPin = 13;

void setup() {
  // 初始化 LED 引脚为输出模式
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // 点亮 LED
  digitalWrite(ledPin, HIGH);
  // 等待 1000 毫秒（1 秒）
  delay(1000);
  // 熄灭 LED
  digitalWrite(ledPin, LOW);
  // 等待 1000 毫秒（1 秒）
  delay(1000);
}