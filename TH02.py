#TH02 by Trent Monahan, 2015
#ported from Intel's UPM TH02 in C

import mraa

TH02_ADDR = 0x40 # device address
TH02_REG_STATUS = 0x00
TH02_REG_DATA_H = 0x01
TH02_REG_DATA_L = 0x02
TH02_REG_CONFIG = 0x03
TH02_REG_ID     = 0x11

TH02_STATUS_RDY_MASK = 0x01

TH02_CMD_MEASURE_HUMI = 0x01
TH02_CMD_MEASURE_TEMP = 0x11

class TH02:
	def __init__(self, bus=0, addr=TH02_ADDR):
		"""
		Instantiates a TH02 object
		"""
		self._address = addr
		self._name = "TH02"
		
		self.i2c = mraa.I2c(bus)
		if self.i2c.address(self._address) != mraa.SUCCESS:
			raise ValueError("mraa_i2c_address() failed")
		
		#TODO: Check if its MRAA_SUCCESS
	def getTemperature(self):
		"""
		Gets the temperature value from the sensor
		"""
		if self.i2c.writeReg(TH02_REG_CONFIG, TH02_CMD_MEASURE_TEMP):
			raise RuntimeError("I2C.WriteReg() failed")
			return 0.0
		while self.getStatus() == False:
			pass
		temperature = self.i2c.readReg(TH02_REG_DATA_H) << 8
		temperature = temperature | self.i2c.readReg(TH02_REG_DATA_L)
		temperature = temperature >> 2
		return (temperature / 32.0) - 50.0 #is conversion needed?
	def getHumidity(self):
		"""
		Gets the humidity value from the sensor
		"""
		if self.i2c.writeReg(TH02_REG_CONFIG, TH02_CMD_MEASURE_HUMI):
			raise RuntimeError("I2C.WriteReg() failed")
			return 0.0
		while self.getStatus() == False:
			pass
		humidity = self.i2c.readReg(TH02_REG_DATA_H) << 8
		humidity = humidity | self.i2c.readReg(TH02_REG_DATA_L)
		humidity = humidity >> 4
		return (humidity / 16.0) - 24.0 #is conversion needed?
	def getStatus(self):
		"""
		Gets the sensor status
		"""
		status = self.i2c.readReg(TH02_REG_STATUS)
		if status & TH02_STATUS_RDY_MASK:
			return False
		else:
			return True
	def name(self):
		"""
		Returns the name of the component
		"""
		return self._name #TH02
