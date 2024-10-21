import matplotlib.pyplot as plt



def plot_visualisieren(c_ox_sat, y_combined, t_combined, cum_feeding):

	
    print("Shape of t_combined:", t_combined.shape)
    print("Shape of y_combined:", y_combined.shape)
    y_combined=y_combined.T
    #t_combined = t_combined[0, :]
    #cum_feeding = cum_feeding[:len(t_combined)]
    
    # Grundeinstellungen ändern
    plt.rcParams['axes.labelsize'] = 18
    plt.rcParams['axes.titlesize'] = 24
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['legend.fontsize'] = 14
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['lines.markersize'] = 6
    
	#color Palette
    col1 = [102/255, 194/255, 165/255]
    col2 = [252/255, 141/255, 98/255]
    col3 = [141/255, 160/255, 203/255]
    col4 = [231/255, 138/255, 195/255]
    col5 = [166/255, 216/255, 84/255]
    col6 = [255/255, 217/255, 47/255]
    col7 = [229/255, 196/255, 148/255]
    col8 = [179/255, 179/255, 179/255]
	
    col_HTW = [249/255, 155/255, 25/255]
    col_x1 = [187/255, 161/255, 53/255]
    col_x2 = [163/255, 106/255, 105/255]
    col_x3 = [111/255, 146/255, 124/255]
    
    
	# Plotten der Grafik
    plt.figure(figsize=(14, 6))
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)

    # Subplot 1
    plt.subplot(1, 2, 1)
    plt.plot(t_combined, y_combined[0, :], label="c_{x}", color=col1)
    plt.plot(t_combined, y_combined[1, :], label="c_{S1}", color=col2)
    #plt.plot(t_combined, y_combined[2, :], label="c_{S2}", color=col3)
    plt.plot(t_combined, y_combined[3, :], label="c_{P}", color=col4)
    plt.plot(t_combined, y_combined[4, :] / c_ox_sat * 100, label="c_{O2}", color=col5)
    plt.plot(t_combined, cum_feeding, label="Sum Feed S1", color=col6)
    plt.title("Fermentationsverlauf")
    plt.xlabel("t in h")
    plt.ylabel("c_{s}, c_{x}, c_{P} in g/L")
    plt.grid(True)
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=4, frameon=False)
    plt.tight_layout()
    
    
	# Subplot 2
    plt.subplot(1, 2, 2)
    plt.plot(t_combined, y_combined[2, :], label="c_{S2}", color=col3)
    plt.title("Fermentationsverlauf c_{S2}")
    plt.xlabel("t in h")
    plt.ylabel("c_{s} in g/L")
    plt.grid(True)
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=4, frameon=False)
    plt.tight_layout()
	
    plt.show()