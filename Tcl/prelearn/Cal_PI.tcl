#!/bin/tclsh
#------ Tinh so PI --------
if {[lindex $argv 0] == "help"} {
   puts "Parameter: n"
   puts "Ex: tclsh Cal_PI.tcl 100"
} else {
   set n [lindex $argv 0]
   set pi 0
   for {set i 0} {$i <= $n} {incr i} {
      set pi [expr $pi + (((-1.0)**$i) / (2*$i + 1))]
   }
   puts [expr ${pi}*4]
}
