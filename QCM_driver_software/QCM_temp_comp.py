import sys
print("Python executable:", sys.executable)

import sympy as sp
import time
import numpy as np


### USER CALIBRATION INPUTS
fT_1 = -0.000146172 
fT_2 = 6.56675E-07
fT_3 = -1.77929E-09

fM_1 = 1.4117E-05
fM_2 = -1.61812E-07
fM_3 = 6.10868E-10


### USER STARTING MEASUREMENT INPUTS
T_start = 21.8  
fT_start = 3.735744
fM_start = 9.9997581

### USER CONSTANTS
mat_dens = 2700 # kg/m^3  // Aluminum density
sens_area = 32.0E-6  # m^2
 

# mass sensitivity coefficients 
fT_0 = (fT_start * 2)/28.5 
fM_0 = (fM_start * 2)/28.5 

# Coefficients for the cubic equation a*T_dif^3 + b*T_dif^2 + c*T_dif + d = 0
# with d calculated later
a = (fM_3*fT_0 - fT_3*fM_0)
b = (fM_2*fT_0 - fT_2*fM_0)
c = (fM_1*fT_0 - fT_1*fM_0) 

def main():
    while True:
        ### USER MEASUREMENT INPUTS
        try:
            fT = 3.732312   #float(input("Enter the measured frequency for the temperature mode (MHz): "))
            fM = 9.9999061   #float(input("Enter the measured frequency for the mass mode (MHz): "))
        except ValueError:
            print("Exiting the program due to invalid input. Please enter numeric values for frequencies.")
            sys.exit(1)

        
        # Start timing the calculations
        start_time = time.time()
        
        # Calculate the differences from the starting frequency measurements 
        fT_dif = fT - fT_start
        fM_dif = fM - fM_start

        # Calculate the 'd' components for the temperature and mass modes
        fT_d = fT_start - fT_3 * T_start**3 - fT_2 * T_start**2 - fT_1 * T_start 
        fM_d = fM_start - fM_3 * T_start**3 - fM_2 * T_start**2 - fM_1 * T_start
        
        # d coefficient for the cubic equation a*T_dif^3 + b*T_dif^2 + c*T_dif + d = 0
        d = fM_0*(fT_dif-fT_d) - fT_0*(fM_dif - fM_d)
        
        # calculate the roots of the cubic equation
        roots = np.roots([a, b, c, d])
        T_dif = roots[np.isclose(roots.imag, 0)].real  # Select only the real root(s)
        
        # Calculate the compensated mass change using the found temperature difference
        M_dif = -(-fM_dif + (fM_3 * (T_dif[0])**3 + fM_2 * (T_dif[0])**2 + fM_1 * (T_dif[0])) - (fM_3 * (T_start)**3 + fM_2 * (T_start)**2 + fM_1 * (T_start)))/ fM_0

        # End timing the calculations
        end_time = time.time()
        calculation_time = end_time - start_time

        # Output the result
        print("\nThe calculated temperature is:",  T_dif[0], "°C") 
        print("The uncompensated SC-cut layer thickness is:", ((fM_dif / fM_0)*1000)/(mat_dens * sens_area), "nanometers")
        print("The compensated layer thickness is:", (M_dif*1000)/(mat_dens * sens_area), "nanometers")
        print(f"Calculation time: {calculation_time:.4f} seconds\n\n")
        break
        
if __name__ == "__main__":
    main()