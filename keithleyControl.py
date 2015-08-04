#!/usr/bin/python

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
        self.port = Serial('/dev/ttyS0', baudrate=57600, bytesize=8, parity=PARITY_ODD, xonxoff=True)

    def init(self):
        #
        # Custom settings
        #

        # Reset Keithley
        self.port.write("*RST\r\n");
        # Disable hardware beeper
        self.port.write(":SYST:BEEP:STAT OFF\r\n");
        # Set voltage source to constant voltage output
        self.port.write(":SOUR:VOLT:MODE FIX\r\n");
        # Set output voltage to zero
        self.port.write(":SOUR:VOLT:IMM:AMPL 0\r\n");
        # Set hardware compliance limit
        self.port.write(":CURR:PROT:LEV 100E-6\r\n");
        # Voltage output on rear panel plugs
        self.port.write(":ROUT:TERM REAR\r\n");

    def setVoltage(self,voltage=0):

        # Set bias voltage

        if not isInt(voltage):
            print "Wrong input"
        else:
            self.port.write(":SOUR:VOLT:IMM:AMPL %s\r\n" %(-abs(voltage)) )
            self.port.write(":OUTP:STAT 1\r\n")

    def readCurrent(self):

        self.port.write(":READ?\r\n")
        line = self.port.readline()
        splited = line.split(",")

        return splited[1]

    def readVoltage(self):

        self.port.write(":READ?\r\n")
        line = self.port.readline()
        splited = line.split(",")

        return splited[0][1:]

    def reset(self):

        # Set output: off
        # Clear error messages
        # Load Presettings
        self.port.write(":OUTP:STAT 0\r\n")
        self.port.write("*CLS\r\n")
        self.port.write(":SYST:PRES\r\n")
        self.init()

    def close(self):

        # Set output: off
        # Reset Keithley
        # Clear error messages
        # Load Presettings
        # Set "LOCAL" mode
        # Close connection

        self.port.write(":OUTP:STAT 0\r\n")
        self.port.write("*RST\r\n")
        self.port.write("*CLS\r\n")
        self.port.write(":SYST:PRES\r\n")
        self.port.write(":SYST:KEY 23\r\n")
        self.port.close()

    def help(self):

        print "-h \t This page"
        print "-e \t Close and reset Keithley connection"
        print "-s xx \t Set voltage"
        print "-rv \t Read voltage"
        print "-rc \t Read current"

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
            print current
            time.sleep(3)
    except KeyboardInterrupt:
        print "\n\nReadMode closed!\n"


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

        # Set voltage
        elif (sys.argv[1] == "-s"):
            k.init()
            k.setVoltage(float(sys.argv[2]))

        # Read voltage and current
        elif (sys.argv[1] == "-rc"):
            print k.readCurrent()

        elif (sys.argv[1] == "-rv"):
            print k.readVoltage()

        # Reset
        elif (sys.argv[1] == "-r"):
            k.close()
            sys.exit("Resetted Keithley device")

        # Exit
        elif (sys.argv[1] == "-e"):
            k.close()
            sys.exit("Resetted and closed Keithley connection")

        # Exception
        else:
            sys.exit("Parameter not found! See -h")


    # Interactive loop
    else:

        # Set custom settings
        k.init()

        while(True):

            command = raw_input("Set voltage (int), (r)ead Current, read Voltage (rv), (res)et Keithley, start ReadMode (rm), (e)xit\n")

            if(isInt(command)):
                voltage = float(command)
                k.setVoltage(voltage)

            elif (command == "res"):
                print "\nReseted\n"
                k.reset()

            elif (command == "r"):
                current = k.readCurrent()
                print "\n" + current + " A\n"

            elif (command == "rv"):
                voltage = k.readVoltage()
                print "\n" + voltage + " V\n"

            elif (command == "e"):
                k.close()
                sys.exit("\nBye\n")

            elif (command == "rm"):
                print "\nEntering ReadMode\n"
                readMode(k)

            else:
                print "\nCommand not found!\n"
