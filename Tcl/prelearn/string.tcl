#!/bin/tclsh

# set func "compare"
# set func "first"
set func "last"
# set func "wordend"
# set func "wordstart"
# set func "trim"
# set func "trimleft"
# set func "range"

switch $func {
    compare {
        # ------- String compare ---------
        # Explain:
        # --------- (-1) -- (0) -- (1) --------->
        # ----------- a ----------- z ---------->
        # ----------- string1 -----> string2
        set str1 [lindex $argv 0]
        set str2 [lindex $argv 1]

        puts [set result [string compare $str1 $str2]]
        switch $result {
            0 {
                puts "$str1 = $str2"
            }
            1 {
                puts "$str1 < $str2"
            }
            -1 {
                puts "$str1 > $str2"
            }
            default { puts "Default switch."}
        }
    }
    first {
        # ------- First string1 in string2 --------
        # Retval: index of str1 in str2. If not found: return -1
        set str1 [lindex $argv 0]
        set str2 [lindex $argv 1]

        puts [set result [string first $str1 $str2]]
        if {$result == -1} {
            puts "$str1 is not found in $str2"
        } else {
            puts "$str1 in $str2 at: $result"
        }
    }
    last {
        # ------- Last str2 in str1 -------
        set str1 [lindex $argv 0]
        set str2 [lindex $argv 1]
        puts [string last $str2 $str1]
    }
    wordend {
        set str1 [lindex $argv 0]
        puts [string wordend $str1 100]
    }
    wordstart {
        set str1 [lindex $argv 0]
        set index [lindex $argv 1]
        puts [string wordstart $str1 $index]
    }
    trim {
        # --------- Trim both side --------
        # Trim str2 in str1
        set str1 [lindex $argv 0]
        set str2 [lindex $argv 1]
        puts [string trim $str1 $str2]
    }
    trimleft {
        # ------- Trim left side ---------
        # Trim str2 in str1
        set str1 [lindex $argv 0]
        set str2 [lindex $argv 1]
        puts [string trimleft $str1 $str2]
    }
    range {
        set str [lindex $argv 0]
        set index1 [lindex $argv 1]
        set index2 [lindex $argv 2]
        puts [string range $str $index1 $index2]
    }
    default {
        puts "Default function"
    }
}