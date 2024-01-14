#!/usr/bin/tclsh

proc tinh_nam {past_year} {
    set this_year [exec date +%Y]
    puts $this_year
    return [expr $this_year - $past_year]
}

puts -nonewline "Nhap nam sinh: "
flush stdout
set nam_sinh [gets stdin]
set tuoi [tinh_nam $nam_sinh]
puts "Tuoi la: $tuoi"
