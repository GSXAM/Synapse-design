#!/usr/bin/tclsh
set str "CLOCKABCDEFG 712        9438            -1.23        2342"

puts [string index $str 40]
puts [string index $str 0]

puts [set word1 [string first " " $str 0]]
puts [set word2 [string first " " $str 40]]

puts [string range $str 0 $word1]
puts [string range $str 40 $word2]


# set string "HI 123 1.23 789"
# set start_index 7
# set end_index [string first " " $string $start_index]
# puts [string range $string $start_index [expr {$end_index - 1}]]

set line "-----------------------------------"
puts [regexp {^-*$} $line]
puts [string match {^-*$} $line]