#!/bin/bash

cd eq_corr
rm dip_eq_corr.dat &> /dev/null
../../encorr.py --calc=eq
diff dip_eq_corr.dat bck_dip_eq_corr.dat  > /dev/null 2>&1
error=$?
if [ $error -eq 0 ]
then
    echo "Passed"
else
    echo "Failed"
fi
cd - &> /dev/null 

