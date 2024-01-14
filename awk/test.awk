awk 'BEGIN {
    array["ep1"]=3;
    array["ep2"]=5;
    print length(array);
    ep = "ep3"
    array[ep] = 0;
    print length(array);
    array[length(array) + 1] = ep;
    print length(array);
    for (comb in array) {
        # split(comb,sep,SUBSEP);
        print comb, array[comb];
    }
}'
