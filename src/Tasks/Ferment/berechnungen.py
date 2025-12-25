import pandas as pd 
import numpy as np 
import os
from scipy.integrate import solve_ivp
from openpyxl import Workbook
from differentialgleichung import ODE_Bioreactor_Monod




from array import array



def berechnung_der_Tabelle1(parameter_werte,modull,data,zuluft,feed,phasen_anzahl):
	#float array deklarieren
	const_array= [array('d', [0] * 20) for _ in range(phasen_anzahl)]

	for i in range(phasen_anzahl):
		const_array[i][0]=parameter_werte[i][0]
		const_array[i][1]=parameter_werte[i][1]
		const_array[i][3]=float(zuluft[i]) #0.2 #Modell H7-k7
		const_array[i][4]=0.2095
		const_array[i][5]=0.0004147
		const_array[i][14]=parameter_werte[i][2]
		const_array[i][19]=float(feed[i]) #0.1 #Modell H10-K10
		if i == 0:  #Phase 1

			const_array[0][2]=data.get(modull, {}).get("RQ") #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];13;FALSCH)
			const_array[0][6]=data.get(modull, {}).get("ks_ox") #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];12;FALSCH)
			const_array[0][7]=data.get(modull, {}).get("Yxox") #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];14;FALSCH)
			const_array[0][8]=data.get(modull, {}).get("Produktbildung") #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];15;FALSCH)
			const_array[0][9]=data.get(modull, {}).get("ap") #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];16;FALSCH)
			const_array[0][10]=data.get(modull, {}).get("bp")  #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];17;FALSCH)
			const_array[0][11]=data.get(modull, {}).get("kp_max")  #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];18;FALSCH)
			const_array[0][12]=data.get(modull, {}).get("km_s1p")	 #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];19;FALSCH)
			const_array[0][13]=data.get(modull, {}).get("Ypx_mu")  #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];20;FALSCH)
			const_array[0][15]=data.get(modull, {}).get("Ks_s1x")  #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];8;FALSCH)
			const_array[0][16]=data.get(modull, {}).get("Yxs1")  #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];10;FALSCH)
			const_array[0][17]=data.get(modull, {}).get("Ks_s2x")  #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];9;FALSCH)
			const_array[0][18]=data.get(modull, {}).get("Yxs2")  #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];11;FALSCH)
		else :	#alle anderen Phasen
			const_array[i][2]=const_array[i-1][2]
			const_array[i][6]=const_array[i-1][6]
			const_array[i][7]=const_array[i-1][7]
			const_array[i][8]=const_array[i-1][8]
			const_array[i][9]=const_array[i-1][9]
			const_array[i][10]=const_array[i-1][10]
			const_array[i][11]=const_array[i-1][11]
			const_array[i][12]=const_array[i-1][12]
			const_array[i][13]=const_array[i-1][13]
			const_array[i][15]=const_array[i-1][15]
			const_array[i][16]=const_array[i-1][16]
			const_array[i][17]=const_array[i-1][17]
			const_array[i][18]=const_array[i-1][18]
		
	
        # Dezimalstellen nach komma grenzen, maximal 9 Stellen nach komma
	for i in range(len(const_array)):
		for j in range(len(const_array[i])):
			try:
				const_array[i][j] = round(float(const_array[i][j]), 9)
			except ValueError:
				pass
	
	return const_array


def berechnung_der_Tabelle2(dauer,phasen_anzahl):
	#float array deklarieren
	t_ranges_array= [array('d', [0] * 2) for _ in range(phasen_anzahl)]
	
	for i in range(phasen_anzahl):
		if i == 0: #Phase 1
			t_ranges_array[i][0]=0
			t_ranges_array[i][1]=dauer[i]
		else:
			t_ranges_array[i][0]=t_ranges_array[i-1][1]
			t_ranges_array[i][1]=t_ranges_array[i-1][1]+dauer[i]
	return t_ranges_array


def berechnung_der_Tabelle3(const_array,startbiomasse,bolus_c,bolus_n,do,phasen_anzahl):
    param_array= [array('d', [0] * 7) for _ in range(phasen_anzahl)]
    
    for i in range(phasen_anzahl):
        if i == 0: #Phase 1
            param_array[i][0]=startbiomasse
            param_array[i][1]=float(bolus_c[i])
            param_array[i][2]=float(bolus_n[i])
            param_array[i][3]=0
            param_array[i][4]=(const_array[i][0]*do)/100
            param_array[i][5]=const_array[i][4]
            param_array[i][6]=const_array[i][5]
        else:
            param_array[i][1]=float(bolus_c[i])
            param_array[i][2]=float(bolus_n[i])
    
    
    return param_array


def berechnung(t_ranges_array,param_array,const_array_array,phasen_anzahl):
	data_rate =10; #Anzahl der Datenpunkte pro Stunde

	t_ranges_array		= np.array(t_ranges_array)
	param_array		= np.array(param_array)
	const_array_array	= np.array(const_array_array)


	t_combined = np.array([])
	y_combined = np.array([])
	cum_feeding = np.array([])
	
	for i in range(phasen_anzahl):
		print(i)
		if(i==0):
			y0=param_array[i,:] #erste Zeile aus Dim. Array als vektor
		else:
		    
		    
			mx_0 = ry[-1, 0]  # Biotrockenmasse in g/L
			cs1_0 = ry[-1, 1] + param_array[i,1]  # Konz. Substrat 1 in g/L
			cs2_0 = ry[-1, 2] + param_array[i,2]  # Konz. Substrat 1 in g/L
			cp_0 = ry[-1, 3]  # Konz. Produkt in g/L
			c_ox_0 = ry[-1, 4]  # Konz. Gelöstsauerstoff in g/L zum Start der Fermentation
			O2_Out = ry[-1, 5]  # Konz. O2 in Abluft
			CO2_Out = ry[-1, 6]  # Konz. CO2 in Abluft
			
			y0	=[mx_0,cs1_0,cs2_0, cp_0,c_ox_0, O2_Out, CO2_Out] #Startparameter in Vektor
		    
		    
		t_start=t_ranges_array[i,0]
		t_end=t_ranges_array[i,1]
		
		if t_start != t_end:
			num1=int(data_rate * (t_end - t_start))
			t_span = np.linspace(t_start, t_end, num=num1)  # Zeitvektor bauen
	     	#Loesen der DGL im Zeitabschnitt 
			consts = const_array_array[i,:]
			#print('computing Phase', i)
	     	
			
			sol = solve_ivp(ODE_Bioreactor_Monod, [t_start, t_end], y0, args=(consts,), t_eval=t_span, atol=1e-9, rtol=1e-9)
			ry = sol.y
			ry = ry.T
			rt = sol.t
			
			#Ergebnisse zum Gesamtvektor hinzufügen
			if (i == 0):
				y_combined = ry
				#y_combined=y_combined.T
				t_combined = rt
				cum_feeding = t_span * consts[19]
				
			else:
				
				#if len(t_span) == len(t_combined):  # Überprüfung der Länge der Zeitvektoren
				y_combined = np.vstack((y_combined, ry))
				#y_combined=y_combined.T
				#print(y_combined)
				t_combined = np.hstack((t_combined,rt))
				cum_feeding = np.hstack((cum_feeding, t_span * consts[19]))
				
				
				#else:
					#print("Warning: Time vectors have different lengths. Skipping this phase.")
	



	#Weiter variablen-Zuweisungen fürs PLotten

	c_ox_sat=const_array_array[0,0]
	cum_feeding=cum_feeding.T

	

	return (c_ox_sat,y_combined,t_combined,cum_feeding)




