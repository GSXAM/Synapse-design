#!/bin/csh
#
#  WHILE_EXAMPLE1.CSH
#  Use the WHILE command to construct a DO loop.
#
#  To make a DO loop, initialize the counter with a SET command.
#
#  Run the loop with a WHILE command, until the counter is equal to one more
#  than your limit.
#
#  Increment the counter with the @ command.
#
#!/bin/csh
set n = 10
while ( $n != 15 )
  echo $n
  @ n = $n + 1
end


