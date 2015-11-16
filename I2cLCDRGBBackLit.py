#Python mraa I2c LCD with RGB background led 
#tested with seeedstudio Grove LCD RGB Backlight and Intel Edison
#Willem-Jan Derks 2015
#"Improved" by Trent Monahan, 2015

#!/usr/bin/python
import mraa
import time

#LCD Instructions
#0x01 Clear display and return to the home position
#0x02 Returns cursor and shift home, screen not cleared
#0x08 + 0x04 Display on
#0x08 + 0x02 Cursor on
#0x08 + 0x01 Cursor Blink on
#0x10 + 0x08 Shift display left
#0x10 + 0x0c Shift display right
#0x10 + 0x00 Shift cursor left
#0x10 + 0x04 Shift cursor right
#0x80 + Address line1 0x00-0x27 line2 0x28-0x4F
class I2CLCDDisplay():
	def __init__(self):
		self.LCD = self.I2cLCDInit()
		self.LCDLED = self.I2cLCDLEDInit()
		
	def LCDInstruction(self, instruction):
		self.LCD.writeReg(0x80,instruction)
		time.sleep(0.05)

	def I2cLCDInit(self):
		LCD = mraa.I2c(0)
		LCD.address(0x3e)
		LCD.writeReg(0x80,0x38) #8Bit, 2lines, 5x7
		time.sleep(0.05)
		LCD.writeReg(0x80,0x08+0x07) #display on, cursor on, blink on
		time.sleep(0.05)
		LCD.writeReg(0x80,0x01) #clear display, cursor 1st line, 1st character
		return(LCD)

	def I2cLCDLEDInit(self):
			LCDLED = mraa.I2c(0)
			LCDLED.address(0x62)
			LCDLED.writeReg(0,0)
			LCDLED.writeReg(1,0)
			LCDLED.writeReg(0x08,0xaa)
			return(LCDLED)

	def LCDPrint(self, text):
		for letter in text:
				self.LCD.writeReg(0x40,ord(letter))
					
	def LEDColor(self, R,G,B):
			self.LCDLED.writeReg(4,R)
			self.LCDLED.writeReg(3,G)
			self.LCDLED.writeReg(2,B)
			return

#Only do the example functionality when called directly (not when imported)
if __name__ == "__main__":
	LCDDisplay = I2CLCDDisplay()
	LCDDisplay.LEDColor(255,255,255) #RGB
	LCDDisplay.LCDPrint("Hello World!")
	LCDDisplay.LCDInstruction(0x80+0x28)
	LCDDisplay.LCDPrint("Line2")

	#cycle through RGB
	while True:
			for i in range(0, 255):
					LCDDisplay.LEDColor(i,0,255-i)
					time.sleep(0.005)
			for i in range(0, 255):
					LCDDisplay.LEDColor(255-i,i,0)
					time.sleep(0.005)
			for i in range(0, 255):
					LCDDisplay.LEDColor(0,255-i,i)
					time.sleep(0.005)
