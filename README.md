#Keithley 2410 Control

A simple python class and interactive/commandline script to control the Keithley 2410 Source Meter.

## Command line options

* *-h*:		    Print help page
* *-e*:       	    Reset and close Keithley connection (exit)
* *-res*:     	    Reset Keithley connection
* *-v x y=100*:     Enable output voltage, set to value -x and compliance limit to value y in uA (default: 100uA)
* *-rv*:      	    Read voltage
* *-rc*:      	    Read current
