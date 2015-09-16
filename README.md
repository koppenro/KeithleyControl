#Keithley 2410 Control

A simple interactive python script to control the Keithley 2410 Source Meter

## Command line options

* *-h*:       Print help page
* *-e*:       Reset and close Keithley connection (exit)
* *-r*:       Reset Keithley connection
* *-v x*:     Enable output voltage and set to value -x, compliance limit 100 uA
* *-s x y*:   Enable output voltage, set to value -x and compliance limit to value y
* *-c y*:     Set compliance limit to value y (in uA)
* *-rv*:      Read voltage
* *-rc*:      Read current
