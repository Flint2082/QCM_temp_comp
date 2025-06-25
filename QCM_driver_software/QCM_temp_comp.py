import sys
print("Python executable:", sys.executable)

import sympy as sp


# mode coefficients for temperature and mass modes
fT_1 = -0.000146172
fT_2 = 6.56675E-07
fT_3 = -1.77929E-09

fM_1 = 1.4117E-05
fM_2 = -1.61812E-07
fM_3 = 6.10868E-10

# mode coefficients for AT-cut quartz crystal 
fAT_1 = 1.16389E-05
fAT_2 = -2.89255E-07
fAT_3 = 2.04472E-09


# starting values for temperature and mass modes
# T_start = 0.0
# fT_start = 3.73871
# fM_start = 9.99952

# T_start = 20.0
# fT_start = 3.736039
# fM_start = 9.999741

# T_start = 22.1
# fT_start = 3.735754
# fM_start = 9.9997585

# T_start = 22.2
# fT_start = 3.735547
# fM_start = 9.9997923

T_start = 23.0  # °C
fT_start = 3.735242
fM_start = 9.99980336 


# for Aluminium being deposited on the QCM
mat_dens = 2700 # kg/m^3
sens_area = 32.0E-6  # m^2
 

# mass sensitivity coefficients 
fT_0 = (fT_start * 2)/28.5 #-131845.6 
fM_0 = (fM_start * 2)/28.5 #-136341.9  



def main():

    # fT = float(input("Enter the temperature mode frequency value in MHz: "))
    # fM = float(input("Enter the mass mode frequency value in MHz: "))
    
    # Measurement values
    # fT = 3.730747
    # fM = 9.9999258
    # T_meas = 73.2
    # T_meas = 22.1
    
    T_meas = 23.0
    M_meas = 0.0 
    fT = 3.734243
    fM = 9.99985381
    
       
    fT_dif = fT - fT_start
    fM_dif = fM - fM_start
    T_dif = T_meas - T_start

    print("fT_dif meas:", fT_dif)
    print("fT meas:", fT)
    print("fM_dif meas:", fM_dif)
    print("fM meas:", fM)
    

    #################################
    
    # layer_thickness = 0  # nm
    
    # M_meas = sens_area * mat_dens * layer_thickness * 1E-3 # g
    
    # T_meas = 34.4  # °C
    
    # T_dif = T_meas - T_start
    
    ### The following code is used to produce synthetic values for testing the compensation algorithm. ###
    # fT_dif = (fT_3 * (T_dif + T_start)**3 + fT_2 * (T_dif + T_start)**2 + fT_1 * (T_dif + T_start)) - (fT_3 * (T_start)**3 + fT_2 * (T_start)**2 + fT_1 * (T_start)) + fT_0 * M_meas
    # fM_dif = (fM_3 * (T_dif + T_start)**3 + fM_2 * (T_dif + T_start)**2 + fM_1 * (T_dif + T_start)) - (fM_3 * (T_start)**3 + fM_2 * (T_start)**2 + fM_1 * (T_start)) + fM_0 * M_meas
       
    # fT = fT_start + fT_dif
    # fM = fM_start + fM_dif
    
    ### The following code is used to calculate the accuracy differences for the AT-cut ###
    fAT_start = 11.996274  # MHz, AT-cut quartz crystal frequency at T_start
    
    fAT_0 = (fAT_start * 2)/28.5 #-131845.6
     
    fAT_dif = (fAT_3 * (T_dif + T_start)**3 + fAT_2 * (T_dif + T_start)**2 + fAT_1 * (T_dif + T_start)) - (fAT_3 * (T_start)**3 + fAT_2 * (T_start)**2 + fAT_1 * (T_start)) + fAT_0 * M_meas
    fAT = fAT_start + fAT_dif
    
    ##############################
    
    dT= sp.symbols('dT')
    
    fT_d = fT_start - fT_3 * T_start**3 - fT_2 * T_start**2 - fT_1 * T_start 
    fM_d = fM_start - fM_3 * T_start**3 - fM_2 * T_start**2 - fM_1 * T_start
          
    T_dif = sp.solve((fM_3*fT_0 - fT_3*fM_0) * (dT + T_start)**3 + (fM_2*fT_0 - fT_2*fM_0) * (dT + T_start)**2 + (fM_1*fT_0 - fT_1*fM_0) * (dT + T_start) + fM_0*(fT_dif-fT_d) - fT_0*(fM_dif - fM_d), dT)
    

    # Output the result
    print("\nThe calculated temperature is:",  T_start+T_dif[0], "°C")  # Assuming the first solution is the desired one
    print("The measured temperature is:", T_meas, "°C")
    print("The temperature error is :", T_meas - (T_start+ T_dif[0]), "°C")
    
    
    M_dif = -(-fM_dif + (fM_3 * (T_dif[0] + T_start)**3 + fM_2 * (T_dif[0] + T_start)**2 + fM_1 * (T_dif[0] + T_start)) - (fM_3 * (T_start)**3 + fM_2 * (T_start)**2 + fM_1 * (T_start)))/ fM_0
    
    print("\nThe uncompensated AT-cut mass difference is:", (fAT_dif / fAT_0) *1000*1000, "nanograms")
    print("The uncompensated AT-cut layer thickness is:", ((fAT_dif / fAT_0)*1000)/(mat_dens * sens_area), "nanometers")
    
    print("\nThe uncompensated SC-cut mass difference is:", (fM_dif / fM_0) *1000*1000, "nanograms")
    print("The uncompensated SC-cut layer thickness is:", ((fM_dif / fM_0)*1000)/(mat_dens * sens_area), "nanometers")
    
    print("\nThe compensated mass difference is:", M_dif * 1000 * 1000, "nanograms")
    print("The compensated layer thickness is:", (M_dif*1000)/(mat_dens * sens_area), "nanometers")
    
    print("\nThe compensation improved the accuracy", abs(((fAT_dif / fAT_0)-M_meas) / (M_dif-M_meas)), "times compared to AT-cut.")
    print("\nThe compensation improved the accuracy", abs(((fM_dif / fM_0)-M_meas) / (M_dif-M_meas)), "times compared to SC-cut.")
    

    

if __name__ == "__main__":
    main()