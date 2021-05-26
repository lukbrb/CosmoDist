import numpy as np
import scipy.integrate as itg

class CalculDistances:
  def __init__(self, H_0, w_m, w_r, w_l, w_k):
    self.H_0 = H_0
    self.w_m = w_m
    self.w_r = w_r
    self.w_l = w_l
    self.w_k = w_k
    
    # -------- Unités-----------------------
    self.c = 299_792.458 #Vitesse de la lumière en km/s
    self.Gyr = 3600 * 24 * 365 * 1e9 # Un milliard d'années en secondes
    self.pars = 3.0856775 * 1e13 # Valeur d'un parsec en km

  def integrande_DCMR(self, a):
    a_point = np.sqrt(self.w_k + self.w_m/a + self.w_r/a**2 + self.w_l * a**2)
    return 1/(a * a_point)


  def integrande_DTT(self, a):
    a_point = np.sqrt(self.w_k + self.w_m/a + self.w_r/a**2 + self.w_l * a**2)
    return 1/a_point


  def J(self, x):
    x = abs(x)
    if x > 1e-6:
      return np.sin(np.sqrt(x)/np.sqrt(x))
    else:
      return 1 + x/6 + x**2/120 + x**3/5040  #... x^n/(2n + 1)!
  

  def calcul_Z(self, z):
    Z, _ = itg.quad(self.integrande_DCMR, 1/(1 + z), 1) 
    # Le deuxième élément du tuple donne l'erreur de calcul
    return Z


  def calcul_DCMR(self, z):
    Z = self.calcul_Z(z)
    return Z * (self.c/self.H_0)
  

  def calcul_DTT(self, z):
    sol_DTT, _ = itg.quad(self.integrande_DTT, 1/(1 + z), 1)
    # Le deuxième élément du tuple donne l'erreur de calcul
    return sol_DTT * (self.c/self.H_0)


  def calcul_TVL(self, z):
    DTT = self.calcul_DTT(z)
    return (1/self.Gyr)* (DTT * 1e6 * self.pars)/self.c 


  def calcul_DA(self, z):
    Z = self.calcul_Z(z)
    return self.J(self.w_k * Z**2) * self.calcul_DCMR(z)/(1+z)


  def calcul_DL(self, z):
    DA = self.calcul_DA(z)
    return (1 + z)**2 * DA