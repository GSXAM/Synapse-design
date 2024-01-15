#!/usr/bin/tclsh
proc rect {{a 0} {b 1}} {
    return [expr $a * $b]
}

proc fibonacci {{n 2}} {
    set output [list 0 1]
    for {set i 2} {$i < $n} {incr i} {
        lappend output [expr [lindex $output [expr $i - 1]] + [lindex $output [expr $i - 2]]]
        # puts $i
    }
    return $output
}

proc fibo_recursive {{n 1}} {
    switch $n {
        2 {
            return 1
        }
        1 {
            return 0
        }
        default {
            return [expr [fibo_recursive [expr $n-1]] + [fibo_recursive [expr $n-2]]]
        }
    }
}

proc print_fibo_re {{n 1}} {
    set output {}
    for {set i 1} {$i <= $n} {incr i} {
        lappend output [fibo_recursive $i]
    }
    return $output
}

# --------------- Main -------------
puts [fibonacci 8]
