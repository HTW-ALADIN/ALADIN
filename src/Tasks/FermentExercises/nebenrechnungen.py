import math
import numpy as np
from array import array



from interne_daten.konstantenDictionary import *


Durchmesser_Ruehrer_durch_Durchmesser_Tank = 0.33					                                #Modell F19
nutzbares_Volumen = 0.7				                                                                #Modell F21
Hoehe_des_Tanks_durch_Durchmesser_Tank = 3						                                    #Modell F20
Anzahl_Rushton_Impeller = 3 		                                                                #Modell F22 
Volumen_Kulturbruehe = 10 / 1000 	                                                                #Modell F18
Durchmesser_Ruehrer = 0.0602                                                                        #!Modell F28
Nettovolumen = Volumen_Kulturbruehe / nutzbares_Volumen	                                            #Modell F27

Durchmesser_Tank = ((Nettovolumen*4) / (Hoehe_des_Tanks_durch_Durchmesser_Tank*math.pi))**(1/3)		#Modell F29			

Hoehe_des_Tanks = Hoehe_des_Tanks_durch_Durchmesser_Tank * Durchmesser_Tank					        #Modell F30
Vcheck = (math.pi/4) * Durchmesser_Tank**2 * Hoehe_des_Tanks 			                            #Modell F32








def parameter(Sauerstoffoeslichkeit_array,kla_werte,data,phasen_anzahl,modell):
    parameter_array = [array('d', [0] * 3) for _ in range(4)]
    
    for j in range(phasen_anzahl):
        parameter_array[j][0]=Sauerstoffoeslichkeit_array[j][5] #!Sauersto. in g/l

    for j in range(phasen_anzahl):
        parameter_array[j][1]=kla_werte[j][17]
    
    for j in range(phasen_anzahl):
        parameter_array[j][2]=data.get(modell, {}).get("umax") #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];7;FALSCH)
    
    return parameter_array




def Berechnung_der_Sauerstoffloeslichkeit(phasen_anzahl,temperatur,druck):


    Sauerstoffoeslichkeit_array = [array('d', [0] * 6) for _ in range(int(phasen_anzahl))]



    ###############################################                             Phase1
    # Attribute für Phase 1
    T_in_K_1          = 273.15 + temperatur                                     # Modell!B11
    p_in_bara_1       = 1.013 + druck[0]  #Modell H8 = 1                                      
    p_o2_in_bara_1    = 0.20946 * p_in_bara_1                            
    kH_o2_bei_T_1     = Henry_Kosntanten["Solut_KH2"]["O2"] * math.exp(-Temperaturkoeffizient["O2"]*((1/T_in_K_1) - (1/Henry_Kosntanten["Solut_T"]["O2"]))) 
    L_o2_in_mmol_l_1  = (p_o2_in_bara_1 / kH_o2_bei_T_1 )*1000              
    L_o2_in_g_l_1     = (L_o2_in_mmol_l_1*32) /1000                       

    for i in range(phasen_anzahl):
        if i == 0:
            Sauerstoffoeslichkeit_array[0]  =  [T_in_K_1,p_in_bara_1,p_o2_in_bara_1,kH_o2_bei_T_1,L_o2_in_mmol_l_1,L_o2_in_g_l_1]
        else :
            Sauerstoffoeslichkeit_array[i][0]=Sauerstoffoeslichkeit_array[i-1][0]   
            Sauerstoffoeslichkeit_array[i][1]= 1.013 + float(druck[i])  #Modell!I8  #Modell j8  #modell k8
            Sauerstoffoeslichkeit_array[i][2]= 0.20946 * Sauerstoffoeslichkeit_array[i][1]
            Sauerstoffoeslichkeit_array[i][3]=Henry_Kosntanten["Solut_KH2"]["O2"] * math.exp(-Temperaturkoeffizient["O2"]*((1/Sauerstoffoeslichkeit_array[i][0]) - (1/Henry_Kosntanten["Solut_T"]["O2"]))) 
            Sauerstoffoeslichkeit_array[i][4]=(Sauerstoffoeslichkeit_array[i][2]/Sauerstoffoeslichkeit_array[i][3])*1000
            Sauerstoffoeslichkeit_array[i][5]=(Sauerstoffoeslichkeit_array[i][4]*32)/1000                    

        # Dezimalstellen nach komma grenzen, maximal 9 Stellen nach komma
    for i in range(len(Sauerstoffoeslichkeit_array)):
        for j in range(len(Sauerstoffoeslichkeit_array[i])):
            try:
                Sauerstoffoeslichkeit_array[i][j] = round(float(Sauerstoffoeslichkeit_array[i][j]), 9)
            except ValueError:
                pass

    return Sauerstoffoeslichkeit_array


def Berechnung_des_kla_Wertes(Sauerstoffoeslichkeit_array,data,drehzahl,modell,zuluft,phasen_anzahl):

    kla_werte = [array('d', [0] * 19) for _ in range(phasen_anzahl)]
    i=0

    drehzahl_1                              = float(drehzahl[i]) #Modell H9
    Drehzahl_pro_sek                        = 1200 / 60
    Dichte                                  = data.get(modell, {}).get("Dichte Bruehe")    #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];21;FALSCH)                    
    dyn_Viskosität1                         = data.get(modell, {}).get("dyn. Viscosity")        #SVERWEIS(Modell!$B$3;Tabelle1[#Alle];22;FALSCH)                    
    dyn_Viskositaet2                        = dyn_Viskosität1/ 1000        #(kg*m)/s
    Ruehrerdurchmesser                      = Durchmesser_Ruehrer  #0.0602 Modell F28
    Reynoldszahl_Re                         = (Dichte * Drehzahl_pro_sek * (Ruehrerdurchmesser**2)) / dyn_Viskositaet2
    Newton_Zahl_Ne                          = 7
    Leistungseintrag_nicht_begast_P_1       = (Newton_Zahl_Ne * Anzahl_Rushton_Impeller * Dichte * (Drehzahl_pro_sek**3) * (Ruehrerdurchmesser**5))  #Modell F22=3
    Leistungseintrag_nicht_begast_P_2       = Leistungseintrag_nicht_begast_P_1 / Volumen_Kulturbruehe   #modell F18 = 0.01
    Leistungseintrag_nicht_begast_P_3       = Leistungseintrag_nicht_begast_P_2 / 1000                   #kW/m3
    
    #Feld 11 später
    Air_Flow_1                              = 0.2                                           #vvm
    Air_Flow_2                              = Air_Flow_1 * Volumen_Kulturbruehe / 60    #Modell F18=0.01  
    cross_scetion                           = (math.pi / 4) * (Durchmesser_Tank**2) #modell F29 = 0.1823                  
    
    #Feld 15 zuert berechnet dann 11
    superficial_velocity                    = Air_Flow_2 / cross_scetion                       #m/s
    Leistungseintrag_Begast_Pg              = Leistungseintrag_nicht_begast_P_1 / math.sqrt(1+float(Konstanten_fuer_P_begast["3"])*superficial_velocity/math.sqrt(9.81*Ruehrerdurchmesser))                  #W =C48/WURZEL(1+SVERWEIS(Modell!$F$22;Daten!$I$43:$J$45;2;FALSCH)*C55/WURZEL(9,81*C44))
                                            #Leistungseintrag_nicht_begast_P_1 / math.sqrt(1+Konstanten_fuer_P_begast.get(Anzahl_Rushton_Impeller)*superficial_velocity/math.sqrt(9.81*Ruehrerdurchmesser))
    kla_pro_sek                             = 0.026 * ( ( Leistungseintrag_Begast_Pg / Volumen_Kulturbruehe) ** (0.4) ) * (superficial_velocity ** (0.5) )  #modell F18 = 0.01
    kla_pro_std                             = kla_pro_sek * 3600                          #1/h
    OTR_max                                 = kla_pro_std * Sauerstoffoeslichkeit_array[i][4]               #mmol/(l*h)


    for i in range(phasen_anzahl):
        if i == 0 :
            kla_werte[0]  = [float(drehzahl_1),float(Drehzahl_pro_sek),float(Dichte),float(dyn_Viskosität1),float(dyn_Viskositaet2),float(Ruehrerdurchmesser),float(Reynoldszahl_Re),float(Newton_Zahl_Ne),float(Leistungseintrag_nicht_begast_P_1),float(Leistungseintrag_nicht_begast_P_2),float(Leistungseintrag_nicht_begast_P_3),float(Leistungseintrag_Begast_Pg),float(Air_Flow_1),float(Air_Flow_2),float(cross_scetion),float(superficial_velocity),float(kla_pro_sek),float(kla_pro_std),float(OTR_max)]
        else    :                                           #alle anderen phasen_anzahl
            
            kla_werte[i][0]=float(drehzahl[i]) #modell I9
            kla_werte[i][1]=float(kla_werte[i][0]/60)
            kla_werte[i][2]=float(kla_werte[i-1][2])
            kla_werte[i][3]=float(kla_werte[i-1][3])
            kla_werte[i][4]=float(kla_werte[i-1][4])
            kla_werte[i][5]=float(kla_werte[i-1][5])
            kla_werte[i][6]=float(( kla_werte[i][2] * kla_werte[i][1] * kla_werte[i][5]**2 ) / kla_werte[i][4])
            kla_werte[i][7]=float(kla_werte[i-1][7])
            kla_werte[i][8]=float(( kla_werte[i][7] * Anzahl_Rushton_Impeller *  kla_werte[i][2] * ( kla_werte[i][1] ** 3 ) * ( float(kla_werte[i][5]) ** 5)) ) #Modell!$F$22 = 3
            kla_werte[i][9]=float(kla_werte[i][8] / Volumen_Kulturbruehe ) #modell F18 = 0.01
            kla_werte[i][10]=float(kla_werte[i][9] / 1000)
            kla_werte[i][12]=float(zuluft[i]) #W/m3 Modell l7 = 0.01
            kla_werte[i][13]=float(kla_werte[i][12] * Volumen_Kulturbruehe / 60) #ModellF18 = 0.01
            kla_werte[i][14]=float(math.pi / 4 * Durchmesser_Tank**2) #modell F29 = 0.1823
            
            #Feld 11 braucht Ergebnis von 15. Deswegen 15 zuerst
            kla_werte[i][15]=float(kla_werte[i][13] / kla_werte[i][14])
            kla_werte[i][11]=float(kla_werte[i][8] / math.sqrt(1 + float(Konstanten_fuer_P_begast["3"])* kla_werte[i][15] / math.sqrt( 9.81 * kla_werte[i][5] ) ) )  #modell F22= 3  #W =C48/WURZEL(1+SVERWEIS(Modell!$F$22;Daten!$I$43:$J$45;2;FALSCH)*C55/WURZEL(9,81*C44))

            Leistungseintrag_Begast_Pg2 = kla_werte[i][11]
            superficial_velocity2=kla_werte[i][15] 
            kla_werte[i][16]=float(0.026 * ((Leistungseintrag_Begast_Pg2  / Volumen_Kulturbruehe ) ** (0.4) ) * (superficial_velocity2 ** (0.5)))    #Modell!$F$18 = 0.01
            kla_werte[i][17]=float(kla_werte[i][16] * 3600 )
            kla_werte[i][18]=float(kla_werte[i][17] * Sauerstoffoeslichkeit_array[i][4]) 
            
            
            
    # Dezimalstellen nach komma grenzen, maximal 9 Stellen nach komma
    for i in range(len(kla_werte)):
        for j in range(len(kla_werte[i])):
            try:
                kla_werte[i][j] = round(float(kla_werte[i][j]), 9)
            except ValueError:
                pass
    
    return kla_werte
    