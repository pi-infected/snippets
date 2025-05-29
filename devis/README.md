# 🎨 Template de Devis Moderne - ReportLab

Un template ultra-élégant et moderne pour générer des devis professionnels avec ReportLab, utilisant votre couleur de marque **#a900d4**.

## ✨ Caractéristiques

- **Design ultra-moderne** avec attention particulière à l'alignement
- **Marges faibles** pour maximiser l'espace
- **Couleurs de marque** personnalisables (violet professionnel #a900d4 par défaut)
- **Tables organisées par groupes** avec sous-totaux automatiques
- **Support logo** d'entreprise
- **Interface simple** et intuitive
- **Styling professionnel** avec typographie soignée
- **🆕 Paiement Stripe intégré** avec QR codes automatiques
- **Texte en marge verticale** (watermark sophistiqué)

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 💳 Configuration Stripe (Optionnelle)

Pour activer les paiements en ligne avec QR codes :

1. **Copiez le fichier d'exemple :**
   ```bash
   cp example.env .env
   ```

2. **Modifiez le fichier `.env` avec votre clé Stripe :**
   ```bash
   # Ouvrez .env dans votre éditeur et remplacez :
   STRIPE_PRIVATE_KEY=sk_test_votre_vraie_cle_stripe_ici
   ```

3. **Pour la production, utilisez votre clé live :**
   ```bash
   STRIPE_PRIVATE_KEY=sk_live_votre_cle_privee_stripe_production
   ```

4. **Sécurité - Ajoutez .env à votre .gitignore :**
   ```bash
   echo ".env" >> .gitignore
   ```

> ⚠️ **Important :** 
> - Gardez votre clé privée Stripe secrète
> - Le fichier `.env` est automatiquement chargé au démarrage
> - Utilisez `sk_test_` pour les tests, `sk_live_` pour la production

## 🧪 Test de Configuration

Vérifiez que tout fonctionne :

```bash
python test_stripe.py
```

Ce test vérifie :
- ✅ Chargement du fichier `.env`
- ✅ Format de la clé Stripe
- ✅ Génération de QR codes
- ✅ Mode démo sans Stripe
- ✅ Configuration avec vraie clé (si disponible)

## 📖 Utilisation Simple

```python
from modern_invoice_template import (
    ModernInvoiceTemplate, CompanyInfo, ClientInfo, ItemGroup, InvoiceItem, ProjectInfo
)
from decimal import Decimal
from datetime import datetime

# Configuration de l'entreprise (avec RIB pour section bancaire)
company = CompanyInfo(
    name="Mon Entreprise",
    address="123 Rue de l'Innovation",
    postal_code="75001",
    city="Paris",
    phone="01 23 45 67 89",
    email="contact@monentreprise.fr",
    website="www.monentreprise.fr",
    rib_iban="FR76 1234 5678 9012 3456 789",
    rib_bic="ABCDEFGHIJK",
    rib_bank="Ma Banque"
)

# Configuration du client
client = ClientInfo(
    name="Client Premium",
    address="456 Avenue du Business",
    postal_code="69000",
    city="Lyon",
    email="client@example.com"
)

# Informations du projet
project = ProjectInfo(
    title="Développement Application Mobile",
    description="Création d'une application mobile moderne avec backend API..."
)

# Création d'un groupe d'items
group = ItemGroup(
    title="Développement Web",
    items=[
        InvoiceItem("Conception", 1, Decimal("2500.00"), "forfait"),
        InvoiceItem("Développement", 40, Decimal("75.00"), "heure"),
    ]
)

# Génération du devis
template = ModernInvoiceTemplate()
template.set_company_info(company)
template.set_client_info(client)
template.set_project_info(project)
template.set_invoice_details("DEV-2024-001", datetime.now())
template.add_item_group(group)
template.add_notes("Devis valable 30 jours")

# Export PDF (avec paiement Stripe automatique si configuré)
pdf_path = template.generate_pdf("mon_devis.pdf")
print(f"Devis créé: {pdf_path}")
```

## 🎯 Exemple Complet

Lancez l'exemple pour voir le template en action :

```bash
python example_usage.py
```

Cela génère un devis ultra-professionnel avec :
- ✅ Design sophistiqué et moderne
- ✅ Section projet avec description
- ✅ **Paiement Stripe avec QR code** (si configuré)
- ✅ Coordonnées bancaires (RIB)
- ✅ Texte en marge verticale pour confidentialité

## 💳 Fonctionnalités de Paiement

### QR Code Automatique
- **Génération automatique** d'un QR code coloré (#a900d4)
- **Scan mobile** pour paiement rapide
- **Design intégré** dans le PDF avec style professionnel

### Lien de Paiement Stripe
- **Sécurité maximale** via Stripe
- **Moyens de paiement** : CB, SEPA, Apple Pay, Google Pay
- **Confirmation automatique** par email
- **Métadonnées** incluant numéro de devis et client

### Configuration Automatique
```python
# Le template configure automatiquement Stripe si la clé est disponible
template = ModernInvoiceTemplate()  # Détecte STRIPE_PRIVATE_KEY automatiquement

# Ou configuration manuelle
template.setup_stripe_payment()  # Force la configuration
```

## 🎨 Personnalisation des Couleurs

Les couleurs sont facilement personnalisables dans la classe `ModernInvoiceTemplate` :

```python
# Couleurs par défaut (basées sur #a900d4)
PRIMARY_COLOR = colors.Color(169/255, 0/255, 212/255)    # #a900d4
SECONDARY_COLOR = colors.Color(240/255, 230/255, 250/255) # Version claire
ACCENT_COLOR = colors.Color(85/255, 0/255, 106/255)      # Version foncée
```

## 📁 Structure des Classes

### `InvoiceItem`
```python
@dataclass
class InvoiceItem:
    description: str        # Description de l'item
    quantity: float         # Quantité
    unit_price: Decimal     # Prix unitaire
    unit: str = "unité"     # Unité de mesure
```

### `ItemGroup`
```python
@dataclass
class ItemGroup:
    title: str                    # Titre du groupe
    items: List[InvoiceItem]      # Liste des items
    
    @property
    def subtotal(self) -> Decimal # Sous-total automatique
```

### `ProjectInfo`
```python
@dataclass
class ProjectInfo:
    title: str              # Nom du projet
    description: str = ""   # Description (Lorem ipsum par défaut)
```

### `CompanyInfo` & `ClientInfo`
Informations structurées pour l'entreprise et le client avec tous les champs nécessaires, y compris les coordonnées bancaires.

## 🔧 Méthodes Principales

### Configuration
- `set_company_info(company: CompanyInfo)` - Définit les infos entreprise
- `set_client_info(client: ClientInfo)` - Définit les infos client  
- `set_project_info(project: ProjectInfo)` - Définit le projet
- `set_invoice_details(number, date, due_date)` - Détails du devis
- `set_logo(logo_path: str)` - Ajoute le logo

### Contenu
- `add_item_group(group: ItemGroup)` - Ajoute un groupe d'items
- `add_notes(notes: str)` - Ajoute des notes (HTML supporté)

### Paiement 💳
- `setup_stripe_payment() -> bool` - Configure Stripe manuellement
- `_create_stripe_payment_link() -> str` - Génère le lien de paiement
- `_generate_qr_code(url: str) -> str` - Crée le QR code

### Génération
- `generate_pdf(filename: str) -> str` - Génère le PDF et retourne le chemin

## 🎨 Design Features

- **Marges optimisées** : 15mm sur tous les côtés
- **Typographie moderne** : Helvetica avec hiérarchie claire
- **Couleurs harmonieuses** : Palette basée sur votre violet #a900d4
- **Alignements parfaits** : Tables et textes parfaitement alignés
- **Espacement maîtrisé** : Respiration optimale entre les sections
- **Support logo** : Intégration élégante de votre logo d'entreprise
- **🆕 QR Code stylé** : Couleurs de marque et positionnement professionnel
- **🆕 Watermark discret** : Numéro de devis en marge verticale

## 📄 Format de Sortie

- Format A4 professionnel
- Fichier PDF haute qualité
- Métadonnées intégrées (titre, auteur)
- Optimisé pour impression et affichage numérique
- **QR code intégré** pour paiement mobile
- **Sections organisées** : Projet, Items, Paiement, RIB, Conditions

## 🆘 Support

Le template gère automatiquement :
- ✅ Calculs des totaux et sous-totaux
- ✅ Formatage des devises (€)
- ✅ Dates au format français (DD/MM/YYYY)
- ✅ Gestion d'erreurs avec messages explicites
- ✅ Support HTML dans les notes
- ✅ Pagination automatique pour longs devis
- ✅ **Stripe API** avec gestion d'erreurs robuste
- ✅ **QR codes** avec nettoyage automatique des fichiers temporaires

## 🔒 Sécurité

- **Clés Stripe** : Stockage sécurisé via variables d'environnement
- **Fichiers temporaires** : Nettoyage automatique des QR codes
- **Validation** : Vérification des données avant génération PDF
- **Gestion d'erreurs** : Messages clairs en cas de problème

---

*Template créé avec passion pour des devis ultra-professionnels avec paiement moderne* 💳💜 