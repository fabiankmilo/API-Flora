# Monarch VFD comunication module

# Dependencies
#import ipdb
import redis
import serial
import time
import binascii
import json

# Serial initialization
#ser = serial.Serial('/dev/serial0')

class Monarch(object):
	"""Implementation for an Elevator Monitor"""

	#### Definition of a Monitor ####

	def __init__(self, debug=True, uart='/dev/serial0', baudrate=9600,):

		super(Monarch, self).__init__()

		# VFD communication
		self.uart = uart
		self.baudrate = baudrate
		self.serial = serial.Serial(self.uart, baudrate=baudrate, timeout=1)
		self.vfd_connected = False

		# Redis communication
		self.redis_cli = redis.Redis()
		self.redis_sub = self.redis_cli.pubsub(ignore_subscribe_messages=True)

	#### Error handlers ####

	#### VFD communication ####

	# Connect to VFD through serial RS232 interface configured
	# with uart and baudrate. This function reads some registers to
	# determine whether the VFD is responding properly or not.
	def connect_to_vfd(self):
		self.vfd_connected = True

	# Subscribe to publish data channel
	def subscribe_and_write_data(self):
		self.redis_sub.subscribe(**{'write_data':self.write_data})
		print('Conected to write_data local')

	# Interact with the VFD, writing and reading registers
	def operate_register(self, register=None, data=None, function_code=3):
		#ipdb.set_trace()
		if not register:
			raise Exception('Register is required.')

		# Convert register number to VFD protocol
		validated_register = self.sanitize_register(register)

		# Slide parameter info and convert to integer
		parameter_function = validated_register[:2]
		parameter_number = validated_register[2:]
		parameter_function_int = int(parameter_function,16)
		parameter_number_int = int(parameter_number,16)
		# print('Parameter: ', validated_register)
		# print('Parameter int: ',parameter_function_int, ' ', parameter_number_int)

		if data != None:
			# Sanitize and Convert to hex
			new_value_hex = hex(data) # TODO: Sanitize
			# print('Data to write: ',new_value_hex) # DATA TO WRITE
			# Fill zeros
			if len(new_value_hex) == 5:
				new_value_hex = new_value_hex[:2]+'0'+new_value_hex[2:]
			elif len(new_value_hex) == 4:
				new_value_hex = new_value_hex[:2]+'0'+new_value_hex[2:]
				new_value_hex = new_value_hex[:2]+'0'+new_value_hex[2:]
			elif len(new_value_hex) == 3:
				new_value_hex = new_value_hex[:2]+'0'+new_value_hex[2:]
				new_value_hex = new_value_hex[:2]+'0'+new_value_hex[2:]
				new_value_hex = new_value_hex[:2]+'0'+new_value_hex[2:]
			print('Data to write: ',new_value_hex) # DATA TO WRITE WITH ZEROS
			# Delete '0x'
			new_value_hex = new_value_hex[2:]
			# Slide value info and convert to integer
			new_value_hex_first = new_value_hex[:2]
			new_value_hex_second = new_value_hex[2:]
			new_value_int_first = int(new_value_hex_first, 16)
			new_value_int_second = int(new_value_hex_second, 16)
			# print('Data to write int: ',new_value_int_first, ' ', new_value_int_second) # DATA TO WRITE INT
		else:
			new_value_hex = None
			new_value_int_first = None
			new_value_int_second = None

		# Convert data to vfd protocol
		data_to_send = self.convert_to_vfd_protocol(
			validated_register,
			parameter_function_int,
			parameter_number_int,
			new_value_hex,
			new_value_int_first,
			new_value_int_second,
			function_code
		)
		print('Data to send: ', data_to_send) # DATA TO SEND

		try:
			# Make request to VFD
			self.serial.write(data_to_send)
			time.sleep(0.1)
			# Read response of VFD
			response = self.serial.read(8)[4:6]
			s = binascii.hexlify(response)
			res = int(s,16)
			print('Response: ', res)
		except:
			print('[VFD]: Communication error')
			raise Exception('Communication error.')

		# Convert response to integer
		print(res)
		#register_data = self.convert_response_to_integer(res)
		return res

	# Sanitize register to match a valid VFD register
	def sanitize_register(self, register):
		# print('Register: ', register) # REGISTER
		parameter_number = register[2:]
		parameter_number_hex = hex(int(parameter_number))
		if len(parameter_number_hex) == 3:
			parameter_number_hex = parameter_number_hex[:2]+'0'+parameter_number_hex[2:]
		# Delete '0x'
		parameter_number_hex = parameter_number_hex[2:]
		sanitized_register = register[:2]+parameter_number_hex
		# print('Register sanitized: ', sanitized_register) # SANITIZED REGISTER
		return sanitized_register

	# Returns the binary data that would be sended to the VFD in order
	# to write or read some parameter
	def convert_to_vfd_protocol(self, register, first_byte, second_byte, data, data_first_byte, data_second_byte, function_code):
		# Create formats templates
		if function_code == 3:
			format = b"0103%s0001%s"
			format_2 = bytearray([0x01,0x03,first_byte, second_byte, 0x00, 0x01])
		elif function_code == 6:
			format = b"0106%s%s%s"
			format_2 = bytearray([0x01,0x06,first_byte, second_byte, data_first_byte, data_second_byte])
		else:
			format = b"0101%s0001%s"
			format_2 = bytearray([0x01,0x01,first_byte, second_byte, 0x00, 0x01])

		# Calculate CRC
		crc = self.computeCRC(format_2)
		crc_hex = hex(crc)

		if len(crc_hex) == 5:
			crc_hex = crc_hex[:2]+'0'+crc_hex[2:]
		elif len(crc_hex) == 4:
			crc_hex = crc_hex[:2]+'0'+crc_hex[2:]
			crc_hex = crc_hex[:2]+'0'+crc_hex[2:]
		if len(crc_hex) == 3:
			crc_hex = crc_hex[:2]+'0'+crc_hex[2:]
			crc_hex = crc_hex[:2]+'0'+crc_hex[2:]
			crc_hex = crc_hex[:2]+'0'+crc_hex[2:]
		print('CRC: '+crc_hex) # CRC

		#ipdb.set_trace()

		# Convert to hex
		if function_code == 6:
			hex_data = format % (str.encode(register), str.encode(data), str.encode(crc_hex[2:6]))
		else:
			hex_data = format % (str.encode(register), str.encode(crc_hex[2:6]))
		binary_array = binascii.unhexlify(hex_data)
		print('Binary to send: ', binary_array) # BINARY TO SEND
		return binary_array

	# Converts the VFD response into integer representarion
	def convert_response_to_integer(self, res):
		try:
			register_integer = int(binascii.hexlify(res[4:6]),16)
		except:
			return None
		return register_integer

	# Disconnet from VFD
	def disconnect(self):
		self.serial.uninit()

	# Generates a CRC16 table
	def __generate_crc16_table(self):
		result = []
		for byte in range(256):
			crc = 0x0000
			for _ in range(8):
				if (byte ^ crc) & 0x0001:
					crc = (crc >> 1) ^ 0xa001
				else: crc >>= 1
				byte >>= 1
			result.append(crc)
		return result

	# Calculates the CRC for a data packet
	def computeCRC(self, data):
		__crc16_table = self.__generate_crc16_table()
		byte2int = lambda b: b
		crc = 0xffff
		for a in data:
			idx = __crc16_table[(crc ^ byte2int(a)) & 0xff]
			crc = ((crc >> 8) & 0xff) ^ idx
		swapped = ((crc << 8) & 0xff00) | ((crc >> 8) & 0x00ff)
		return swapped

	def write_data(self, message):
		print('Sended to write')
		message = json.loads(message['data'])
		parameter = message['p']
		new_value = message['v']
		# Send data to vfd
		self.operate_register(
			parameter,
			int(new_value),
			6
		)

	

if __name__=="__main__":
	m = Monarch()
	m.subscribe_and_write_data()
	#f000
	f000_value = None
	f000_latest_value = None

	#f001
	f001_value = None
	f001_latest_value = None

	#f002
	f002_value = None
	f002_latest_value = None

	#f003
	f003_value = None
	f003_latest_value = None

	#f004
	f004_value = None
	f004_latest_value = None

	#f005
	f005_value = None
	f005_latest_value = None

	#f006
	f006_value = None
	f006_latest_value = None

	#f007
	f007_value = None
	f007_latest_value = None

	#f100
	f100_value = None
	f100_latest_value = None

	#f101
	f101_value = None
	f101_latest_value = None

	#f102
	f102_value = None
	f102_latest_value = None

	#f103
	f103_value = None
	f103_latest_value = None

	#f104
	f104_value = None
	f104_latest_value = None

	#f105
	f105_value = None
	f105_latest_value = None

	#f106
	f106_value = None
	f106_latest_value = None

	#f111
	f111_value = None
	f111_latest_value = None

	#f200
	f200_value = None
	f200_latest_value = None

	#f201
	f201_value = None
	f201_latest_value = None

	#f202
	f202_value = None
	f202_latest_value = None

	#f203
	f203_value = None
	f203_latest_value = None

	#f204
	f204_value = None
	f204_latest_value = None

	#f205
	f205_value = None
	f205_latest_value = None

	#f206
	f206_value = None
	f206_latest_value = None

	#f207
	f207_value = None
	f207_latest_value = None

	#f208
	f208_value = None
	f208_latest_value = None

	#f209
	f209_value = None
	f209_latest_value = None

	#f210
	f210_value = None
	f210_latest_value = None

	#f211
	f211_value = None
	f211_latest_value = None

	#f311
	f311_value = None
	f311_latest_value = None

	#f400
	f400_value = None
	f400_latest_value = None

	#f401
	f401_value = None
	f401_latest_value = None

	#f402
	f402_value = None
	f402_latest_value = None

	#f403
	f403_value = None
	f403_latest_value = None

	#f500
	f500_value = None
	f500_latest_value = None

	#f502
	f502_value = None
	f502_latest_value = None

	#f501
	f501_value = None
	f501_latest_value = None

	#f503
	f503_value = None
	f503_latest_value = None

	#f504
	f504_value = None
	f504_latest_value = None

	#f505
	f505_value = None
	f505_latest_value = None

	#f506
	f506_value = None
	f506_latest_value = None

	#f507
	f507_value = None
	f507_latest_value = None

	#f508
	f508_value = None
	f508_latest_value = None

	#f509
	f509_value = None
	f509_latest_value = None

	#f510
	f510_value = None
	f510_latest_value = None

	#f511
	f511_value = None
	f511_latest_value = None

	#f512
	f512_value = None
	f512_latest_value = None

	#f513
	f513_value = None
	f513_latest_value = None

	#f514
	f514_value = None
	f514_latest_value = None

	#f515
	f515_value = None
	f515_latest_value = None

	#f516
	f516_value = None
	f516_latest_value = None

	#f517
	f517_value = None
	f517_latest_value = None

	#f518
	f518_value = None
	f518_latest_value = None

	#f519
	f519_value = None
	f519_latest_value = None

	#f520
	f520_value = None
	f520_latest_value = None

	#f521
	f521_value = None
	f521_latest_value = None

	#f522
	f522_value = None
	f522_latest_value = None

	#f523
	f523_value = None
	f523_latest_value = None

	#f524
	f524_value = None
	f524_latest_value = None

	#f600
	f600_value = None
	f600_latest_value = None

	#f601
	f601_value = None
	f601_latest_value = None

	#f602
	f602_value = None
	f602_latest_value = None

	#f603
	f603_value = None
	f603_latest_value = None

	#f604
	f604_value = None
	f604_latest_value = None

	#f611
	f611_value = None
	f611_latest_value = None

	#f704
	f704_value = None
	f704_latest_value = None

	#f705
	f705_value = None
	f705_latest_value = None

	#f801
	f801_value = None
	f801_latest_value = None

	#f900
	f900_value = None
	f900_latest_value = None

	#f901
	f901_value = None
	f901_latest_value = None

	#f902
	f902_value = None
	f902_latest_value = None

	#f903
	f903_value = None
	f903_latest_value = None

	#f904
	f904_value = None
	f904_latest_value = None

	#f905
	f905_value = None
	f905_latest_value = None

	#f906
	f906_value = None
	f906_latest_value = None

	#f907
	f907_value = None
	f907_latest_value = None

	#f908
	f908_value = None
	f908_latest_value = None

	#f909
	f909_value = None
	f909_latest_value = None

	#f910
	f910_value = None
	f910_latest_value = None

	#f911
	f911_value = None
	f911_latest_value = None

	#f912
	f912_value = None
	f912_latest_value = None

	#f913
	f913_value = None
	f913_latest_value = None

	#f919
	f919_value = None
	f919_latest_value = None

	#fa03
	fa03_value = None
	fa03_latest_value = None

	#fa07
	fa07_value = None
	fa07_latest_value = None

	#fa11
	fa11_value = None
	fa11_latest_value = None

	#fa12
	fa12_value = None
	fa12_latest_value = None

	#fa18
	fa18_value = None
	fa18_latest_value = None

	#fa19
	fa19_value = None
	fa19_latest_value = None

	#fa21
	fa21_value = None
	fa21_latest_value = None

	#fa22
	fa22_value = None
	fa22_latest_value = None

	#fa23
	fa23_value = None
	fa23_latest_value = None

	#fa26
	fa26_value = None
	fa26_latest_value = None

	#fa33
	fa33_value = None
	fa33_latest_value = None

	#fc01
	fc01_value = None
	fc01_latest_value = None

	#fc20
	fc20_value = None
	fc20_latest_value = None

	#fc21
	fc21_value = None
	fc21_latest_value = None

	#fc24
	fc24_value = None
	fc24_latest_value = None

	#fc28
	fc28_value = None
	fc28_latest_value = None

	#fc60
	fc60_value = None
	fc60_latest_value = None


	while True:
		# Get write commands from cloud
		m.redis_sub.get_message()
		time.sleep(0.001)

		# Get VFD registers values
		# f000
		f000_value = m.operate_register('f000', None, 3)
		if (f000_value != f000_latest_value) and (f000_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f000','data':f000_value}))
			f000_latest_value = f000_value
			time.sleep(0.001)

		# f001
		f001_value = m.operate_register('f001', None, 3)
		if (f001_value != f001_latest_value) and (f001_value != None):
			print('publishhh')
			m.redis_cli.publish('publish_data', json.dumps({'register':'f001','data':f001_value}))
			f001_latest_value = f001_value
			time.sleep(0.001)

		# f002
		f002_value = m.operate_register('f002', None, 3)
		if (f002_value != f002_latest_value) and (f002_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f002','data':f002_value}))
			f002_latest_value = f002_value
			time.sleep(0.001)

		# f003
		f003_value = m.operate_register('f003', None, 3)
		print(f003_value)
		if (f003_value != f003_latest_value) and (f003_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f003','data':f003_value}))
			f003_latest_value = f003_value
			time.sleep(0.001)

		# f004
		f004_value = m.operate_register('f004', None, 3)
		if (f004_value != f004_latest_value) and (f004_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f004','data':f004_value}))
			f004_latest_value = f004_value
			time.sleep(0.001)

		# f005
		f005_value = m.operate_register('f005', None, 3)
		if (f005_value != f005_latest_value) and (f005_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f005','data':f005_value}))
			f005_latest_value = f005_value
			time.sleep(0.001)

		# f006
		f006_value = m.operate_register('f006', None, 3)
		if (f006_value != f006_latest_value) and (f006_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f006','data':f006_value}))
			f006_latest_value = f006_value
			time.sleep(0.001)

		# f007
		f007_value = m.operate_register('f007', None, 3)
		if (f007_value != f007_latest_value) and (f007_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f007','data':f007_value}))
			f007_latest_value = f007_value
			time.sleep(0.001)

		# f100
		f100_value = m.operate_register('f100', None, 3)
		if (f100_value != f100_latest_value) and (f100_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f100','data':f100_value}))
			f100_latest_value = f100_value
			time.sleep(0.001)

		# f101
		f101_value = m.operate_register('f101', None, 3)
		if (f101_value != f101_latest_value) and (f101_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f101','data':f101_value}))
			f101_latest_value = f101_value
			time.sleep(0.001)

		# f102
		f102_value = m.operate_register('f102', None, 3)
		if (f102_value != f102_latest_value) and (f102_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f102','data':f102_value}))
			f102_latest_value = f102_value
			time.sleep(0.001)

		# f103
		# wdt_2.feed()
		f103_value = m.operate_register('f103', None, 3)
		if (f103_value != f103_latest_value) and (f103_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f103','data':f103_value}))
			f103_latest_value = f103_value
			time.sleep(0.001)

		# f104
		# wdt_2.feed()
		f104_value = m.operate_register('f104', None, 3)
		if (f104_value != f104_latest_value) and (f104_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f104','data':f104_value}))
			f104_latest_value = f104_value
			time.sleep(0.001)

		# f105
		# wdt_2.feed()
		f105_value = m.operate_register('f105', None, 3)
		if (f105_value != f105_latest_value) and (f105_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f105','data':f105_value}))
			f105_latest_value = f105_value
			time.sleep(0.001)

		# f106
		# wdt_2.feed()
		f106_value = m.operate_register('f106', None, 3)
		if (f106_value != f106_latest_value) and (f106_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f106','data':f106_value}))
			f106_latest_value = f106_value
			time.sleep(0.001)

		# f111
		# wdt_2.feed()
		f111_value = m.operate_register('f111', None, 3)
		if (f111_value != f111_latest_value) and (f111_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f111','data':f111_value}))
			f111_latest_value = f111_value
			time.sleep(0.001)

		# f200
		# wdt_2.feed()
		f200_value = m.operate_register('f200', None, 3)
		if (f200_value != f200_latest_value) and (f200_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f200','data':f200_value}))
			f200_latest_value = f200_value
			time.sleep(0.001)

		# f201
		# wdt_2.feed()
		f201_value = m.operate_register('f201', None, 3)
		if (f201_value != f201_latest_value) and (f201_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f201','data':f201_value}))
			f201_latest_value = f201_value
			time.sleep(0.001)

		# f202
		# wdt_2.feed()
		f202_value = m.operate_register('f202', None, 3)
		if (f202_value != f202_latest_value) and (f202_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f202','data':f202_value}))
			f202_latest_value = f202_value
			time.sleep(0.001)

		# f203
		# wdt_2.feed()
		f203_value = m.operate_register('f203', None, 3)
		if (f203_value != f203_latest_value) and (f203_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f203','data':f203_value}))
			f203_latest_value = f203_value
			time.sleep(0.001)

		# f204
		# wdt_2.feed()
		f204_value = m.operate_register('f204', None, 3)
		if (f204_value != f204_latest_value) and (f204_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f204','data':f204_value}))
			f204_latest_value = f204_value
			time.sleep(0.001)

		# f205
		# wdt_2.feed()
		f205_value = m.operate_register('f205', None, 3)
		if (f205_value != f205_latest_value) and (f205_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f205','data':f205_value}))
			f205_latest_value = f205_value
			time.sleep(0.001)

		# f206
		# wdt_2.feed()
		f206_value = m.operate_register('f206', None, 3)
		if (f206_value != f206_latest_value) and (f206_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f206','data':f206_value}))
			f206_latest_value = f206_value
			time.sleep(0.001)

		# f207
		# wdt_2.feed()
		f207_value = m.operate_register('f207', None, 3)
		if (f207_value != f207_latest_value) and (f207_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f207','data':f207_value}))
			f207_latest_value = f207_value
			time.sleep(0.001)

		# f208
		# wdt_2.feed()
		f208_value = m.operate_register('f208', None, 3)
		if (f208_value != f208_latest_value) and (f208_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f208','data':f208_value}))
			f208_latest_value = f208_value
			time.sleep(0.001)

		# f209
		# wdt_2.feed()
		f209_value = m.operate_register('f209', None, 3)
		if (f209_value != f209_latest_value) and (f209_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f209','data':f209_value}))
			f209_latest_value = f209_value
			time.sleep(0.001)

		# f210
		# wdt_2.feed()
		f210_value = m.operate_register('f210', None, 3)
		if (f210_value != f210_latest_value) and (f210_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f210','data':f210_value}))
			f210_latest_value = f210_value
			time.sleep(0.001)

		# f211
		# wdt_2.feed()
		f211_value = m.operate_register('f211', None, 3)
		if (f211_value != f211_latest_value) and (f211_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f211','data':f211_value}))
			f211_latest_value = f211_value
			time.sleep(0.001)

		# f311
		# wdt_2.feed()
		f311_value = m.operate_register('f311', None, 3)
		if (f311_value != f311_latest_value) and (f311_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f311','data':f311_value}))
			f311_latest_value = f311_value
			time.sleep(0.001)

		# f400
		# wdt_2.feed()
		f400_value = m.operate_register('f400', None, 3)
		if (f400_value != f400_latest_value) and (f400_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f400','data':f400_value}))
			f400_latest_value = f400_value
			time.sleep(0.001)

		# f401
		# wdt_2.feed()
		f401_value = m.operate_register('f401', None, 3)
		if (f401_value != f401_latest_value) and (f401_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f401','data':f401_value}))
			f401_latest_value = f401_value
			time.sleep(0.001)

		# f402
		# wdt_2.feed()
		f402_value = m.operate_register('f402', None, 3)
		if (f402_value != f402_latest_value) and (f402_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f402','data':f402_value}))
			f402_latest_value = f402_value
			time.sleep(0.001)

		# f403
		# wdt_2.feed()
		f403_value = m.operate_register('f403', None, 3)
		if (f403_value != f403_latest_value) and (f403_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f403','data':f403_value}))
			f403_latest_value = f403_value
			time.sleep(0.001)

		# f500
		# wdt_2.feed()
		f500_value = m.operate_register('f500', None, 3)
		if (f500_value != f500_latest_value) and (f500_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f500','data':f500_value}))
			f500_latest_value = f500_value
			time.sleep(0.001)

		# f501
		# wdt_2.feed()
		f501_value = m.operate_register('f501', None, 3)
		if (f501_value != f501_latest_value) and (f501_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f501','data':f501_value}))
			f501_latest_value = f501_value
			time.sleep(0.001)

		# f502
		# wdt_2.feed()
		f502_value = m.operate_register('f502', None, 3)
		if (f502_value != f502_latest_value) and (f502_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f502','data':f502_value}))
			f502_latest_value = f502_value
			time.sleep(0.001)

		# f503
		# wdt_2.feed()
		f503_value = m.operate_register('f503', None, 3)
		if (f503_value != f503_latest_value) and (f503_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f503','data':f503_value}))
			f503_latest_value = f503_value
			time.sleep(0.001)

		# f504
		# wdt_2.feed()
		f504_value = m.operate_register('f504', None, 3)
		if (f504_value != f504_latest_value) and (f504_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f504','data':f504_value}))
			f504_latest_value = f504_value
			time.sleep(0.001)

		# f505
		# wdt_2.feed()
		f505_value = m.operate_register('f505', None, 3)
		if (f505_value != f505_latest_value) and (f505_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f505','data':f505_value}))
			f505_latest_value = f505_value
			time.sleep(0.001)

		# f506
		# wdt_2.feed()
		f506_value = m.operate_register('f506', None, 3)
		if (f506_value != f506_latest_value) and (f506_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f506','data':f506_value}))
			f506_latest_value = f506_value
			time.sleep(0.001)

		# f507
		# wdt_2.feed()
		f507_value = m.operate_register('f507', None, 3)
		if (f507_value != f507_latest_value) and (f507_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f507','data':f507_value}))
			f507_latest_value = f507_value
			time.sleep(0.001)

		# f508
		# wdt_2.feed()
		f508_value = m.operate_register('f508', None, 3)
		if (f508_value != f508_latest_value) and (f508_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f508','data':f508_value}))
			f508_latest_value = f508_value
			time.sleep(0.001)

		# f509
		# wdt_2.feed()
		f509_value = m.operate_register('f509', None, 3)
		if (f509_value != f509_latest_value) and (f509_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f509','data':f509_value}))
			f509_latest_value = f509_value
			time.sleep(0.001)

		# f510
		# wdt_2.feed()
		f510_value = m.operate_register('f510', None, 3)
		if (f510_value != f510_latest_value) and (f510_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f510','data':f510_value}))
			f510_latest_value = f510_value
			time.sleep(0.001)

		# f511
		# wdt_2.feed()
		f511_value = m.operate_register('f511', None, 3)
		if (f511_value != f511_latest_value) and (f511_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f511','data':f511_value}))
			f511_latest_value = f511_value
			time.sleep(0.001)

		# f512
		# wdt_2.feed()
		f512_value = m.operate_register('f512', None, 3)
		if (f512_value != f512_latest_value) and (f512_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f512','data':f512_value}))
			f512_latest_value = f512_value
			time.sleep(0.001)

		# f513
		# wdt_2.feed()
		f513_value = m.operate_register('f513', None, 3)
		if (f513_value != f513_latest_value) and (f513_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f513','data':f513_value}))
			f513_latest_value = f513_value
			time.sleep(0.001)

		# f514
		# wdt_2.feed()
		f514_value = m.operate_register('f514', None, 3)
		if (f514_value != f514_latest_value) and (f514_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f514','data':f514_value}))
			f514_latest_value = f514_value
			time.sleep(0.001)

		# f515
		# wdt_2.feed()
		f515_value = m.operate_register('f515', None, 3)
		if (f515_value != f515_latest_value) and (f515_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f515','data':f515_value}))
			f515_latest_value = f515_value
			time.sleep(0.001)

		# f516
		# wdt_2.feed()
		f516_value = m.operate_register('f516', None, 3)
		if (f516_value != f516_latest_value) and (f516_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f516','data':f516_value}))
			f516_latest_value = f516_value
			time.sleep(0.001)

		# f517
		# wdt_2.feed()
		f517_value = m.operate_register('f517', None, 3)
		if (f517_value != f517_latest_value) and (f517_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f517','data':f517_value}))
			f517_latest_value = f517_value
			time.sleep(0.001)

		# f518
		# wdt_2.feed()
		f518_value = m.operate_register('f518', None, 3)
		if (f518_value != f518_latest_value) and (f518_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f518','data':f518_value}))
			f518_latest_value = f518_value
			time.sleep(0.001)

		# f519
		# wdt_2.feed()
		f519_value = m.operate_register('f519', None, 3)
		if (f519_value != f519_latest_value) and (f519_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f519','data':f519_value}))
			f519_latest_value = f519_value
			time.sleep(0.001)

		# f520
		# wdt_2.feed()
		f520_value = m.operate_register('f520', None, 3)
		if (f520_value != f520_latest_value) and (f520_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f520','data':f520_value}))
			f520_latest_value = f520_value
			time.sleep(0.001)

		# f521
		# wdt_2.feed()
		f521_value = m.operate_register('f521', None, 3)
		if (f521_value != f521_latest_value) and (f521_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f521','data':f521_value}))
			f521_latest_value = f521_value
			time.sleep(0.001)

		# f522
		# wdt_2.feed()
		f522_value = m.operate_register('f522', None, 3)
		if (f522_value != f522_latest_value) and (f522_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f522','data':f522_value}))
			f522_latest_value = f522_value
			time.sleep(0.001)

		# f523
		# wdt_2.feed()
		f523_value = m.operate_register('f523', None, 3)
		if (f523_value != f523_latest_value) and (f523_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f523','data':f523_value}))
			f523_latest_value = f523_value
			time.sleep(0.001)

		# f524
		# wdt_2.feed()
		f524_value = m.operate_register('f524', None, 3)
		if (f524_value != f524_latest_value) and (f524_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f524','data':f524_value}))
			f524_latest_value = f524_value
			time.sleep(0.001)

		# f600
		f600_value = m.operate_register('f600', None, 3)
		if (f600_value != f600_latest_value) and (f600_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f600','data':f600_value}))
			f600_latest_value = f600_value
			time.sleep(0.001)

		# f601
		f601_value = m.operate_register('f601', None, 3)
		if (f601_value != f601_latest_value) and (f601_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f601','data':f601_value}))
			f601_latest_value = f601_value
			time.sleep(0.001)

		# f602
		f602_value = m.operate_register('f602', None, 3)
		if (f602_value != f602_latest_value) and (f602_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f602','data':f602_value}))
			f602_latest_value = f602_value
			time.sleep(0.001)

		# f603
		f603_value = m.operate_register('f603', None, 3)
		if (f603_value != f603_latest_value) and (f603_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f603','data':f603_value}))
			f603_latest_value = f603_value
			time.sleep(0.001)

		# f604
		f604_value = m.operate_register('f604', None, 3)
		if (f604_value != f604_latest_value) and (f604_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f604','data':f604_value}))
			f604_latest_value = f604_value
			time.sleep(0.001)

		# f611
		f611_value = m.operate_register('f611', None, 3)
		if (f611_value != f611_latest_value) and (f611_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f611','data':f611_value}))
			f611_latest_value = f611_value
			time.sleep(0.001)

		# f704
		f704_value = m.operate_register('f704', None, 3)
		if (f704_value != f704_latest_value) and (f704_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f704','data':f704_value}))
			f704_latest_value = f704_value
			time.sleep(0.001)

		# f705
		f705_value = m.operate_register('f705', None, 3)
		if (f705_value != f705_latest_value) and (f705_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f705','data':f705_value}))
			f705_latest_value = f705_value
			time.sleep(0.001)

		# f801
		# wdt_2.feed()
		f801_value = m.operate_register('f801', None, 3)
		if (f801_value != f801_latest_value) and (f801_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f801','data':f801_value}))
			f801_latest_value = f801_value
			time.sleep(0.001)

		# f900
		# wdt_2.feed()
		f900_value = m.operate_register('f900', None, 3)
		if (f900_value != f900_latest_value) and (f900_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f900','data':f900_value}))
			f900_latest_value = f900_value
			time.sleep(0.001)

		# f901
		# wdt_2.feed()
		f901_value = m.operate_register('f901', None, 3)
		if (f901_value != f901_latest_value) and (f901_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f901','data':f901_value}))
			f901_latest_value = f901_value
			time.sleep(0.001)

		# f902
		# wdt_2.feed()
		f902_value = m.operate_register('f902', None, 3)
		if (f902_value != f902_latest_value) and (f902_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f902','data':f902_value}))
			f902_latest_value = f902_value
			time.sleep(0.001)

		# f903
		# wdt_2.feed()
		f903_value = m.operate_register('f903', None, 3)
		if (f903_value != f903_latest_value) and (f903_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f903','data':f903_value}))
			f903_latest_value = f903_value
			time.sleep(0.001)

		# f904
		# wdt_2.feed()
		f904_value = m.operate_register('f904', None, 3)
		if (f904_value != f904_latest_value) and (f904_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f904','data':f904_value}))
			f904_latest_value = f904_value
			time.sleep(0.001)

		# f905
		# wdt_2.feed()
		f905_value = m.operate_register('f905', None, 3)
		if (f905_value != f905_latest_value) and (f905_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f905','data':f905_value}))
			f905_latest_value = f905_value
			time.sleep(0.001)

		# f906
		# wdt_2.feed()
		f906_value = m.operate_register('f906', None, 3)
		if (f906_value != f906_latest_value) and (f906_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f906','data':f906_value}))
			f906_latest_value = f906_value
			time.sleep(0.001)

		# f907
		# wdt_2.feed()
		f907_value = m.operate_register('f907', None, 3)
		if (f907_value != f907_latest_value) and (f907_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f907','data':f907_value}))
			f907_latest_value = f907_value
			time.sleep(0.001)

		# f908
		# wdt_2.feed()
		f908_value = m.operate_register('f908', None, 3)
		if (f908_value != f908_latest_value) and (f908_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f908','data':f908_value}))
			f908_latest_value = f908_value
			time.sleep(0.001)

		# f909
		# wdt_2.feed()
		f909_value = m.operate_register('f909', None, 3)
		if (f909_value != f909_latest_value) and (f909_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f909','data':f909_value}))
			f909_latest_value = f909_value
			time.sleep(0.001)

		# f910
		# wdt_2.feed()
		f910_value = m.operate_register('f910', None, 3)
		if (f910_value != f910_latest_value) and (f910_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f910','data':f910_value}))
			f910_latest_value = f910_value
			time.sleep(0.001)

		# f911
		# wdt_2.feed()
		f911_value = m.operate_register('f911', None, 3)
		if (f911_value != f911_latest_value) and (f911_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f911','data':f911_value}))
			f911_latest_value = f911_value
			time.sleep(0.001)

		# f912
		# wdt_2.feed()
		f912_value = m.operate_register('f912', None, 3)
		if (f912_value != f912_latest_value) and (f912_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f912','data':f912_value}))
			f912_latest_value = f912_value
			time.sleep(0.001)

		# f913
		# wdt_2.feed()
		f913_value = m.operate_register('f913', None, 3)
		if (f913_value != f913_latest_value) and (f913_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f913','data':f913_value}))
			f913_latest_value = f913_value
			time.sleep(0.001)

		# f919
		# wdt_2.feed()
		f919_value = m.operate_register('f919', None, 3)
		if (f919_value != f919_latest_value) and (f919_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'f919','data':f919_value}))
			f919_latest_value = f919_value
			time.sleep(0.001)

		### Slower

		# fa03
		# wdt_2.feed()
		fa03_value = m.operate_register('fa03', None, 3)
		if (fa03_value != fa03_latest_value) and (fa03_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa03','data':fa03_value}))
			fa03_latest_value = fa03_value
			time.sleep(0.001)	

		fa07_value = m.operate_register('fa07', None, 3)
		if (fa07_value != fa07_latest_value) and (fa07_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa07','data':fa07_value}))
			fa07_latest_value = fa07_value
			time.sleep(0.001)	

		fa11_value = m.operate_register('fa11', None, 3)
		if (fa11_value != fa11_latest_value) and (fa11_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa11','data':fa11_value}))
			fa11_latest_value = fa11_value
			time.sleep(0.001)

		fa12_value = m.operate_register('fa12', None, 3)
		if (fa12_value != fa12_latest_value) and (fa12_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa12','data':fa12_value}))
			fa12_latest_value = fa12_value
			time.sleep(0.001)	

		# fa18
		# wdt_2.feed()
		fa18_value = m.operate_register('fa18', None, 3)
		if (fa18_value != fa18_latest_value) and (fa18_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa18','data':fa18_value}))
			fa18_latest_value = fa18_value
			time.sleep(0.001)

		# fa19
		# wdt_2.feed()
		fa19_value = m.operate_register('fa19', None, 3)
		if (fa19_value != fa19_latest_value) and (fa19_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa19','data':fa19_value}))
			fa19_latest_value = fa19_value
			time.sleep(0.001)

		# fa21
		# wdt_2.feed()
		fa21_value = m.operate_register('fa21', None, 3)
		if (fa21_value != fa21_latest_value) and (fa21_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa21','data':fa21_value}))
			fa21_latest_value = fa21_value
			time.sleep(0.001)

		# fa22
		# wdt_2.feed()
		fa22_value = m.operate_register('fa22', None, 3)
		if (fa22_value != fa22_latest_value) and (fa22_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa22','data':fa22_value}))
			fa22_latest_value = fa22_value
			time.sleep(0.001)

		# fa23
		# wdt_2.feed()
		fa23_value = m.operate_register('fa23', None, 3)
		if (fa23_value != fa23_latest_value) and (fa23_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa23','data':fa23_value}))
			fa23_latest_value = fa23_value
			time.sleep(0.001)

		# fa26
		# wdt_2.feed()
		fa26_value = m.operate_register('fa26', None, 3)
		if (fa26_value != fa26_latest_value) and (fa26_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa26','data':fa26_value}))
			fa26_latest_value = fa26_value
			time.sleep(0.001)

		# fa33
		# wdt_2.feed()
		fa33_value = m.operate_register('fa33', None, 3)
		if (fa33_value != fa33_latest_value) and (fa33_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fa33','data':fa33_value}))
			fa33_latest_value = fa33_value
			time.sleep(0.001)

		# fc01
		fc01_value = m.operate_register('fc01', None, 3)
		if (fc01_value != fc01_latest_value) and (fc01_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fc01','data':fc01_value}))
			fc01_latest_value = fc01_value
			time.sleep(0.001)

		# fc20
		fc20_value = m.operate_register('fc20', None, 3)
		if (fc20_value != fc20_latest_value) and (fc20_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fc20','data':fc20_value}))
			fc20_latest_value = fc20_value
			time.sleep(0.001)

		# fc21
		# wdt_2.feed()
		fc21_value = m.operate_register('fc21', None, 3)
		if (fc21_value != fc21_latest_value) and (fc21_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fc21','data':fc21_value}))
			fc21_latest_value = fc21_value
			time.sleep(0.001)

		# fc24
		# wdt_2.feed()
		fc24_value = m.operate_register('fc24', None, 3)
		if (fc24_value != fc24_latest_value) and (fc24_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fc24','data':fc24_value}))
			fc24_latest_value = fc24_value
			time.sleep(0.001)

		# fc28
		# wdt_2.feed()
		fc28_value = m.operate_register('fc28', None, 3)
		if (fc28_value != fc28_latest_value) and (fc28_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fc28','data':fc28_value}))
			fc28_latest_value = fc28_value
			time.sleep(0.001)

		# fc60
		fc60_value = m.operate_register('fc60', None, 3)
		if (fc60_value != fc60_latest_value) and (fc60_value != None):
			m.redis_cli.publish('publish_data', json.dumps({'register':'fc60','data':fc60_value}))
			fc60_latest_value = fc60_value
			time.sleep(0.001)
