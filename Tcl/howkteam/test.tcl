#!/usr/bin/tclsh

puts [set now [clock seconds]]
set year [clock format $now]
puts $year