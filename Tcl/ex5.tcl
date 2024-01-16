#!/usr/bin/tclsh
set flag_print 0
set next 0
set output_format "%-25s%-25s"
set fp [open "../input/inputfile.txt"]
while {[gets $fp line] >= 0} {
    if {[string match "=*func_worstLT*=" $line]} {
        set flag_print 1
        # puts "Match_print"
    } elseif {$flag_print == 1} {
        if {[string match "*Clock*Skew*" $line]} {
            set clock_index [string first "Clock" $line]
            set skew_index [string first "Skew" $line]
            puts [format $output_format "Clock" "Skew"]
            set flag_print 0
            set next "---"
        }
    } elseif {$next == "---" && [regexp {^-*$} $line]} {
        set next "print_table"
    } elseif {$next == "print_table"} {
        if {[regexp {^-*$} $line]} {
            set next 0
        } else {
            # print table
            set clock_val [string range $line $clock_index [string first " " $line $clock_index]]
            set skew_val [string range $line $skew_index [string first " " $line $skew_index]]
            puts [format $output_format $clock_val $skew_val]
        }
    }
}
close $fp