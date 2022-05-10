#!/bin/bash

test_check(){
if [ $1 -eq 0 ]
then
    echo "Passed"
else
    echo "Failed"
fi
}

cd eq_corr
rm dip_eq_corr.dat &> /dev/null
../../encorr.py --calc=eq
diff dip_eq_corr.dat bck_dip_eq_corr.dat  > /dev/null 2>&1
error=$?
test_check $error
cd - &> /dev/null 

cd neq_corr
rm dip_neq_corr.dat &> /dev/null
../../encorr.py --calc=neq
diff dip_neq_corr.dat bck_dip_neq_corr.dat  > /dev/null 2>&1
error=$?
test_check $error
cd - &> /dev/null 

cd neq_2d
rm dip_pol_neq_2d.dat &> /dev/null
../../encorr.py --calc=neq_2d
diff dip_pol_neq_2d.dat bck_dip_pol_neq_2d.dat  > /dev/null 2>&1
error=$?
test_check $error
cd - &> /dev/null 
