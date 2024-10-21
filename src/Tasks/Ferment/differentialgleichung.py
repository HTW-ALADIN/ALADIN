


import numpy as np    



def ODE_Bioreactor_Monod(t, p, consts) : 
	
   
    #Entnehmen der Kostanten aus consts

    c_ox_sat = consts[0]       #Sauerstofflöslichkeit in der Fermentation
    kla = consts[1]            #kla Wert in 1/h Info eine OTR von 100 mmol/(L*h) entspricht bei DO=0% ~ einem kla von 400 1/h
    RQ = consts[2]             #Respiratory Coefficient
    Begasungsrate = consts[3]  #Begasungsrate in NL(Luft)/(L(Kulturbrühe)*min) quasi vvm
    c_O2_Luft = consts[4]      #Sauerstoffgehalt Luft in mol/L
    c_CO2_Luft = consts[5]     #CO2 Gehalt der Luft in mol/L
    ks_ox = consts[6]          #Halbsaettigungskonstante Sauerstoff in g/L
    Yxox = consts[7]           #Ausbeutekoeffizient g Biomasse je g Sauerstoff nach HArvard Bionumbers für E.coli
    P=consts[8]                #Produktbildung an =1 oder aus =0
    ap = consts[9]             #Luedking Piret Parameter für wachsumassoziierte Produktbildung
    bp = consts[10]            #Luedking Piret Parameter für nicht wachsumassoziierte Produktbildung
    kp_max = consts[11]        #maximale spezifische Produktbildungsrate in g(P)/(g(x)*L*h) nicht wachstumsassoziierte Produktbildung
    km_s1p = consts[12]        #Km Wert in Analogie zur Michaelis Menten-Gleichung für die Bildung von P aus S - nicht wachstumsassoziiert
    Ypx_mu = consts[13]        #Ausbeutekoeffizient Produktbildung direkt wachstumsassoziiert aus Substrat
    mumax =consts[14]          #maximale Wachstumsrate  in 1/h
    ks_s1x=consts[15]          #Halbsaettigungskonstante Substrat in g/L für Berechnung von Wachstumsrat µ
    Yxs1=consts[16]            #Ausbeutekoeff fuer Zellmasse in g/g
    ks_s2x=consts[17]          #Halbsaettigungskonstante Ks für Substrat S2 in g/L für Berechnung von Wachstumsrat µ
    Yxs2=consts[18]            #Ausbeutekoeff fuer Zellmasse auf Substrat 2 1 in g/g
    feed_s1=consts[19]         #Feedrate Substrat 1 in g/L*h


    #Zuweisungen der Eingangswerte / = Konzentrationen die das Model berechnet
   
    cx = p[0]                   #Konzentration Biotrockenmasse in g/L
    cs1 = p[1]                  #Substratkonzentration 1 in g/L
    cs2 = p[2]                  #Substratkonzentration 2 in g/L
    cp = p[3]                   #Produktkonzentration in g/L
    c_ox = p[4]                 #Gelöstsaurestoffkonznetration in g/L
    c_O2_Out = p[5]             #Abluftkonzentration O2
    c_CO2_Out = p[6]            #Abluftkonzentration CO2
    
    #Nebenrechnungen
    
    Vm_norm=22.41950113		#molares Volumen bei Normbedingungen
    Luft_In=Begasungsrate*60 	#ZuLuftstrom Luft in NL/(L_Brühe*h)
    Luft_Out=Luft_In  		#Molenstrom Abluft in mol/(L*h) ; evtl. mal erweitern wenn Luft_Out <> Luft_In
    #Sauerstoff als limitierendes Substrat
    OTR=kla*(c_ox_sat - c_ox) 	#in g/(L*h)
    
    
    #Modellgleichungen
    #spez. Wachstumsrate
    mu_s = mumax*cs1/(ks_s1x+cs1)*cs2/(ks_s2x+cs2)*c_ox/(ks_ox+c_ox); # Monod Kinetik fuer spezifische Wachstumsrate
    #k_ox = 0.01*cs1/(ks_ox+cs1); %nicht wachstumsabhängige Sauerstoffverbrauchsrate, beschrieben als MichaMenten Kinetik %%%%CHANGE!!
    #Produktbildungsrate
    kp = kp_max*cs1/(km_s1p+cs1); #Michaelis Menten Kinetik für nicht wachstumssassoziierte Produktbildung
    
    #OUR=cx*(mu_s/Yxox-k_ox);
    OUR=cx*(mu_s/Yxox);
    #Begasung / Sauerstoff
    CER=OUR/32*RQ; #Umrechung von g/L in mol/L
    
    
        
    value_0 = float(mu_s * cx)
    
    #Substratverbrauchsgeschwindigkeit Substrat 1 durch Biomassebildung und Produktbildung
    value_1= float(cx*(-mu_s/Yxs1)-P*((mu_s*cx*Ypx_mu)*ap+(cx*kp)*bp)+feed_s1)
    
    #Substratverbrauchsgeschwindigkeit Substrat 2 durch Biomassebildung NICHT Genutzt zur Produktbildung Produktbildung
    value_2= float(cx*(-(mu_s/Yxs2)))

    #Produktbildung nach Luedeking Piret;
    value_3= float(P*((mu_s*cx*Ypx_mu)*ap+(cx*kp)*bp))

    #Berechnung Gelöstsauerstoffkonzentration (OTR-OUR) mit Nebenbedingung
    #darf nicht NUll sein
    value_4= float(kla*(c_ox_sat-c_ox)-cx*(mu_s/Yxox))

    #Berechnung O2-gehalt in Vol% Abluf IN Analogie zu einem CSTR F(C_in-Cout)-Reaktion
    value_5= float(Luft_In*c_O2_Luft-Luft_Out*c_O2_Out-OUR/32*Vm_norm)

    #Berechnung CO2-gehalt in Vol% Abluf IN Analogie zu einem CSTR F(C_in-Cout)-Reaktion
    value_6= float(Luft_In*c_CO2_Luft-Luft_Out*c_CO2_Out+CER*Vm_norm)
   
    retval = np.array([value_0,value_1,value_2,value_3,value_4,value_5,value_6])
    
    
    return retval
  


