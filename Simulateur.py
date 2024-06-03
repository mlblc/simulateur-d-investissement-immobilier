import streamlit as st
import pandas as pd
import locale
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import altair as alt

# Définition de la région comme étant la France
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


# Activer le mode "wide"
st.set_page_config(layout="wide")


st.image("Images/banniere.jpeg", use_column_width="auto")
st.title('Simulateur v6')

col1, col2= st.columns(2, gap="large")

with col1:

    st.subheader('Paramètres du projet')

    col1_1, col1_2= st.columns(2, gap="large")

    with col1_1:
        duree_projet = st.slider('Durée du projet', min_value=1, max_value=20, value=5)
        #st.divider()
        st.markdown("**Partie foncière**")
        prix_aquisition = st.number_input('Prix du bien FAI', step=None, min_value=0, value=100000)
        frais_notaire = 0.08 * prix_aquisition
        st.write(f"frais de notaire: {round(frais_notaire):,} €")
        st.write("\n")
        idv = st.toggle('Accompagnement IDV')
        if idv:
            accompagnement_idv = st.radio('Accompagnement', ['Mentorat', 'Clef en main'])
            if accompagnement_idv == 'Mentorat':
                prix_idv = 3500
                st.write(f"frais d'accompagnement: {prix_idv} €")
            else:
                prix_idv = round(0.075 * (prix_aquisition + frais_notaire))
                st.write(f"frais d'accompagnement: {prix_idv:,} €")
        else:
            prix_idv = 0
        nb_lots = st.slider('Nombre de lots', min_value=1, max_value=10)

        st.divider()
        st.markdown("**Partie travaux**")

        montant_travaux = st.number_input('Montant des travaux', step=5000, value=10000)
        accompagnement_travaux = st.toggle('Accompagnement travaux')
        if accompagnement_travaux:
            accompagnement_travaux = st.radio('Accompagnement', ['Courtage', 'Maitrise d\'oeuvre'])
            if accompagnement_travaux == 'Courtage':
                prix_accompagnement_travaux = 990+250*(nb_lots-1)
                st.write(f"frais d'accompagnement: {prix_accompagnement_travaux:,} €")
            else:
                prix_accompagnement_travaux = max(round(0.075 * montant_travaux),1000)
                st.write(f"frais d'accompagnement: {prix_accompagnement_travaux:,} €")
        else:
            prix_accompagnement_travaux = 0
        st.write("\n")
        # Liste pour stocker les valeurs des st.slider
        liste_duree_travaux = []

        # Boucle pour afficher st.slider nb_lots fois
        for i in range(nb_lots):
            duree_travaux = st.slider(f'Durée des travaux pour le lot n° {i+1}', min_value=0, max_value=18, step=1)
            liste_duree_travaux.append(duree_travaux)
        st.write("\n")
            
        st.divider()


    with col1_2:
        st.markdown("**Partie bancaire**")

        apport = st.number_input('Apport', step=1000, min_value=0, max_value= round(prix_aquisition + frais_notaire + prix_idv + montant_travaux), value = round(0.1*(prix_aquisition + frais_notaire + prix_idv + montant_travaux)))
        montant_emprunte = prix_aquisition + frais_notaire + prix_idv + montant_travaux - apport
        st.write(f"Montant emprunté : {montant_emprunte} €")
        duree_emprunt = st.slider('Durée de l emprunt', min_value=10, max_value=35, step=5, value = 20)
        taux_emprunt = st.slider('Taux d intérets', min_value=0.00, max_value=10.0, step=0.1, value=4.0) /100
        if taux_emprunt == 0:
            mensualite_bancaire = montant_emprunte / (12 * duree_emprunt)
        else:
            mensualite_bancaire = ((montant_emprunte * taux_emprunt)/12)/(1-(1+taux_emprunt/12)**(-12*duree_emprunt))
        
        st.write(f"Mensualité bancaire : {round(mensualite_bancaire):,} €")

        prefinancement = st.toggle('Pré-financement')
        duree_prefinancement = 0
        if prefinancement:
            duree_prefinancement = st.slider('Durée du pré-financement en mois',min_value=1, max_value=24, value=6)
            mensualite_prefinancement = (montant_emprunte*taux_emprunt)/12
            st.write(f"Mensualité pendant la période de pré-financement : {round(mensualite_prefinancement):,} €")
        differe = st.toggle('Différé bancaire')
        duree_differe = 0
        if differe:
            duree_differe = st.slider('Durée du différé en mois',min_value=1, max_value=24, value=6)
            mensualite_differe = (montant_emprunte*taux_emprunt)/12
            mensualite_post_differe = ((montant_emprunte * taux_emprunt)/12)/(1-(1+taux_emprunt/12)**(-(12*duree_emprunt-duree_differe)))
            st.write(f"Mensualité pendant le différé : {round(mensualite_differe):,} €")
            st.write(f"Mensualité après le différé : {round(mensualite_post_differe):,} €")

        st.divider()
        st.markdown("**Partie location**")

        # Liste pour stocker les valeurs des st.number_input
        liste_loyers = []

        # Boucle pour afficher st.number_input nb_lots fois
        for i in range(nb_lots):
            loyer = st.number_input(f'Loyer du lot n° {i+1}', step=50, min_value=100, max_value=5000)
            liste_loyers.append(loyer)
        # Calcul de la somme des loyers mensuels
        total_loyers_mensuels = sum(liste_loyers)
        total_loyers_annuels = 12*total_loyers_mensuels
        if nb_lots>1:
            st.write(f"Loyer mensuel : {total_loyers_mensuels:,} €")
        
        gestion_locative = st.toggle('Gestion locative déléguée')
        if gestion_locative:
            frais_gestion_locative = total_loyers_annuels * 0.06
            st.write(f"Frais de gestion locative : {frais_gestion_locative:,} €")
        else:
            frais_gestion_locative=0

        st.divider()
        st.markdown("**Charges**")

        frais_assurance = round(total_loyers_mensuels/2)
        st.write(f"Frais d'assurance propriétaire non-occupant : {frais_assurance:,} €")
        frais_expert_comptable = 576 + 84*(nb_lots-1)
        st.write(f"Frais d'expertise comptable : {frais_expert_comptable:,} €")
        taxe_fonciere = total_loyers_mensuels
        st.write(f"Taxe foncière : {taxe_fonciere:,} €")



with col2:

    montant_projet_total = prix_aquisition + frais_notaire + prix_idv + montant_travaux + prix_accompagnement_travaux

    rentabilite_projet = 100*(total_loyers_annuels / montant_projet_total)
    total_charges = frais_assurance + frais_expert_comptable + taxe_fonciere + frais_gestion_locative
    total_foncier = prix_aquisition + frais_notaire + prix_idv
    total_travaux = montant_travaux + prix_accompagnement_travaux


    # Création du DataFrame pour le tableau
    table_mensualites = []

    # Boucle pour générer les données du tableau
    capital_du = montant_emprunte
    for mois in range(1, 12 * duree_projet + 1):
        # Si le préfinancement est activé et le mois est inférieur ou égal à la durée du préfinancement
        if prefinancement and mois <= duree_prefinancement:
            mensualite = mensualite_prefinancement
        # Si le différé est activé et le mois est compris entre duree_prefinancement et duree_prefinancement + duree_differe
        elif differe and duree_prefinancement < mois <= duree_prefinancement + duree_differe:
            mensualite = mensualite_differe
        # Si le différé est activé et le mois est supérieur à duree_prefinancement + duree_differe
        elif differe and mois > duree_prefinancement + duree_differe:
            mensualite = mensualite_post_differe
        # Si ni le préfinancement ni le différé ne sont activés ou si le mois n'est pas concerné par le préfinancement ou le différé
        else:
            mensualite = mensualite_bancaire
        loyers_encaisses = 0
        for lot in range(0,nb_lots):
            if mois > liste_duree_travaux[lot]:
                loyers_encaisses = loyers_encaisses + liste_loyers[lot]
        remboursement_interets = (taux_emprunt * capital_du)/12
        remboursement_capital = mensualite - remboursement_interets
        capital_du = capital_du - remboursement_capital
        
        # Ajouter les données à la liste
        table_mensualites.append({
            "Mois": mois,
            "Mensualité": round(mensualite),
            "Capital remboursé": round(remboursement_capital),
            "Intérets remboursés": round(remboursement_interets),
            "capital restant dû": round(capital_du),
            "Loyers encaissés":loyers_encaisses
        })


    # Création du DataFrame à partir de la liste de dictionnaires
    df_mensualites = pd.DataFrame(table_mensualites)


    table_synthese_annuelle = []
    tresorerie = 0
    capitalisation = 0
    for annee in range(1,duree_projet+1):
        # Filtrer les données pour l'année actuelle
        donnees_annee = df_mensualites[(df_mensualites['Mois'] >= (annee - 1) * 12 + 1) & (df_mensualites['Mois'] <= annee * 12)]
        # Calcul de la somme des mensualités bancaires pour l'année actuelle
        somme_mensualites = donnees_annee['Mensualité'].sum()
        # Calcul de la somme des intérets bancaires pour l'année actuelle
        somme_interets = donnees_annee['Intérets remboursés'].sum()
        # Calcul de la somme du capital remboursé pour l'année actuelle
        somme_capital_rembourse = donnees_annee['Capital remboursé'].sum()
        capitalisation = capitalisation + somme_capital_rembourse
        somme_loyers_encaisses = donnees_annee['Loyers encaissés'].sum()
        # Calcul du cashflow pour l'année actuelle
        cashflow = somme_loyers_encaisses - somme_mensualites - total_charges
        tresorerie = tresorerie + cashflow

        # Ajouter les données à la liste
        table_synthese_annuelle.append({
            "Année": annee,
            "Loyers encaissés":somme_loyers_encaisses,
            "Somme des mensualités": somme_mensualites,
            "Somme des intérets": somme_interets,
            "Capital remboursé": somme_capital_rembourse,
            "Capitalisation": capitalisation,
            "Charges annuelles":total_charges,
            "Cashflow": cashflow,
            "Trésorerie": tresorerie
        })
    
    annualite_bancaire = somme_mensualites
    benefice_projet = capitalisation+tresorerie
    df_synthese_annuelle = pd.DataFrame(table_synthese_annuelle)
    endettement = (0.7 * total_loyers_annuels - annualite_bancaire)/12
    with st.expander("Tableaux"):
        tab1, tab2 = st.tabs(["Mensualités de crédit","Détail annuel du projet"])
        with tab1:
            st.dataframe(df_mensualites, use_container_width=True, hide_index=True)
        with tab2:
            st.dataframe(df_synthese_annuelle, use_container_width=True, hide_index=True)
        

    st.subheader('Synthèse')

    col2_1, col2_2= st.columns(2, gap="large")

    with col2_1:
        st.write(f"Projet total : {round(montant_projet_total):,} €")
        st.write(f"Rentabilité du projet : {round(rentabilite_projet, ndigits=1)} %")
        st.write(f"Bénéfice sur {duree_projet} ans : {round(benefice_projet):,} €")
        st.write("\n")

    with col2_2:
        st.write(f"Total des loyers annuels : {total_loyers_annuels:,} €")
        st.write(f"Annualité bancaire : {round(annualite_bancaire):,} €")
        st.write(f"Charges annuelles : {total_charges:,} €")
        st.write("\n")
    st.write(f"Total partie foncière : {round(total_foncier):,} €")
    st.write(f"Total partie travaux : {total_travaux:,} €")
    

    st.write("\n")
    
    
    st.write(f"Epargne nécessaire : {round(apport + annualite_bancaire):,} €")
    st.write(f"Endettement résultant du projet : {round(endettement):,} €")
    st.write("\n")



    # Créer le graphique
    fig1 = go.Figure()

    # Créer un DataFrame artificiel pour "Année 0" avec des valeurs nulles
    zero_year_data = {
        "Année": [0],
        "Trésorerie": [0],
        "Capitalisation": [0]
    }
    zero_year_df = pd.DataFrame(zero_year_data)

    # Concaténer le DataFrame artificiel avec df_synthese_annuelle
    combined_df = pd.concat([zero_year_df, df_synthese_annuelle])

    # Créer le graphique avec les données combinées
    fig1.add_trace(go.Scatter(
        x=combined_df['Année'],
        y=combined_df['Trésorerie'],
        mode='lines',
        stackgroup='one',
        name='Trésorerie'
    ))

    fig1.add_trace(go.Scatter(
        x=combined_df['Année'],
        y=combined_df['Capitalisation'],
        mode='lines',
        stackgroup='one',
        name='Capitalisation'
    ))

    # Mise en forme du graphique
    fig1.update_layout(
        title='Capitalisation et Trésorerie par année',
        xaxis_title='Année',
        yaxis_title='Montant',
        xaxis=dict(range=[0, max(df_synthese_annuelle['Année'])])  # Définir la plage de l'axe x

    )

    tab1, tab2 = st.tabs(["Valeurs séparées","Valeurs groupées"])
    with tab1:
        # Afficher le graphique en lignes
        st.line_chart(combined_df.set_index('Année')[['Trésorerie', 'Capitalisation']])
    with tab2:
        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig1, use_container_width=True)


    # Créer un graphique à barres groupées
    fig = go.Figure()

    # Ajouter les barres pour chaque série
    fig.add_trace(go.Bar(
        x=df_synthese_annuelle['Année'],
        y=df_synthese_annuelle['Loyers encaissés'],
        name='Loyers encaissés',
        marker_color = '#0057ff'
    ))

    fig.add_trace(go.Bar(
        x=df_synthese_annuelle['Année'],
        y=df_synthese_annuelle['Somme des mensualités'],
        name='Somme des mensualités',
        marker_color = '#ff4200'
    ))

    fig.add_trace(go.Bar(
        x=df_synthese_annuelle['Année'],
        y=df_synthese_annuelle['Charges annuelles'],
        name='Charges annuelles',
        marker_color = '#ffd000'
    ))

    fig.add_trace(go.Bar(
        x=df_synthese_annuelle['Année'],
        y=df_synthese_annuelle['Cashflow'],
        name='Cashflow',
        marker_color = '#60AEFF'
    ))

    # Configuration du layout pour grouper les barres par années
    fig.update_layout(
        barmode='group',
        bargroupgap=0.1,  # Ajuster cette valeur pour changer l'espace entre les barres dans les groupes
        xaxis_title='Année',
        yaxis_title='Montant',
        title='Graphique à barres groupées par années'
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)







    # Créer le pie chart
    piechart = go.Figure(data=[go.Pie(labels=['Frais d\'assurance', 'Frais d\'expert-comptable', 'Taxe foncière', 'Frais de gestion locative'], values=[frais_assurance, frais_expert_comptable, taxe_fonciere, frais_gestion_locative], hole=0.6)])

    # Définir le titre du pie chart
    piechart.update_layout(title='Répartition des frais')

    # Afficher le pie chart dans Streamlit
    st.plotly_chart(piechart)
