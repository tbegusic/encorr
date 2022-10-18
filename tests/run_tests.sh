#!/bin/bash

# Runs three tests and outputs Passed/Failed for each test: ./run_tests.sh
# Cleans tests to delete previous result: ./run_tests.sh clean

test_check(){
if [ $1 -eq 0 ]
then
    echo "Passed"
else
    echo "Failed"
fi
}

compare(){
diff $1 bck_$1 > /dev/null 2>&1
error=$?
test_check $error
}

run_test(){
rm $1/$2 &> /dev/null
if [ "$a" != 'clean' ]; then
  cd $1
  ../../encorr.py --calc=$3
  compare $2
  cd - &> /dev/null
fi
}

a=$1
run_test eq_corr test_dip_eq_corr.dat eq
run_test neq_corr dip_neq_corr.dat neq
run_test neq_2d dip_pol_neq_2d.dat neq_2d

