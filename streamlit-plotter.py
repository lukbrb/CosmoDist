import streamlit as st
import csv
import numpy as np
import pandas as pd
import plotly.express as px
from CalculDistances import CalculDistances

st.title("Calculateur de distances Cosmologiques")
st.header("Résultats")

st.sidebar.title("Paramètres :")

z = st.sidebar.number_input("Redshift", value=1)
H_0 = st.sidebar.number_input("Constante de Hubble", value=65)
# st.sidebar.latex("\Omega_m")
w_m = st.sidebar.number_input("Densité de matière", value=0.24)
# st.sidebar.latex("$\Omega_$")
w_r = st.sidebar.number_input("Densité de rayonnement ", value= 4.6 * 1e-5)
# st.sidebar.latex("$\Omega_m$")
w_l = st.sidebar.number_input("Constante cosmologique", value=0.76)
# st.sidebar.latex("$\Omega_m$")
w_k = st.sidebar.number_input("Paramètre de courbure", value=0.)

calculer = st.sidebar.button("Calculer")


# if not calculer:
#     z = 1
#     base = CalculDistances(65, 0.24, 4.6 * 1e-5, 0.76, 0)
#     st.markdown(f"**Distance comobile radiale à *redshift* {z} =** {base.calcul_DCMR(z)} **Mpc**")
#     st.markdown(f"**Temps de voyage de la lumière à *redhsift* {z} =** {base.calcul_TVL(z)} **Gyr**")
#     st.markdown(f"**Distance Angulaire à *redshift* {z} =** {base.calcul_DA(z)} **Mpc**")      
#     st.markdown(f"**Distance de luminosité à *redshift* {z} =** {base.calcul_DL(z)} **Mpc**")

# if calculer:
Univ = CalculDistances(65, 0.24, 4.6 * 1e-5, 0.76, 0)
st.markdown(f"**Distance comobile radiale à *redshift* {z} =** {Univ.calcul_DCMR(z)} **Mpc**")
st.markdown(f"**Temps de voyage de la lumière à *redhsift* {z} =** {Univ.calcul_TVL(z)} **Gyr**")
st.markdown(f"**Distance Angulaire à *redshift* {z} =** {Univ.calcul_DA(z)} **Mpc**")      
st.markdown(f"**Distance de luminosité à *redshift* {z} =** {Univ.calcul_DL(z)} **Mpc**")

with open('donnees/distance_redshift.csv', 'w', newline='') as iter_redshift:
    titres_colonnes = ['z', 'DCMR', 'TVL', 'DA', 'DL']
        
    csv_writer = csv.DictWriter(iter_redshift, fieldnames=titres_colonnes, delimiter=';')
    csv_writer.writeheader()
    for z in np.arange(0, 51, 1):
        DCMR = Univ.calcul_DCMR(z)
        TVL = Univ.calcul_TVL(z)
        DA = Univ.calcul_DA(z)
        DL = Univ.calcul_DL(z)
        csv_writer.writerow({'z': z, 
                            'DCMR': DCMR,
                            'TVL': TVL,
                            'DA': DA,
                            'DL': DL
                            })
df = pd.read_csv("donnees/distance_redshift.csv", delimiter=";")
DCMR = df["DCMR"]; TVL = df["TVL"]; DA = df["DA"]; DL = df["DL"]; redshift = df["z"]

    # col1, col2 = st.beta_columns(2)
    
    # with col1:
st.plotly_chart(px.line(df, x="z", y="DCMR", title="Distance comobile radiale", labels={"z":"z", "DCMR":"DCMR (Mpc)"}), use_container_width=True)
st.plotly_chart(px.line(df, x="z", y="TVL", title="Temps de voyage de la lumière", labels={"z":"z", "TVL":"TVL (Mpc)"}), use_container_width=True)
    # with col2:
st.plotly_chart(px.line(df, x="z", y="DA", title="Distance de diamètre angulaire", labels={"z":"z", "DA":"DA (Mpc)"}), use_container_width=True)
st.plotly_chart(px.line(df, x="z", y="DL", title="Distance de luminosité", labels={"z":"z", "DL":"DL (Mpc)"}), use_container_width=True)