# 🎨 Template de Devis Moderne - ReportLab

Un template ultra-élégant et moderne pour générer des devis professionnels avec ReportLab, utilisant votre couleur de marque.

## ✨ Caractéristiques

- **Design moderne** avec attention particulière à l'alignement
- **Marges faibles** pour maximiser l'espace
- **Couleurs de marque** personnalisables
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

**Créez le fichier `.env` avec votre clé Stripe :**
   ```bash
   # Ouvrez .env dans votre éditeur et remplacez :
   STRIPE_PRIVATE_KEY=sk_live_votre_vraie_cle_stripe_ici
   ```

> ⚠️ **Important :** 
> - Gardez votre clé privée Stripe secrète
> - Le fichier `.env` est automatiquement chargé au démarrage
> - Utilisez la clef `sk_test_` pour les tests et `sk_live_` pour la production

## 🎨 Personnalisation des Couleurs

Les couleurs sont facilement personnalisables dans la classe `ModernInvoiceTemplate` :

```python
# Couleurs par défaut
PRIMARY_COLOR = colors.Color(169/255, 0/255, 212/255)    # #a900d4
SECONDARY_COLOR = colors.Color(240/255, 230/255, 250/255) # Version claire
ACCENT_COLOR = colors.Color(85/255, 0/255, 106/255)      # Version foncée
```