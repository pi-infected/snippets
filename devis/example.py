#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple anonymisé de devis - Site E-commerce Professionnel
Démonstration complète des fonctionnalités du template moderne
"""

import hashlib
from datetime import datetime, timedelta
from decimal import Decimal
from invoice import (
  InvoiceTemplate,
  ModernInvoiceTemplate, 
  CompanyInfo, 
  ClientInfo, 
  ItemGroup, 
  InvoiceItem,
  ProjectInfo
)


def create_demo_invoice():
  """Crée un devis de démonstration pour un projet e-commerce"""
  
  # Informations de l'entreprise fictive
  company = CompanyInfo(
    name="Digital Solutions SARL",
    address="42 Avenue des Technologies",
    postal_code="75008",
    city="Paris",
    phone="01 42 85 96 47",
    email="contact@digital-solutions.example",
    website="www.digital-solutions.example",
    siret="84512345600019",
    rib_iban="FR14 2004 1010 0505 0001 3M02 606",
    rib_bic="PSSTFRPPPAR",
    rib_bank="La Banque Postale",
    vat_status="company_with_vat",  # Société soumise à TVA
    vat_number="FR25845123456"  # Numéro de TVA intracommunautaire
  )
  
  # Informations du client fictif
  client = ClientInfo(
    name="Entreprise ModaStyle",
    address="156 Rue du Commerce",
    postal_code="69002",
    city="Lyon",
    email="direction@modastyle-demo.example"
  )
  
  # Informations du projet
  project = ProjectInfo(
    title="Plateforme E-commerce Premium",
    description="""
    <b>CONTEXTE & VISION</b><br/>
    ModaStyle souhaite révolutionner sa présence digitale en lançant une plateforme e-commerce 
    moderne et performante pour commercialiser sa gamme de vêtements premium. L'objectif est de 
    créer une expérience utilisateur exceptionnelle qui reflète l'image haut de gamme de la marque.<br/><br/>

    <b>PÉRIMÈTRE FONCTIONNEL</b><br/>
    • <b>Frontend moderne :</b> Interface utilisateur responsive et élégante avec React.js<br/>
    • <b>Backend robuste :</b> API REST sécurisée avec Node.js et base de données PostgreSQL<br/>
    • <b>Gestion produits :</b> Catalogue avancé avec variantes, stock, promotions automatisées<br/>
    • <b>Tunnel de commande :</b> Processus d'achat optimisé avec paiements multiples (Stripe, PayPal)<br/>
    • <b>Administration :</b> Back-office complet pour la gestion quotidienne<br/>
    • <b>Marketing digital :</b> Intégrations SEO, analytics, newsletters, réseaux sociaux<br/><br/>

    <b>INNOVATION TECHNIQUE</b><br/>
    • <b>Performance :</b> Optimisation avancée avec mise en cache Redis et CDN<br/>
    • <b>Mobile-first :</b> PWA (Progressive Web App) pour une expérience mobile native<br/>
    • <b>IA intégrée :</b> Recommandations personnalisées et chatbot d'assistance<br/>
    • <b>Analytics :</b> Dashboard en temps réel avec KPIs métier personnalisés
    """
  )
  
  # Groupe 1 : Conception & Design
  design_group = ItemGroup(
    title="Phase 1 - Conception & Design UX/UI",
    items=[
      InvoiceItem(
        description="Atelier de cadrage et audit de l'existant - Analyse concurrentielle et définition de la stratégie digitale",
        quantity=3,
        unit_price=Decimal("800.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Conception UX/UI - Wireframes, maquettes haute-fidélité, design system, prototype interactif",
        quantity=8,
        unit_price=Decimal("750.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Charte graphique digitale - Adaptation de l'identité visuelle pour le web, iconographie personnalisée",
        quantity=4,
        unit_price=Decimal("600.00"),
        unit="jours"
      ),
    ]
  )
  
  # Groupe 2 : Développement Frontend
  frontend_group = ItemGroup(
    title="Phase 2 - Développement Frontend",
    items=[
      InvoiceItem(
        description="Setup technique - Configuration React.js, outils de build (Webpack, Vite), structure projet",
        quantity=2,
        unit_price=Decimal("700.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Développement interface utilisateur - Composants React, pages produits, panier, tunnel de commande",
        quantity=12,
        unit_price=Decimal("650.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Responsive design - Adaptation mobile/tablette, optimisation tactile, PWA",
        quantity=5,
        unit_price=Decimal("620.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Animations & interactions - Micro-animations, transitions fluides, feedback utilisateur",
        quantity=3,
        unit_price=Decimal("680.00"),
        unit="jours"
      ),
    ]
  )
  
  # Groupe 3 : Développement Backend & API
  backend_group = ItemGroup(
    title="Phase 3 - Backend & Infrastructure",
    items=[
      InvoiceItem(
        description="Architecture backend - Setup Node.js/Express, structure API REST, middleware de sécurité",
        quantity=4,
        unit_price=Decimal("720.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Base de données - Modélisation PostgreSQL, migrations, optimisations des requêtes",
        quantity=3,
        unit_price=Decimal("700.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Gestion produits & stock - CRUD avancé, gestion des variantes, stock temps réel",
        quantity=6,
        unit_price=Decimal("650.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Système de commandes - Workflow complet, gestion états, historique, facturation",
        quantity=5,
        unit_price=Decimal("680.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Intégrations paiement - Stripe, PayPal, sécurisation PCI DSS",
        quantity=4,
        unit_price=Decimal("750.00"),
        unit="jours"
      ),
    ]
  )
  
  # Groupe 4 : Fonctionnalités Avancées
  advanced_group = ItemGroup(
    title="Phase 4 - Fonctionnalités Premium",
    items=[
      InvoiceItem(
        description="Back-office administration - Dashboard, gestion produits, commandes, clients, statistiques",
        quantity=8,
        unit_price=Decimal("620.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Module de recommandations IA - Algorithme de suggestions, analyse comportementale",
        quantity=5,
        unit_price=Decimal("800.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Système de fidélité - Points, rewards, coupons, parrainage",
        quantity=4,
        unit_price=Decimal("650.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Intégrations marketing - Google Analytics, Facebook Pixel, Mailchimp, SEO technique",
        quantity=3,
        unit_price=Decimal("600.00"),
        unit="jours"
      ),
    ]
  )
  
  # Groupe 5 : Déploiement & Formation
  deployment_group = ItemGroup(
    title="Phase 5 - Mise en Production",
    items=[
      InvoiceItem(
        description="Infrastructure cloud - Setup AWS/OVH, Docker, CI/CD, monitoring, sauvegardes",
        quantity=4,
        unit_price=Decimal("750.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Tests & optimisations - Tests automatisés, performance, sécurité, audit qualité",
        quantity=3,
        unit_price=Decimal("700.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Formation équipe - Sessions hands-on pour back-office, bonnes pratiques, maintenance",
        quantity=2,
        unit_price=Decimal("800.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Documentation complète - Guides utilisateur, technique, procédures de maintenance",
        quantity=2,
        unit_price=Decimal("600.00"),
        unit="jours"
      ),
      InvoiceItem(
        description="Support post-lancement - Assistance 30 jours, corrections mineures, optimisations",
        quantity=1,
        unit_price=Decimal("1500.00"),
        unit="forfait"
      ),
    ]
  )
  
  # Création du template
  template = ModernInvoiceTemplate()
  
  # Configuration complète
  template.set_company_info(company)
  template.set_client_info(client)
  template.set_project_info(project)
  
  # Génération d'un numéro de devis unique
  current_date = datetime.now()
  hash_input = f"DS-2025-ECOM-{current_date.strftime('%Y%m%d')}"
  md5_hash = hashlib.md5(hash_input.encode()).hexdigest()
  invoice_number = f"DS-2025-{md5_hash[:6].upper()}"
  
  template.set_invoice_details(
    number=invoice_number,
    date=current_date,
    due_date=current_date + timedelta(days=45)
  )
  
  # Logo (si disponible)
  template.set_logo("logo.png")
  
  # Ajout de tous les groupes de tâches
  template.add_item_group(design_group)
  template.add_item_group(frontend_group)
  template.add_item_group(backend_group)
  template.add_item_group(advanced_group)
  template.add_item_group(deployment_group)
  
  # Configuration du pourcentage de paiement à 40% (pour démarrer le projet)
  template.set_payment_percentage(0.4)
  
  # Définition du titre du devis
  template.set_invoice_title("DEVIS E-COMMERCE PREMIUM")
  
  # Notes professionnelles complètes
  notes = """
  <b>🔹 CALENDRIER DE FACTURATION :</b><br/>
  • <b>Acompte initial :</b> 40% à la signature du présent devis (voir QR code ci-dessus)<br/>
  • <b>Étape intermédiaire :</b> 35% à la validation des phases 1 & 2 (Design + Frontend)<br/>
  • <b>Livraison finale :</b> 25% à la mise en production et formation terminée<br/>
  • <b>Conditions de paiement :</b> 30 jours nets après émission de facture<br/><br/>
  
  <b>🔹 PRESTATIONS & GARANTIES :</b><br/>
  • <b>Méthodologie Agile :</b> Sprints de 2 semaines avec démonstrations régulières<br/>
  • <b>Propriété intellectuelle :</b> Code source livré intégralement au client<br/>
  • <b>Garantie technique :</b> 6 mois de corrections bugs sans surcoût<br/>
  • <b>Formation incluse :</b> Sessions utilisateur et technique pour l'équipe<br/>
  • <b>Hébergement 1ère année :</b> Offert (hébergement haute performance inclus)<br/><br/>
  
  <b>🔹 OPTIONS & ÉVOLUTIONS :</b><br/>
  • <b>Marketplace multi-vendeurs :</b> +15 000€ HT (module optionnel)<br/>
  • <b>Application mobile native :</b> +25 000€ HT (iOS + Android)<br/>
  • <b>Module B2B avancé :</b> +12 000€ HT (devis, commandes groupées)<br/><br/>
  
  <b>🔹 CONDITIONS GÉNÉRALES :</b><br/>
  • <b>Validité du devis :</b> 45 jours à compter de la date d'émission<br/>
  • <b>Délai de réalisation :</b> 16 semaines à partir de la validation du design<br/>
  • <b>TVA :</b> 20% en sus (société soumise à TVA)<br/>
  • <b>Révisions :</b> 3 cycles de révisions inclus par phase de validation<br/>
  • <b>Clause de confidentialité :</b> NDA mutuel signé avant démarrage
  """
  template.add_notes(notes)
  
  # Génération du PDF
  try:
    pdf_path = template.generate_pdf("devis_demo_ecommerce.pdf")
    print(f"✅ Devis de démonstration généré : {pdf_path}")
    print(f"📊 Nombre de groupes de tâches : {len([design_group, frontend_group, backend_group, advanced_group, deployment_group])}")
    print(f"💰 Montant total du projet : {sum(group.subtotal for group in [design_group, frontend_group, backend_group, advanced_group, deployment_group]):.2f}€ HT")
    return pdf_path
  except Exception as e:
    print(f"❌ Erreur lors de la génération du devis : {e}")
    return None


if __name__ == "__main__":
  create_demo_invoice()
