#!/bin/bash

sleep_until_socket_opens(){
c=0
while ! grep -qs "$1" /proc/net/unix
do
  sleep 0.2
  c=$((c + 1))
  if [[ $c -gt 100 ]]; then
    break 
  fi
done 
}

i-pi-eq_neq_spectra input.xml input_spec.xml &> output &
sleep_until_socket_opens water
sleep_until_socket_opens dipole
for i in `seq 1 1`
do
  /home/tbegusic/Software/mylammps/build/lmp < in.lmp &>output_tmp &
  i-pi-driver -u -h dipole -m water_dip_pol -o 1,4,300,1000,200 &> tmp_out &
done
wait
