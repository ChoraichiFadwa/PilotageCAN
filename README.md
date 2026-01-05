# SBI Student Challenge - CAN 2025 Edition

## Plateforme Décisionnelle Intelligente pour le Pilotage Opérationnel de la CAN 2025

---

## 📋 CONTEXTE & PROBLÉMATIQUE

### Contexte Réel
Le Maroc accueille la CAN 2025 (21 décembre 2025 - 18 janvier 2026) avec :
- **120+ chantiers d'infrastructures** mobilisant 12 milliards MAD
- **9 stades répartis dans 6 villes** (Rabat, Casablanca, Marrakech, Agadir, Tanger, Fès)
- **8 fan zones** accueillant jusqu'à 50 000 personnes simultanément
- **Période critique** : coïncidant avec vacances de Nouvel An (afflux touristique exceptionnel)

### Problème Métier Identifié

Les organisateurs font face à des **défis opérationnels critiques** révélés dès les premiers jours :

**Incidents Réels Observés :**
- 🌪️ **Fan zone Casablanca (El Hank)** : effondrement complet lors d'intempéries (16 déc.)
- 🎫 **Système billetterie** : bugs massifs FAN ID, files d'attente 20 000+ personnes
- 🏟️ **Gestion affluence** : stades semi-vides vs milliers de supporters bloqués à l'extérieur
- 🚗 **Mobilité** : congestion routes d'accès aux stades


### 🎯 Problématique Centrale

**Comment centraliser et exploiter les données opérationnelles multi-domaines (mobilité, sécurité, fan zones, météo) pour anticiper les incidents critiques et permettre une prise de décision éclairée en temps réel aux organisateurs de la CAN 2025 ?**

---

## 💡 SOLUTION PROPOSÉE

### Vue d'Ensemble
Une **plateforme cloud décisionnelle** qui :
1. Centralise les données de **5 domaines critiques**
2. Transforme les données brutes en **indicateurs actionnables**
3. Détecte les **situations à risque** via scoring intelligent
4. Génère des **alertes proactives** pour aide à la décision
5. Visualise en temps réel via **dashboards interactifs**

### Valeur Ajoutée Métier
- **Anticipation** : détecter les risques 24-48h avant
- **Réactivité** : réduire temps de détection incidents de 60 min → 5 min
- **Coordination** : vue unifiée pour tous les acteurs (sécurité, transport, CAF)
- **Capitalisation** : système réutilisable pour Mondial 2030

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Vue Globale

```
┌─────────────────────────────────────────────────────────┐
│           SOURCES DE DONNÉES (Multi-domaines)            │
├─────────────────────────────────────────────────────────┤
│  🚦 Mobilité  │ 👥 Affluence │ 🌤️ Météo │ 🏟️ Événements │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│               INGESTION & STOCKAGE CLOUD                 │
│  ┌────────────────┐        ┌──────────────────┐        │
│  │ Azure Data     │───────▶│ Azure Data Lake  │        │
│  │ Factory        │        │ Gen2 (Parquet)   │        │
│  └────────────────┘        └──────────────────┘        │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│          TRANSFORMATION & MODÉLISATION                   │
│  ┌────────────────┐        ┌──────────────────┐        │
│  │ Azure Synapse  │───────▶│ Schéma en Étoile │        │
│  │ Analytics      │        │ (OLAP Optimisé)  │        │
│  └────────────────┘        └──────────────────┘        │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│              MODULE INTELLIGENCE (Python)                │
│  ┌──────────────┐  ┌────────────┐  ┌────────────────┐ │
│  │ Calcul Score │  │ Détection  │  │ Prédiction     │ │
│  │ Risque       │  │ Anomalies  │  │ Affluence      │ │
│  └──────────────┘  └────────────┘  └────────────────┘ │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│              VISUALISATION & ALERTES                     │
│           Power BI Service (Cloud)                       │
│  ┌──────────────┐  ┌────────────┐  ┌────────────────┐ │
│  │ Dashboard    │  │ Dashboard  │  │ Dashboard      │ │
│  │ Command      │  │ Mobilité   │  │ Fan Zones &    │ │
│  │ Center       │  │ & Accès    │  │ Sécurité       │ │
│  └──────────────┘  └────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 SOURCES DE DONNÉES (Réalistes)

### 🚦 Domaine 1 : Mobilité & Trafic
**Sources :**
- Données historiques trafic villes hôtes (open data municipalités)
- Temps de trajet simulés (Google Maps Distance Matrix API)
- Données incidents routiers (simulées à partir de patterns réels)
- Localisation stades + fan zones + parkings

**Métriques Clés :**
- Congestion par zone (index 0-100)
- Temps moyen accès stade
- Nombre d'incidents routiers
- Taux d'occupation parkings

---

### 👥 Domaine 2 : Affluence Fan Zones
**Sources :**
- Capacités officielles : 8 fan zones (5K - 50K personnes)
- Données billetterie matchs (nombre de billets vendus par stade)
- Historique affluence événements similaires (Mawazine, matchs Lions Atlas)
- Horaires matchs CAN 2025

**Métriques Clés :**
- Taux de remplissage fan zones (%)
- Affluence prévue vs capacité
- Pics horaires (avant/pendant/après matchs)

---

### 🌤️ Domaine 3 : Météo
**Sources :**
- API météo publique (OpenWeatherMap / Weatherstack)
- Historique intempéries décembre/janvier Maroc
- Alertes météo (vent, pluie, températures)

**Métriques Clés :**
- Conditions météo par ville/jour
- Alertes intempéries (rouge/orange/vert)
- Impact potentiel sur infrastructures temporaires (fan zones)

---

### 🏟️ Domaine 4 : Événements Sportifs
**Sources :**
- Calendrier officiel CAN 2025 (24 équipes, 52 matchs)
- Localisation matchs par stade
- Horaires & phases (groupes, éliminations, finale)

**Métriques Clés :**
- Nombre de matchs simultanés
- Stades actifs par jour
- Niveau d'attractivité (Maroc, finale vs autres)

---

### 🚨 Domaine 5 : Sécurité & Infrastructures
**Sources :**
- Incidents simulés (basés sur CAN précédentes)
- Capacités infrastructures (stades, fan zones, hôpitaux)
- Dispositifs sécurité (effectifs police, Plan Orsec)

**Métriques Clés :**
- Nombre d'incidents par type
- Temps de résolution
- Disponibilité ressources (ambulances, forces)

---


##  MODULE INTELLIGENCE & ANTICIPATION

###  Composant 1 : Scoring de Risque
**Objectif :** Calculer un score 0-100 pour chaque zone/période

**Algorithme Simple :**
```python
risk_score = (
    affluence_ratio * 0.35 +          # Taux remplissage zone
    meteo_impact * 0.25 +              # Conditions météo
    traffic_congestion_index * 0.20 +  # Congestion routière
    infrastructure_strain * 0.20       # Tension infrastructures
) * 100
```

**Seuils d'Alerte :**
- 🟢 **0-40** : Situation normale
- 🟠 **40-70** : Vigilance renforcée
- 🔴 **70-100** : Action immédiate requise

---

### 🔔 Composant 2 : Système d'Alertes Intelligentes
**Déclencheurs Automatiques :**

| Condition | Alerte Générée | Action Recommandée |
|-----------|----------------|-------------------|
| Score risque > 70 | 🔴 CRITIQUE | Renfort transport/sécurité immédiat |
| Affluence > 85% capacité | 🟠 HAUTE | Rediriger flux, communication supporters |
| Intempéries + fan zone temporaire | 🔴 URGENCE | Évacuation préventive |
| Incident non résolu > 30 min | 🟠 ALERTE | Escalade équipes intervention |

**Intégration :**
- Power BI Alerts natives (email/SMS automatiques)
- Affichage prioritaire sur Dashboard Command Center

---

### 📈 Composant 3 : Prédiction Légère Affluence
**Modèle :** Régression linéaire simple (scikit-learn)

**Variables Prédictives :**
- Jour de match (oui/non)
- Attractivité match (Maroc/finale = coefficient 2x)
- Historique affluence même stade
- Conditions météo prévues
- Période vacances scolaires

**Output :** 
```
Affluence prévue Fan Zone Casablanca :
38 000 ± 4 000 personnes (18h-22h)
Recommandation : Capacité OK mais surveiller flux parking
```

**Technologie :** Python (pandas, scikit-learn), intégré via Azure ML endpoint

---

## 📊 DASHBOARDS POWER BI (3 Vues Stratégiques)

### 🎛️ Dashboard 1 : Command Center (Vue Globale)

**Audience :** Directeurs organisation, CAF, Ministère Intérieur

**KPIs Affichés :**
-  **Nombre incidents actifs** (temps réel)
-  **Stades/Fan zones sous tension** (% capacité)
-  **Niveau alerte global** (couleur dominante)
-  **Temps moyen résolution incidents** (objectif < 30 min)
-  **Carte de chaleur risque** par zone géographique

**Visuels :**
- Carte Maroc interactive (zones colorées rouge/orange/vert)
- Jauges KPI avec seuils
- Timeline incidents dernières 24h
- Top 5 zones critiques à surveiller

**Fonctionnalité Wow :**
- **Scénario What-If** : "Si pluie forte demain sur Rabat → Impact ?"
  - Slider météo → Recalcul automatique scores risque
  
---

###  Dashboard 2 : Mobilité & Accès Stades

**Audience :** Responsables transport, police routière

**Analyses :**
-  **Carte trafic temps réel** par axe routier
-  **Temps d'accès moyens** depuis fan zones → stades
-  **Taux d'occupation parkings** officiels
-  **Incidents routiers actifs** (localisation + gravité)

**Alertes Automatiques :**
- Congestion > 80% capacité route
- Temps accès > 30 min vs normal
- Parking plein (redirection alternatives)

**Recommandations Auto-générées :**
- "Activer navettes supplémentaires ligne Casablanca-Rabat"
- "Ouvrir parking B (1200 places) en anticipation"

---

###  Dashboard 3 : Fan Zones & Sécurité

**Audience :** Responsables fan zones, sécurité civile

**Monitoring :**
-  **Affluence temps réel** par fan zone (jauge % capacité)
-  **Alertes météo** impactant infrastructures temporaires
-  **Incidents sécurité** (type, gravité, résolution)
-  **Disponibilité ressources médicales** (ambulances, postes secours)

**Cas d'Usage Réel :**
> **Alerte automatique 16 déc. 14h** :
> " Fan Zone Casablanca (El Hank) : vents prévus 80 km/h (20h-23h).
> Structure temporaire à risque. Recommandation : évacuation préventive 18h."

**Heatmap Spéciale :**
- Carte fan zones avec code couleur risque
- Capacité résiduelle affichée en temps réel

---
