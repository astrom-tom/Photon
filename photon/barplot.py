######################
#R. THOMAS @ ESO, 2017
######################
## This code convert normal
## X, Y spectrum to 'bar plot'
## spectrum
#############


def create_barplot(X,Y):
    '''
    This function convert the X, Y 
    to another Xd and Yd that allows to plot 'bar spectra'
    Parameter
    ---------
    X       numpy array, wavelength
    Y       numpy array, flux
    '''

    Xd = []
    Yd = []
    dd = (X[1]-X[0])/2
    for i in range(len(X)):
        Xd.append(X[i]-dd)    
        Xd.append(X[i]+dd)
        Yd.append(Y[i])
        Yd.append(Y[i])

    return Xd, Yd
