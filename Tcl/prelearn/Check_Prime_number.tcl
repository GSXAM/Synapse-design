#------ Kiem tra so ngto --------
# Parameter: number
set number [lindex $argv 0]

if {$number <= 1} {
    puts "$number ko phai so ngto"
    return 0
} else {
    for {set i 2} {$i <= [expr int(sqrt($number))]} {incr i} {
        if {$number % $i == 0} {
            puts "$number ko phai so ngto"
            return 0
        }
    }
    puts "$number la so ngto"
}