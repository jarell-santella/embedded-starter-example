
* Using SPI0
* Enable in /boot/uEnv.txt
	uboot overlay addr5=/lib/firmware/BB-SPIDEV0-00A0.dtbo
	(enables pins; view with `show-pins`)
* Test
	https://github.com/derekmolloy/exploringBB/blob/version2/chp08/spi/spidev_test/spidev_test.c
	- Change constant for which SPI channel to use.
* Test
  - Install
	sudo apt install spi-tools
  - Query config
	sudo spi-config -d /dev/spidev0.0 -q
  - Setup (Mode 0)
	// ?? sudo spi-config -d /dev/spidev0.0 -q
	
* Disable I2C1 (/dev/i2c-1)
	?? Nothing.. unneeded? 
			
* C:
-install lgpio
	(done)
		wget https://github.com/joan2937/lg/archive/master.zip
		unzip master.zip
	cd lg-master
	make
	sudo make install		# Fails on python, but still works.
- Build C sample
	cd c
	make
	sudo ./main 1.54
- Changes:
	DEV_Config.h:
		```
		#define USE_DEV_LIB 1
		#define LCD_CS   60     // P9.12    <-- UNUSED (but it sets to output)
		#define LCD_RST  31     // P9.13    
		#define LCD_DC   30     // P9.11
		#define LCD_BL   60     // ??       <-- Set to output, set to 1.
		```
		
	DEV_Config.c:
		- DEV_ModuleInit 
			- Ensure using lgGpiochipOpen(0);
			- Ensure using lgSpiOpen(0, 0, 25000000, 0);
