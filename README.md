# TrocTendance

![TrocTendance Logo](static/images/logo.png)

### 🌟 Marketplace de Vêtements de Seconde Main Élégante et Responsable
  
  [![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*Donnez une seconde vie à vos vêtements avec style et responsabilité*
---

## 📖 Table des Matières

- [🎯 À Propos](#-à-propos)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🛠️ Technologies Utilisées](#️-technologies-utilisées)
- [⚙️ Installation](#️-installation)
- [🚀 Démarrage Rapide](#-démarrage-rapide)
- [📱 Aperçu de l'Application](#-aperçu-de-lapplication)
- [🏗️ Architecture](#️-architecture)
- [🔧 Configuration](#-configuration)
- [📸 Captures d'Écran](#-captures-décran)
- [🤝 Contribution](#-contribution)
- [📄 Licence](#-licence)
- [📞 Contact](#-contact)

---

## 🎯 À Propos

**TrocTendance** est une marketplace moderne et élégante dédiée à la vente de vêtements de seconde main. Conçue avec une approche responsable et durable, elle permet aux utilisateurs d'acheter, vendre et échanger des vêtements de qualité tout en contribuant à l'économie circulaire.

### 🌍 Notre Mission

- **Durabilité** : Promouvoir la mode circulaire et réduire le gaspillage textile
- **Accessibilité** : Rendre la mode de qualité accessible à tous
- **Communauté** : Créer un écosystème de confiance entre acheteurs et vendeurs
- **Innovation** : Offrir une expérience utilisateur moderne et intuitive

---

## ✨ Fonctionnalités

### 👤 **Gestion des Utilisateurs**

- ✅ Inscription et connexion sécurisées
- ✅ Profils utilisateurs personnalisables avec avatar
- ✅ Système de notation et d'avis bidirectionnel
- ✅ Historique complet des transactions

### 🛍️ **Marketplace Avancée**

- ✅ Catalogue de produits avec filtrage intelligent
- ✅ Recherche avancée multi-critères
- ✅ Catégorisation détaillée (robes, pantalons, boubous, etc.)
- ✅ Support des images multiples avec compression automatique
- ✅ Gestion des stocks et statuts de produits

### 💬 **Communication Intégrée**

- ✅ Système de messagerie en temps réel
- ✅ Conversations organisées par produit
- ✅ Notifications push pour nouveaux messages
- ✅ Messages rapides prédéfinis

### 🛒 **Processus de Commande**

- ✅ Panier et checkout sécurisé
- ✅ Simulation de paiement intégrée
- ✅ Suivi de commande en temps réel
- ✅ Gestion des livraisons et retraits

### 🔄 **Système d'Échange**

- ✅ Propositions d'échange entre utilisateurs
- ✅ Négociation facilitée
- ✅ Historique des échanges

### 📊 **Tableau de Bord**

- ✅ Statistiques de vente en temps réel
- ✅ Analyse des revenus avec commission
- ✅ Gestion des commandes vendeur/acheteur
- ✅ Suivi des performances

### 🎨 **Design & UX**

- ✅ Interface responsive et moderne
- ✅ Animations fluides et micro-interactions
- ✅ Design system cohérent
- ✅ Accessibilité optimisée

---

## 🛠️ Technologies Utilisées

### **Backend**

- **Django 4.2+** - Framework web Python robuste
- **Django REST Framework** - API REST pour les interactions frontend
- **SQLite** - Base de données légère pour développement
- **Pillow** - Traitement d'images avancé
- **Django Crispy Forms** - Rendu de formulaires élégant

### **Frontend**

- **TailwindCSS** - Framework CSS utilitaire moderne
- **JavaScript Vanilla** - Interactions dynamiques sans dépendances
- **HTML5 Sémantique** - Structure accessible et SEO-friendly
- **Font Awesome** - Icônes vectorielles

### **Outils de Développement**

- **Git** - Contrôle de version
- **VS Code** - Environnement de développement
- **Django Debug Toolbar** - Débogage et optimisation
- **Black** - Formatage automatique du code Python

---

## ⚙️ Installation

### Prérequis

- Python 3.9+ installé
- Git installé
- Node.js (pour TailwindCSS)

### Étapes d'Installation

```bash
# 1. Cloner le repository
git clone https://github.com/Mouha7/TrocTendance.git
cd TrocTendance

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement virtuel
# Sur Windows
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate

# 4. Installer les dépendances Python
pip install -r requirements.txt

# 5. Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# 6. Charger les données de démonstration
python manage.py loaddata fixtures/users.json
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/products.json
python manage.py loaddata fixtures/product_images.json
python manage.py loaddata fixtures/orders.json
python manage.py loaddata fixtures/reviews.json
python manage.py loaddata fixtures/messages.json

# 7. Créer un superutilisateur (optionnel)
python manage.py createsuperuser

# 8. Compiler TailwindCSS
npm install
npm run build-css

# 9. Lancer le serveur de développement
python manage.py runserver
```

---

## 🚀 Démarrage Rapide

Une fois l'installation terminée :

1. **Accédez à l'application** : `http://localhost:8000`
2. **Créez un compte** ou connectez-vous avec les données de démonstration
3. **Explorez le catalogue** de vêtements disponibles
4. **Ajoutez vos propres articles** à vendre
5. **Commencez à négocier** avec d'autres utilisateurs

### Comptes de Démonstration

```
Vendeur/Acheteur :
- Email: fatou_diouf
- Mot de passe: passer123

Vendeur/Acheteur :
- Email: alioune_sow 
- Mot de passe: passer123
```

---

## 📱 Aperçu de l'Application

### Pages Principales

- **🏠 Accueil** : Page d'accueil avec présentation et statistiques
- **📋 Catalogue** : Naviguation et filtrage des produits
- **👕 Détail Produit** : Informations complètes avec galerie d'images
- **🛒 Checkout** : Processus de commande sécurisé
- **💬 Messages** : Interface de communication intégrée
- **📊 Tableau de Bord** : Gestion des ventes et achats
- **👤 Profil** : Gestion du compte utilisateur

---

## 🏗️ Architecture

```
TrocTendance/
├── 📁 core/                    # Applications Django
│   ├── 📁 accounts/           # Gestion utilisateurs
│   ├── 📁 products/           # Catalogue produits
│   └── 📁 orders/             # Commandes et messages
├── 📁 templates/              # Templates HTML
│   ├── 📁 accounts/
│   ├── 📁 products/
│   ├── 📁 orders/
│   └── base.html
├── 📁 static/                 # Ressources statiques
│   ├── 📁 css/               # Styles compilés
│   ├── 📁 js/                # Scripts JavaScript
│   └── 📁 images/            # Images et assets
├── 📁 media/                  # Uploads utilisateurs
├── 📁 fixtures/               # Données de démonstration
├── 📄 manage.py              # Commandes Django
├── 📄 requirements.txt       # Dépendances Python
└── 📄 README.md             # Documentation
```

---

## 🔧 Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet :

```env
# Base de données
DATABASE_URL=sqlite:///db.sqlite3

# Sécurité
SECRET_KEY=votre-clé-secrète-django
DEBUG=True

# Email (pour production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe

# Médias
MEDIA_ROOT=media/
MEDIA_URL=/media/

# Statiques
STATIC_ROOT=staticfiles/
STATIC_URL=/static/
```

### Configuration de Production

Pour déployer en production :

1. Configurez une base de données PostgreSQL
2. Utilisez un serveur de médias (AWS S3, Cloudinary)
3. Configurez un serveur web (Nginx + Gunicorn)
4. Activez HTTPS et les headers de sécurité
5. Configurez le monitoring et les logs

---

## 📸 Captures d'Écran

<div align="center">
  
### 🏠 Page d'Accueil

*Interface élégante avec navigation intuitive*

### 📋 Catalogue de Produits

*Filtrage avancé et présentation moderne*

### 💬 Système de Messagerie

*Communication fluide entre utilisateurs*

### 📊 Tableau de Bord Vendeur

*Statistiques en temps réel et gestion des ventes*

## 🤝 Contribution

Nous accueillons avec plaisir les contributions de la communauté !

### Comment Contribuer

1. **Fork** le projet
2. **Créez** une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Commitez** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrez** une Pull Request

### Standards de Code

- Suivez PEP 8 pour Python
- Utilisez des noms de variables descriptifs
- Commentez le code complexe
- Ajoutez des tests pour les nouvelles fonctionnalités
- Mettez à jour la documentation

### Roadmap

- [ ] **API REST complète** pour mobile
- [ ] **Application mobile** React Native
- [ ] **Intégration paiements** réels (Wave, Orange Money)
- [ ] **Système de recommandations** IA
- [ ] **Géolocalisation** avancée
- [ ] **Mode sombre** interface
- [ ] **Multi-langues** support

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">
  
### 🌟 Si ce projet vous plaît, donnez-lui une étoile

*Fait avec ❤️ pour une mode plus durable*

### 🌟 Si ce projet vous plaît, donnez-lui une étoile

*Fait avec ❤️ pour une mode plus durable*

**[⬆ Retour en haut](#troctendance)**
