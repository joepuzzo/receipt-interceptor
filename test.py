from escpos.printer import Serial

# Initialize a Serial printer object with the correct port and baud rate
p = Serial(devfile='/dev/ttyUSB0', baudrate=9600, profile="TM-T20II")

# Send some commands to the emulated printer
p.text("Hello World\n")
p.cut()
