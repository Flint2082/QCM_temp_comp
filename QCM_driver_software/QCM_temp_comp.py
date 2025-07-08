import sys
print("Python executable:", sys.executable)

import sympy as sp


### USER CALIBRATION INPUTS
fT_1 = -0.000146172 
fT_2 = 6.56675E-07
fT_3 = -1.77929E-09

fM_1 = 1.4117E-05
fM_2 = -1.61812E-07
fM_3 = 6.10868E-10


### USER STARTING MEASUREMENT INPUTS
T_start = 23.0  
fT_start = 3.735242
fM_start = 9.99980336 

### USER CONSTANTS
mat_dens = 2700 # kg/m^3  // Aluminum density
sens_area = 32.0E-6  # m^2
 

# mass sensitivity coefficients 
fT_0 = (fT_start * 2)/28.5 
fM_0 = (fM_start * 2)/28.5 


def main():
    while True:
        ### USER MEASUREMENT INPUTS
        try:
            fT = float(input("Enter the measured frequency for the temperature mode (Hz): "))
            fM = float(input("Enter the measured frequency for the mass mode (Hz): "))
        except ValueError:
            print("Exiting the program due to invalid input. Please enter numeric values for frequencies.")
            sys.exit(1)

        
        # Calculate the differences from the starting values 
        fT_dif = fT - fT_start
        fM_dif = fM - fM_start

        # Calculate the 'd' components for the temperature and mass modes
        fT_d = fT_start - fT_3 * T_start**3 - fT_2 * T_start**2 - fT_1 * T_start 
        fM_d = fM_start - fM_3 * T_start**3 - fM_2 * T_start**2 - fM_1 * T_start
        
        dT= sp.symbols('dT')      
        T_dif = sp.solve((fM_3*fT_0 - fT_3*fM_0) * (dT + T_start)**3 + (fM_2*fT_0 - fT_2*fM_0) * (dT + T_start)**2 + (fM_1*fT_0 - fT_1*fM_0) * (dT + T_start) + fM_0*(fT_dif-fT_d) - fT_0*(fM_dif - fM_d), dT)
        M_dif = -(-fM_dif + (fM_3 * (T_dif[0] + T_start)**3 + fM_2 * (T_dif[0] + T_start)**2 + fM_1 * (T_dif[0] + T_start)) - (fM_3 * (T_start)**3 + fM_2 * (T_start)**2 + fM_1 * (T_start)))/ fM_0


        # Output the result
        print("\nThe calculated temperature is:",  T_start+T_dif[0], "°C") 
        print("The uncompensated SC-cut layer thickness is:", ((fM_dif / fM_0)*1000)/(mat_dens * sens_area), "nanometers")
        print("The compensated layer thickness is:", (M_dif*1000)/(mat_dens * sens_area), "nanometers \n\n")
        

if __name__ == "__main__":
    main()