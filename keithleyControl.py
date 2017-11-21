#!/usr/bin/env/python3

import sys, time, math
from serial import *

class keithley:

    def __init__(self):
        #
        # Open port
        #
        #Syntax: serial.Serial(port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE,
        #                      stopbits=STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False,
        #                      writeTimeout=None, dsrdtr=False, interCharTimeout=None)
        self.port = Serial('COM4', baudrate=57600, bytesize=8, parity=PARITY_ODD, xonxoff=True)

    def init(self):
        #
        # Custom settings
        #

        # Reset Keithley
        self.port.write("*RST\r\n".encode());
        # Disable hardware beeper
        self.port.write(":SYST:BEEP:STAT OFF\r\n".encode());
        # Set voltage source to constant voltage output
        self.port.write(":SOUR:VOLT:MODE FIX\r\n".encode());
        # Set output voltage to zero
        self.port.write(":SOUR:VOLT:IMM:AMPL 0\r\n".encode());
        # Voltage output on rear panel plugs
        self.port.write(":ROUT:TERM REAR\r\n".encode());
        # Set compliance to 100uA
        self.port.write(":CURR:PROT:LEV 100E-6\r\n".encode())

    def setCompliance(self,complcurrent=100):

        # Set hardware compliance limit
        if not isInt(complcurrent):
            print("Wrong input format, only integer numbers allowed for compliance limit (in uA)")
        else:
            self.port.write((":CURR:PROT:LEV %sE-6\r\n" %(complcurrent)).encode() )

    def setVoltage(self,voltage=0):

        # Set bias voltage
        if not isInt(voltage):
            print("Wrong input format, only integer numbers allowed for voltage")
        else:
            self.port.write((":SOUR:VOLT:IMM:AMPL %s\r\n" %(-abs(voltage))).encode() )
            self.port.write(":OUTP:STAT 1\r\n".encode())

    def readCurrent(self):

        self.port.write(":READ?\r\n".encode())
        line = self.port.readline().decode()
        splitted = line.split(",")
        return splitted[1]

    def readVoltage(self):

        self.port.write(":READ?\r\n".encode())
        line = self.port.readline().decode()
        splitted = line.split(",")
        return splitted[0][1:]

    def reset(self):

        # Set output: off
        # Clear error messages
        # Load Presettings
        # Init custom settings

        self.port.write(":OUTP:STAT 0\r\n".encode())
        self.port.write("*CLS\r\n".encode())
        self.port.write(":SYST:PRES\r\n".encode())
        self.init()

    def close(self):

        # Set output: off
        # Reset Keithley
        # Clear error messages
        # Load Presettings
        # Set "LOCAL" mode
        # Close connection

        self.port.write(":OUTP:STAT 0\r\n".encode())
        self.port.write("*RST\r\n".encode())
        self.port.write("*CLS\r\n".encode())
        self.port.write(":SYST:PRES\r\n".encode())
        self.port.write(":SYST:KEY 23\r\n".encode())
        self.port.close()

    def help(self):

        print("\nKeithley 2410 Commandline Control Program")
        print("(c) 2015, IEKP Karlsruhe\n")

        print("-h \t Print this help page")
        print("-e \t Reset and close Keithley connection (exit)")
        print("-res \t Reset Keithley connection")
        print("-v x y=100 \t Enable output voltage, set to value -x and compliance limit to value y in uA (default: 100)")
        print("-rv \t Read voltage")
        print("-rc \t Read current")

def isInt(string):

    try:
        float(string)
        return True
    except ValueError:
        return False

def readMode(k):

    try:
        while True:
            current = k.readCurrent()
            print("   Current: " + current + " A")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\nReadMode closed!\n")


# main loop
if __name__=='__main__':

    # Instanciate Keithly
    k = keithley()

    # Check command line arguments
    if (len(sys.argv) > 1):

        # Help page
        if (sys.argv[1] == "-h"):
            k.help()
            sys.exit()

        # Set voltage and compliance
        elif (sys.argv[1] == "-v"):
            k.init()
            if ( (len(sys.argv)>3)):
                if isInt(sys.argv[3]):
                    k.setCompliance(float(sys.argv[3]))
            k.setVoltage(float(sys.argv[2]))

        # Set compliance limit
        elif (sys.argv[1] == "-c"):
            k.setCompliance(float(sys.argv[2]))

        # Read voltage and current
        elif (sys.argv[1] == "-rc"):
            print(k.readCurrent())

        elif (sys.argv[1] == "-rv"):
            print(k.readVoltage())

        # Reset
        elif (sys.argv[1] == "-res"):
            k.reset()
            sys.exit("Resetted Keithley device.")

        # Exit
        elif (sys.argv[1] == "-e"):
            k.close()
            sys.exit("Resetted and closed Keithley connection. Goodbye.")

        # Exception
        else:
            sys.exit("Invalid command line parameter! Use -h for help")


    # Interactive loop
    else:

        # Set custom settings
        k.init()

        print("\nKeithley 2410 Interactive Control Program")
        print("(c) 2015, IEKP Karlsruhe\n")

        while(True):

            command = input("Available commands: \nset voltage (int), set (c)ompliance, (r)ead Current, read Voltage (rv), enter ReadMode (rm), (res)et Keithley, (e)xit Program\n")

            if(isInt(command)):
                voltage = float(command)
                k.setVoltage(voltage)
                print("\n   Output voltage set to " + command + " V\n")

            elif (command == "c"):
                compl = raw_input('Enter compliance limit (in uA): ')
                k.setCompliance(compl)
                print("\n   Compliance limit set to " + compl + " uA\n")

            elif (command == "res"):
                k.reset()
                print("\n   Resetted Keithley device\n")

            elif (command == "r"):
                current = k.readCurrent()
                print("\n   Current: " + current + " A\n")

            elif (command == "rv"):
                voltage = k.readVoltage()
                print("\n   Voltage: " + voltage + " V\n")

            elif (command == "e"):
                k.close()
                sys.exit("\nConnection closed. Goodbye.\n")

            elif (command == "rm"):
                print("\nEntering ReadMode (press Ctrl+C to exit)\n")
                readMode(k)

            else:
                print("\nCommand not found!\n")
