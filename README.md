# encorr
Equilibrium and nonequilibrium correlation functions for vibrational spectroscopy

encorr is meant to be used in combination with i-pi (https://github.com/i-pi/i-pi) or with i-pi-eq_neq_spectra tool from https://github.com/tbegusic/i-pi. Dipole moment vectors and/or 
polarizability tensors should be printed out along a trajectory propagated using one of those tools. Then, appropriate correlation functions can be evaluated.
Check out relevant documentation about i-pi-eq_neq_spectra, available at https://github.com/tbegusic/i-pi, before using encorr.

## Installation
To start using the code, download it using
```
git clone git@github.com:tbegusic/encorr.git
```
If you want to add it to your path, run
```
source env.sh
```
or add that line to your .bashrc if you want to have it always available.

Code was tested only on CentOS Linux 7 with python3 (version 3.8.5).

## Usage
There are three applications of encorr: equilibrium correlation functions, nonequilibrium response, and two-time equilibrium-nonequilibrium response.

**Equilibrium time correlation functions for IR absorption and anisotropic Raman spectra**

To compute equilibrium time correlation function related to IR absorption spectroscopy,
$$C(t) = \langle \vec{\mu}(0) \cdot \vec{\mu}(t) \rangle,$$
three files are needed: 
1. input.xml: Input for i-pi. If the file name is not exactly 'input.xml', it should be passed as option to encorr as --input_ipi='different_input_name'.
2. input_spec.xml: Input for encorr. If the file name is not exactly 'input_spec.xml', it should be passed as option to encorr as --input_spec='different_input_name'.
3. simulation_name.dip_X: File containing dipole moments along a trajectory, 3 numbers (x, y, z components) per line, as produced by i-pi. 
X denotes the number of bead.  encorr will automatically average over all beads, whose number is obtained from i-pi input.

For Raman spectra, encorr assumes a file called simulation_name.pol_X is available, with 9 number (xx, xy, xz, ..., zz components of the polarizability tensor) per line.
It evaluates the anisotropic correlation function:
$$C(t) = \langle \text{Tr}[\boldsymbol{\beta}(0) \cdot \boldsymbol{\beta}(t)]\rangle,$$
where $\boldsymbol{\beta} = \boldsymbol{\Pi} - \frac{1}{3} \text{Tr}(\boldsymbol{\Pi})\mathbf{1}$.

In either case, the command to run encorr is
```
encorr.py --calc=eq_corr --input_ipi='ipi_input_name' --input_spec='spec_input_name'
```
or, if ipi_input_name is 'input.xml' and spec_input_name is 'input_spec.xml', all settings agree with defaults, so it is sufficient to run
```
encorr.py
```
Annotated example of input_spec.xml file can be found in tests/eq_corr.

**Nonequilibrium response to external field perturbation**

With option
```
encorr.py --calc=neq_corr
```
we can compute quantity
$$C(t) = \frac{1}{\varepsilon}\langle \mu_{+}(t) - \mu_{-}(t) \rangle,$$
where $\mu_{\pm}(t)$ is the z-component of $\vec{\mu}$ along a trajectory that was "kicked" at time zero by a force equal to $\pm (\varepsilon / 2) \mu^{\prime}(0)$, 
which corresponds to an interaction with an instantaneous (delta pulse) electric field. $C(t)$ computed this way can be related to IR spectroscopy and the 
equilibrium dipole-dipole correlation function for sufficiently small $\varepsilon$.

Values of $\mu_{\pm}(t)$ are obtained from a file 'simulation_name.dip_X' produced by i-pi-eq-neq-spectra,
which uses both input.xml (i-pi input) and input_spec.xml (encorr input) to obtain relevant parameters.
An example with annotated input files can be found in tests/neq_corr.

**Two-time equilibrium-nonequilibrium response**

Option
```
encorr.py --calc=neq_2d
```
evaluates
$$C(t) = \frac{\beta}{\varepsilon}\langle [a_{+}(t_2) - a_{-}(t_2)] b(-t_1) \rangle,$$
where $a$ and $b$ are components of dipole moment vector or polarizability tensor, depending on the input.
This correlation is related to the two-time response function of two-dimensional infrared-Raman spectroscopy.

encorr assumes that an appropriate simulation with i-pi-eq_neq_spectra was performed, and that outputs simulation_name.dip_X and simulation_name.pol_X are available.
See tests/neq_2d for an annotated input file.

