#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Template de devis moderne et élégant utilisant ReportLab
Couleur principale: #a900d4 (violet professionnel)
Design ultra-professionnel avec attention aux détails
"""

import os
from datetime import datetime
from typing import List, Optional, Any
from dataclasses import dataclass
from decimal import Decimal
from dotenv import load_dotenv

import stripe
import qrcode

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
  Paragraph, Spacer, Table, TableStyle, 
  KeepTogether, Image, PageTemplate, BaseDocTemplate, Frame
)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY

load_dotenv()

@dataclass
class InvoiceItem:
  """Item d'un devis avec description, quantité, prix unitaire"""
  description: str
  quantity: float
  unit_price: Decimal
  unit: str = "unité"
  
  @property
  def total_price(self) -> Decimal:
    return Decimal(str(self.quantity)) * self.unit_price


@dataclass
class ItemGroup:
  """Groupe d'items avec sous-total"""
  title: str
  items: List[InvoiceItem]
  
  @property
  def subtotal(self) -> Decimal:
    return sum(item.total_price for item in self.items)


@dataclass
class CompanyInfo:
  """Informations de l'entreprise"""
  name: str
  address: str
  postal_code: str
  city: str
  phone: str
  email: str
  siret: Optional[str] = None
  website: Optional[str] = None
  rib_iban: Optional[str] = None
  rib_bic: Optional[str] = None
  rib_bank: Optional[str] = None
  vat_status: str = "auto_entrepreneur"  # "auto_entrepreneur", "company_with_vat", "company_exempt"
  vat_number: Optional[str] = None  # Numéro de TVA intracommunautaire si applicable


@dataclass
class ClientInfo:
  """Informations du client"""
  name: str
  address: str
  postal_code: str
  city: str
  email: Optional[str] = None


@dataclass
class ProjectInfo:
  """Informations du projet"""
  title: str
  description: str = ""


class InvoiceTemplate(BaseDocTemplate):
  """Template de document personnalisé avec texte en marge verticale"""
  
  def __init__(self, filename, invoice_number="", **kwargs):
    self.invoice_number = invoice_number
    BaseDocTemplate.__init__(self, filename, **kwargs)
    
    # Configuration des marges
    margin = 15 * mm
    frame = Frame(
      margin, margin, 
      A4[0] - 2*margin, A4[1] - 2*margin,
      leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0
    )
    
    template = PageTemplate(id='normal', frames=[frame], onPage=self._draw_margin_text)
    self.addPageTemplates([template])
  
  def _draw_margin_text(self, canvas, doc):
    """Dessine le texte en marge verticale"""
    canvas.saveState()
    
    # Couleur violette claire pour le texte en marge
    canvas.setFillColor(colors.Color(169/255, 0/255, 212/255, alpha=0.3))
    canvas.setFont("Helvetica", 8)
    
    # Texte vertical sur la marge gauche
    if self.invoice_number:
      canvas.rotate(90)
      canvas.drawString(
        50 * mm,  # Position Y (après rotation)
        -8 * mm,  # Position X (après rotation) 
        f"DEVIS {self.invoice_number} • CONFIDENTIEL"
      )
    
    canvas.restoreState()


class ModernInvoiceTemplate:
  """
  Template moderne et élégant pour générer des devis professionnels ultra-sophistiqués
  
  Utilisation:
    template = ModernInvoiceTemplate()
    template.set_company_info(company)
    template.set_client_info(client)
    template.set_project_info(project)
    template.add_item_group(group)
    template.generate_pdf("devis_001.pdf")
  """
  
  # Couleurs du thème professionnelles (palette bleu marine et gris)
  PRIMARY_COLOR = colors.Color(25/255, 55/255, 109/255)  # Bleu marine professionnel #19376D
  SECONDARY_COLOR = colors.Color(248/255, 249/255, 252/255)  # Gris très clair #F8F9FC
  ACCENT_COLOR = colors.Color(15/255, 35/255, 70/255)  # Bleu foncé #0F2346
  GRADIENT_START = colors.Color(100/255, 130/255, 180/255)  # Bleu moyen pour gradients #6482B4
  GRADIENT_END = colors.Color(245/255, 247/255, 250/255)  # Gris très clair #F5F7FA
  GREY_LIGHT = colors.Color(0.96, 0.97, 0.98)  # Gris clair
  GREY_MEDIUM = colors.Color(0.55, 0.60, 0.65)  # Gris moyen
  GREY_DARK = colors.Color(0.15, 0.20, 0.25)  # Gris foncé
  WHITE = colors.white
  BLACK = colors.black
  SEPARATOR_COLOR = colors.Color(200/255, 210/255, 220/255)  # Gris-bleu clair #C8D2DC
  
  def __init__(self):
    self.company_info: Optional[CompanyInfo] = None
    self.client_info: Optional[ClientInfo] = None
    self.project_info: Optional[ProjectInfo] = None
    self.item_groups: List[ItemGroup] = []
    self.invoice_number: str = ""
    self.invoice_date: datetime = datetime.now()
    self.due_date: Optional[datetime] = None
    self.notes: str = ""
    self.logo_path: Optional[str] = None
    self.payment_percentage: float = 1.0  # Proportion du montant pour le paiement (1.0 = 100%, 0.3 = 30%)
    self.invoice_title: str = "DEVIS PROFESSIONNEL"  # Titre personnalisable du devis
    
    # Configuration des marges ultra-fines
    self.margin_left = 15 * mm
    self.margin_right = 15 * mm
    self.margin_top = 15 * mm
    self.margin_bottom = 15 * mm
    
    # Styles personnalisés ultra-sophistiqués
    self._setup_styles()

    # Configuration Stripe
    self.stripe_private_key = os.getenv("STRIPE_PRIVATE_KEY")
    if self.stripe_private_key:
      stripe.api_key = self.stripe_private_key
    
    # QR Code et paiement
    self.payment_link: Optional[str] = None
    self.qr_code_path: Optional[str] = None

  def _setup_styles(self):
    """Configure les styles personnalisés ultra-sophistiqués"""
    self.styles = getSampleStyleSheet()
    
    # Style pour le titre principal (plus imposant)
    self.styles.add(ParagraphStyle(
      name='UltraTitle',
      parent=self.styles['Title'],
      fontSize=32,
      textColor=self.PRIMARY_COLOR,
      spaceAfter=15,
      fontName='Times-Bold',
      alignment=TA_LEFT,
      leading=36
    ))
    
    # Style pour les titres de projet
    self.styles.add(ParagraphStyle(
      name='ProjectTitle',
      parent=self.styles['Heading1'],
      fontSize=18,
      textColor=self.ACCENT_COLOR,
      spaceAfter=10,
      spaceBefore=10,
      fontName='Times-Bold',
      alignment=TA_LEFT,
      leading=22
    ))
    
    # Style pour les sous-titres élégants
    self.styles.add(ParagraphStyle(
      name='ElegantSubtitle',
      parent=self.styles['Heading2'],
      fontSize=13,
      textColor=self.ACCENT_COLOR,
      spaceAfter=8,
      spaceBefore=15,
      fontName='Times-Bold',
      alignment=TA_LEFT,
      borderPadding=5,
      leftIndent=5
    ))
    
    # Style pour le texte sophistiqué
    self.styles.add(ParagraphStyle(
      name='SophisticatedNormal',
      parent=self.styles['Normal'],
      fontSize=10,
      textColor=self.GREY_DARK,
      spaceAfter=6,
      fontName='Times-Roman',
      leading=15,
      alignment=TA_JUSTIFY
    ))
    
    # Style pour les informations VIP
    self.styles.add(ParagraphStyle(
      name='VIPInfo',
      parent=self.styles['Normal'],
      fontSize=11,
      textColor=self.BLACK,
      fontName='Times-Bold',
      spaceAfter=8,
      leading=16
    ))
    
    # Style pour les totaux premium
    self.styles.add(ParagraphStyle(
      name='PremiumTotal',
      parent=self.styles['Normal'],
      fontSize=14,
      textColor=self.PRIMARY_COLOR,
      fontName='Times-Bold',
      alignment=TA_RIGHT,
      spaceAfter=10
    ))
    
    # Style pour les encadrés
    self.styles.add(ParagraphStyle(
      name='BoxedContent',
      parent=self.styles['Normal'],
      fontSize=9,
      textColor=self.GREY_DARK,
      fontName='Times-Roman',
      leading=12,
      leftIndent=10,
      rightIndent=10,
      spaceAfter=8
    ))

  def set_company_info(self, company: CompanyInfo):
    """Définit les informations de l'entreprise"""
    self.company_info = company
  
  def set_client_info(self, client: ClientInfo):
    """Définit les informations du client"""
    self.client_info = client
  
  def set_project_info(self, project: ProjectInfo):
    """Définit les informations du projet"""
    self.project_info = project
  
  def set_invoice_details(self, number: str, date: datetime = None, due_date: datetime = None):
    """Définit les détails du devis"""
    self.invoice_number = number
    if date:
      self.invoice_date = date
    self.due_date = due_date
  
  def set_logo(self, logo_path: str):
    """Définit le chemin vers le logo"""
    if os.path.exists(logo_path):
        self.logo_path = logo_path
  
  def add_item_group(self, group: ItemGroup):
    """Ajoute un groupe d'items"""
    self.item_groups.append(group)
  
  def add_notes(self, notes: str):
    """Ajoute des notes au devis"""
    self.notes = notes
  
  def set_payment_percentage(self, percentage: float):
    """Définit le pourcentage du montant total à demander pour le paiement (0.0 à 1.0)"""
    if not 0.0 <= percentage <= 1.0:
      raise ValueError("Le pourcentage doit être entre 0.0 et 1.0")
    self.payment_percentage = percentage
  
  def set_invoice_title(self, title: str):
    """Définit le titre du devis"""
    self.invoice_title = title
  
  def configure_vat_status(self, status: str, vat_number: Optional[str] = None):
    """
    Configure le statut TVA de l'entreprise
    
    Args:
      status: Type de statut TVA
        - "auto_entrepreneur": Auto-entrepreneur en franchise de TVA
        - "company_with_vat": Société soumise à TVA
        - "company_exempt": Société exonérée de TVA
      vat_number: Numéro de TVA intracommunautaire (optionnel)
    """
    if self.company_info:
      self.company_info.vat_status = status
      if vat_number:
        self.company_info.vat_number = vat_number
    else:
      raise ValueError("Les informations de l'entreprise doivent être définies avant de configurer la TVA")
  
  def _create_elegant_separator(self) -> Table:
    """Crée une ligne de séparation élégante"""
    separator_data = [['', '']]
    separator_table = Table(separator_data, colWidths=[180*mm, 0])
    separator_table.setStyle(TableStyle([
      ('LINEBELOW', (0, 0), (0, 0), 0.5, self.SEPARATOR_COLOR),
      ('LEFTPADDING', (0, 0), (-1, -1), 0),
      ('RIGHTPADDING', (0, 0), (-1, -1), 0),
      ('TOPPADDING', (0, 0), (-1, -1), 0),
      ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return separator_table
  
  def _create_header(self) -> List[Any]:
    """Crée l'en-tête sophistiqué avec logo et informations entreprise"""
    elements = []
    
    # Encadré élégant pour l'en-tête
    header_data = []
    
    if self.logo_path and os.path.exists(self.logo_path):
      try:
        logo = Image(self.logo_path, width=25*mm, height=25*mm, hAlign='LEFT')
        company_text = f"""
        <font size="16" color="{self.PRIMARY_COLOR.hexval()}"><b>{self.company_info.name}</b></font><br/>
        <font size="9" color="{self.GREY_DARK.hexval()}">
        {self.company_info.address}<br/>
        {self.company_info.postal_code} {self.company_info.city}<br/>
        <b>Tel:</b> {self.company_info.phone}<br/>
        <b>Email:</b> {self.company_info.email}
        </font>
        """
        if self.company_info.website:
          company_text += f'<br/><font size="9" color="{self.PRIMARY_COLOR.hexval()}"><b>{self.company_info.website}</b></font>'
        
        header_data = [[logo, Paragraph(company_text, self.styles['SophisticatedNormal'])]]
      except:
        header_data = [[self._create_company_text_only()]]
    else:
      header_data = [[self._create_company_text_only()]]
    
    header_table = Table(header_data, colWidths=[35*mm, 145*mm])
    header_table.setStyle(TableStyle([
      ('ALIGN', (0, 0), (0, 0), 'LEFT'),
      ('ALIGN', (1, 0), (1, 0), 'LEFT'),
      ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      ('BACKGROUND', (0, 0), (-1, -1), self.SECONDARY_COLOR),
      ('LEFTPADDING', (0, 0), (-1, -1), 12),
      ('RIGHTPADDING', (0, 0), (-1, -1), 12),
      ('TOPPADDING', (0, 0), (-1, -1), 12),
      ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
      ('ROUNDEDCORNERS', (0, 0), (-1, -1), [3, 3, 3, 3]),
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 15))
    
    return elements
  
  def _create_company_text_only(self) -> Paragraph:
    """Crée le texte de l'entreprise sans logo (version sophistiquée)"""
    company_text = f"""
    <font size="20" color="{self.PRIMARY_COLOR.hexval()}"><b>{self.company_info.name}</b></font><br/>
    <font size="10" color="{self.GREY_DARK.hexval()}">
    {self.company_info.address}<br/>
    {self.company_info.postal_code} {self.company_info.city}<br/>
    <b>Tel:</b> {self.company_info.phone} • <b>Email:</b> {self.company_info.email}
    </font>
    """
    if self.company_info.website:
      company_text += f'<br/><font size="10" color="{self.PRIMARY_COLOR.hexval()}"><b>{self.company_info.website}</b></font>'
    
    return Paragraph(company_text, self.styles['SophisticatedNormal'])
  
  def _create_invoice_title_and_info(self) -> List[Any]:
    """Crée le titre du devis et informations avec design sophistiqué"""
    elements = []
    
    # Titre principal ultra-imposant
    title = Paragraph(self.invoice_title, self.styles['UltraTitle'])
    elements.append(title)
    elements.append(Spacer(1, 15))
    
    # Informations dans un layout sophistiqué
    invoice_info = f"""
    <font size="10" color="{self.GREY_DARK.hexval()}">
    <b>N° de devis:</b> <font color="{self.PRIMARY_COLOR.hexval()}"><b>{self.invoice_number}</b></font><br/>
    <b>Date d'émission:</b> {self.invoice_date.strftime('%d/%m/%Y')}<br/>
    """
    if self.due_date:
      invoice_info += f'<b>Date limite:</b> {self.due_date.strftime("%d/%m/%Y")}<br/>'
    
    invoice_info += '</font>'
    
    client_info = f"""
    <font size="12" color="{self.ACCENT_COLOR.hexval()}"><b>Facturé à</b></font><br/>
    <font size="11" color="{self.BLACK.hexval()}"><b>{self.client_info.name}</b></font><br/>
    <font size="10" color="{self.GREY_DARK.hexval()}">
    {self.client_info.address}<br/>
    {self.client_info.postal_code} {self.client_info.city}
    """
    if self.client_info.email:
      client_info += f'<br/><b>Email:</b> {self.client_info.email}'
    client_info += '</font>'
    
    info_data = [[
      Paragraph(invoice_info, self.styles['SophisticatedNormal']),
      Paragraph(client_info, self.styles['SophisticatedNormal'])
    ]]
    
    info_table = Table(info_data, colWidths=[85*mm, 95*mm])
    info_table.setStyle(TableStyle([
      ('ALIGN', (0, 0), (0, 0), 'LEFT'),
      ('ALIGN', (1, 0), (1, 0), 'LEFT'),
      ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      ('BACKGROUND', (0, 0), (0, 0), self.GREY_LIGHT),
      ('BACKGROUND', (1, 0), (1, 0), self.SECONDARY_COLOR),
      ('LEFTPADDING', (0, 0), (-1, -1), 15),
      ('RIGHTPADDING', (0, 0), (-1, -1), 15),
      ('TOPPADDING', (0, 0), (-1, -1), 12),
      ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
      ('ROUNDEDCORNERS', (0, 0), (-1, -1), [5, 5, 5, 5]),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 15))
    elements.append(self._create_elegant_separator())
    elements.append(Spacer(1, 12))
    
    return elements
  
  def _create_project_section(self) -> List[Any]:
    """Crée la section projet avec lorem ipsum"""
    if not self.project_info:
      return []
    
    elements = []
    
    # Titre du projet
    project_title = Paragraph(f"◆ PROJET : {self.project_info.title.upper()}", self.styles['ProjectTitle'])
    elements.append(project_title)
    elements.append(Spacer(1, 10))
    
    # Description ou lorem ipsum
    description = self.project_info.description or """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    
    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, 
    eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
    """
    
    # Encadré pour la description
    desc_data = [[Paragraph(description, self.styles['SophisticatedNormal'])]]
    desc_table = Table(desc_data, colWidths=[180*mm])
    desc_table.setStyle(TableStyle([
      ('BACKGROUND', (0, 0), (-1, -1), self.GREY_LIGHT),
      ('LEFTPADDING', (0, 0), (-1, -1), 20),
      ('RIGHTPADDING', (0, 0), (-1, -1), 20),
      ('TOPPADDING', (0, 0), (-1, -1), 15),
      ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
      ('ROUNDEDCORNERS', (0, 0), (-1, -1), [8, 8, 8, 8]),
      ('LINEBELOW', (0, 0), (-1, -1), 3, self.PRIMARY_COLOR),
    ]))
    
    elements.append(desc_table)
    elements.append(Spacer(1, 15))
    elements.append(self._create_elegant_separator())
    elements.append(Spacer(1, 12))
    
    return elements
  
  def _create_items_table(self) -> List[Any]:
    """Crée le tableau des items unifié et compact"""
    elements = []
    
    if not self.item_groups:
      return elements
    
    # Construction des données pour une seule grande table
    table_data = []
    
    # En-tête du tableau principal
    headers = ['DESCRIPTION', 'QTÉ', 'UNITÉ', 'PRIX UNITAIRE HT', 'TOTAL HT']
    table_data.append(headers)
    
    total_general = Decimal('0')
    
    for group_index, group in enumerate(self.item_groups):
      # Ligne de titre du groupe (si il y a un titre)
      if group.title:
        group_row = [group.title.upper(), '', '', '', '']
        table_data.append(group_row)
      
      # Items du groupe
      for item in group.items:
        row = [
          item.description,
          f"{item.quantity:g}",
          item.unit,
          f"{item.unit_price:.2f} €",
          f"{item.total_price:.2f} €"
        ]
        table_data.append(row)
      
      # Sous-total du groupe
      subtotal_row = ['', '', '', 'Sous-total HT:', f"{group.subtotal:.2f} €"]
      table_data.append(subtotal_row)
      
      # Ligne vide de séparation entre groupes (sauf pour le dernier)
      if group_index < len(self.item_groups) - 1:
        separator_row = ['', '', '', '', '']
        table_data.append(separator_row)
      
      total_general += group.subtotal
    
    # Total général
    total_row = ['', '', '', 'TOTAL GÉNÉRAL HT:', f"{total_general:.2f} €"]
    table_data.append(total_row)
    
    # Création de la table unifiée avec colonnes réduites
    items_table = Table(table_data, colWidths=[95*mm, 15*mm, 20*mm, 25*mm, 25*mm])
    
    # Répétition de l'en-tête si le tableau doit se couper sur plusieurs pages
    items_table.repeatRows = 1
    
    # Style unifié avec textes plus petits et cases moins hautes
    table_style = [
      # En-tête principal
      ('BACKGROUND', (0, 0), (-1, 0), self.PRIMARY_COLOR),
      ('TEXTCOLOR', (0, 0), (-1, 0), self.WHITE),
      ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
      ('FONTSIZE', (0, 0), (-1, 0), 8),  # Taille réduite
      ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
      
      # Style par défaut pour toutes les cellules
      ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
      ('FONTSIZE', (0, 1), (-1, -1), 8),  # Taille réduite
      ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
      ('ALIGN', (0, 1), (0, -1), 'LEFT'),
      
      # Réduction de la hauteur des cellules
      ('TOPPADDING', (0, 0), (-1, -1), 4),  # Padding réduit
      ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
      ('LEFTPADDING', (0, 0), (-1, -1), 8),
      ('RIGHTPADDING', (0, 0), (-1, -1), 8),
      
      # Bordures - seulement horizontales
      ('LINEBELOW', (0, 1), (-1, -1), 0.5, self.GREY_MEDIUM),  # Lignes horizontales uniquement
      ('LINEBELOW', (0, 0), (-1, 0), 2, self.ACCENT_COLOR),
      
      # CONTRAINTES DE PAGINATION - Éviter la casse après l'en-tête
      ('NOSPLIT', (0, 0), (-1, 2)),  # Garde l'en-tête + au moins 2 lignes ensemble
    ]
    
    # Application des styles spécifiques selon le type de ligne
    current_row = 1  # Commence après l'en-tête
    
    for group_index, group in enumerate(self.item_groups):
      # Style pour la ligne de titre du groupe
      if group.title:
          table_style.extend([
            ('BACKGROUND', (0, current_row), (-1, current_row), self.SECONDARY_COLOR),
            ('FONTNAME', (0, current_row), (-1, current_row), 'Times-Bold'),
            ('FONTSIZE', (0, current_row), (-1, current_row), 9),
            ('TEXTCOLOR', (0, current_row), (-1, current_row), self.ACCENT_COLOR),
            ('SPAN', (0, current_row), (4, current_row)),  # Fusion des colonnes
            ('ALIGN', (0, current_row), (-1, current_row), 'LEFT'),
            # Éviter la casse juste après un titre de groupe
            ('NOSPLIT', (0, current_row), (-1, current_row + 1)),
          ])
          current_row += 1
      
      # Style pour les items normaux avec alternance
      for item_index, item in enumerate(group.items):
        if item_index % 2 == 0:
          table_style.append(('BACKGROUND', (0, current_row), (-1, current_row), self.GREY_LIGHT))
        current_row += 1
      
      # Style pour la ligne de sous-total
      table_style.extend([
        ('BACKGROUND', (0, current_row), (-1, current_row), self.GRADIENT_START),
        ('FONTNAME', (0, current_row), (-1, current_row), 'Times-Bold'),
        ('FONTSIZE', (0, current_row), (-1, current_row), 8),
        ('ALIGN', (3, current_row), (-1, current_row), 'RIGHT'),
        ('TEXTCOLOR', (0, current_row), (-1, current_row), self.BLACK),
        # Éviter la casse juste avant un sous-total
        ('NOSPLIT', (0, current_row - 1), (-1, current_row)),
      ])
      current_row += 1
      
      # Ligne de séparation (si pas le dernier groupe)
      if group_index < len(self.item_groups) - 1:
        table_style.append(('BACKGROUND', (0, current_row), (-1, current_row), colors.white))
        current_row += 1
    
    # Style pour le total général (dernière ligne)
    table_style.extend([
      ('BACKGROUND', (0, -1), (-1, -1), self.ACCENT_COLOR),
      ('TEXTCOLOR', (0, -1), (-1, -1), self.WHITE),
      ('FONTNAME', (0, -1), (-1, -1), 'Times-Bold'),
      ('FONTSIZE', (0, -1), (-1, -1), 10),  # Légèrement plus grand pour le total
      ('ALIGN', (3, -1), (-1, -1), 'RIGHT'),
      # Éviter la casse juste avant le total général
      ('NOSPLIT', (0, -2), (-1, -1)),
    ])
    
    items_table.setStyle(TableStyle(table_style))
    
    # Utilisation de KeepTogether pour les premières lignes critiques
    table_with_constraints = KeepTogether([items_table])
    elements.append(table_with_constraints)
    elements.append(Spacer(1, 15))
    
    return elements
  
  def _create_recurring_payments_table(self) -> List[Any]:
    """Crée le tableau des frais de gestion récurrents"""
    elements = []
    
    # Titre de la section
    recurring_title = Paragraph("◆ MAINTENANCE & SUPPORT RÉCURRENTS", self.styles['ElegantSubtitle'])
    elements.append(recurring_title)
    elements.append(Spacer(1, 10))
    
    # Description introductive
    intro_text = """
    <font size="10" color="#19376D"><b>Services de maintenance et évolution continue</b></font><br/>
    <font size="9" color="#404040">
    Après la livraison du projet, nous proposons un service de maintenance incluant :<br/>
    • Surveillance et maintenance technique proactive<br/>
    • Mises à jour de sécurité et optimisations<br/>
    • Support technique prioritaire et hotline<br/>
    • Sauvegardes automatiques et monitoring<br/>
    • Évolutions mineures et améliorations continues<br/>
    • Rapports mensuels de performance et recommandations
    </font>
    """
    
    intro_data = [[Paragraph(intro_text, self.styles['SophisticatedNormal'])]]
    intro_table = Table(intro_data, colWidths=[180*mm])
    intro_table.setStyle(TableStyle([
      ('BACKGROUND', (0, 0), (-1, -1), self.GREY_LIGHT),
      ('LEFTPADDING', (0, 0), (-1, -1), 15),
      ('RIGHTPADDING', (0, 0), (-1, -1), 15),
      ('TOPPADDING', (0, 0), (-1, -1), 12),
      ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
      ('ROUNDEDCORNERS', (0, 0), (-1, -1), [5, 5, 5, 5]),
    ]))
    
    elements.append(intro_table)
    elements.append(Spacer(1, 12))
    
    # Tableau des options de maintenance
    recurring_data = []
    
    # En-têtes
    headers = ['FORMULE', 'ENGAGEMENT', 'PRIX MENSUEL', 'ÉCONOMIE', 'TOTAL']
    recurring_data.append(headers)
    
    # Option mensuelle
    monthly_row = [
      'Maintenance Essentielle',
      '1 mois',
      '450,00 €',
      '-',
      '450,00 € / mois'
    ]
    recurring_data.append(monthly_row)
    
    # Option semestrielle
    semester_row = [
      'Maintenance Premium',
      '6 mois payés d\'avance',
      '320,00 €',
      '130,00 € / mois\n(29% d\'économie)',
      '1 920,00 € / semestre'
    ]
    recurring_data.append(semester_row)
    
    # Option annuelle
    annual_row = [
      'Maintenance Enterprise',
      '12 mois payés d\'avance',
      '280,00 €',
      '170,00 € / mois\n(38% d\'économie)',
      '3 360,00 € / an'
    ]
    recurring_data.append(annual_row)
    
    # Création de la table
    recurring_table = Table(recurring_data, colWidths=[40*mm, 35*mm, 30*mm, 40*mm, 35*mm])
    
    # Répétition de l'en-tête si le tableau doit se couper sur plusieurs pages
    recurring_table.repeatRows = 1
    
    # Style du tableau
    recurring_table.setStyle(TableStyle([
      # En-tête
      ('BACKGROUND', (0, 0), (-1, 0), self.PRIMARY_COLOR),
      ('TEXTCOLOR', (0, 0), (-1, 0), self.WHITE),
      ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
      ('FONTSIZE', (0, 0), (-1, 0), 9),
      ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
      
      # Lignes de données
      ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
      ('FONTSIZE', (0, 1), (-1, -1), 8),
      ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
      ('ALIGN', (0, 1), (0, -1), 'LEFT'),
      
      # Alternance de couleurs
      ('BACKGROUND', (0, 1), (-1, 1), self.SECONDARY_COLOR),
      ('BACKGROUND', (0, 2), (-1, 2), self.GREY_LIGHT),
      ('BACKGROUND', (0, 3), (-1, 3), self.SECONDARY_COLOR),
      
      # Mise en évidence des économies
      ('TEXTCOLOR', (3, 2), (3, 2), self.PRIMARY_COLOR),
      ('FONTNAME', (3, 2), (3, 2), 'Times-Bold'),
      ('TEXTCOLOR', (3, 3), (3, 3), self.PRIMARY_COLOR),
      ('FONTNAME', (3, 3), (3, 3), 'Times-Bold'),
      
      # Padding
      ('TOPPADDING', (0, 0), (-1, -1), 6),
      ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
      ('LEFTPADDING', (0, 0), (-1, -1), 6),
      ('RIGHTPADDING', (0, 0), (-1, -1), 6),
      
      # Bordures
      ('LINEBELOW', (0, 0), (-1, 0), 2, self.ACCENT_COLOR),
      ('LINEBELOW', (0, 1), (-1, -1), 0.5, self.GREY_MEDIUM),
      ('ROUNDEDCORNERS', (0, 0), (-1, -1), [3, 3, 3, 3]),
      
      # CONTRAINTES DE PAGINATION - Éviter la casse après l'en-tête
      ('NOSPLIT', (0, 0), (-1, 2)),  # Garde l'en-tête + au moins 2 lignes ensemble
    ]))
    
    # Utilisation de KeepTogether pour éviter les coupures malheureuses
    table_with_constraints = KeepTogether([recurring_table])
    elements.append(table_with_constraints)
    elements.append(Spacer(1, 12))
    
    # Note explicative
    note_text = """
    <font size="8" color="#666666"><i>
    <b>Note :</b> Les contrats de maintenance sont optionnels et peuvent être souscrits dans les 30 jours après livraison. 
    Les formules longue durée offrent des économies substantielles et incluent des services premium. 
    Aucun frais de mise en service. Résiliation possible avec préavis de 30 jours.
    </i></font>
    """
    
    note_data = [[Paragraph(note_text, self.styles['SophisticatedNormal'])]]
    note_table = Table(note_data, colWidths=[180*mm])
    note_table.setStyle(TableStyle([
      ('BACKGROUND', (0, 0), (-1, -1), colors.Color(0.98, 0.98, 1.0)),
      ('LEFTPADDING', (0, 0), (-1, -1), 12),
      ('RIGHTPADDING', (0, 0), (-1, -1), 12),
      ('TOPPADDING', (0, 0), (-1, -1), 8),
      ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
      ('ROUNDEDCORNERS', (0, 0), (-1, -1), [3, 3, 3, 3]),
    ]))
    
    elements.append(note_table)
    elements.append(Spacer(1, 15))
    
    return elements

  def _calculate_total(self) -> Decimal:
    """Calcule le total général du devis"""
    return sum(group.subtotal for group in self.item_groups)

  def _create_stripe_payment_link(self) -> Optional[str]:
    """Crée un lien de paiement Stripe et retourne l'URL"""
    if not self.stripe_private_key:
      print("⚠️ Clé privée Stripe non configurée. Définissez STRIPE_PRIVATE_KEY.")
      return None
    
    if not self.item_groups:
      print("⚠️ Aucun item pour créer le lien de paiement.")
      return None
    
    try:
      total_amount = self._calculate_total()
      # Calcul du montant selon le pourcentage défini
      payment_amount = total_amount * Decimal(str(self.payment_percentage))
      # Stripe travaille en centimes
      amount_in_cents = int(payment_amount * 100)
      
      # Création d'un produit Stripe pour ce devis
      product = stripe.Product.create(
        name=f"Devis {self.invoice_number} ({self.payment_percentage*100:.0f}%)",
        description=f"Acompte de {self.payment_percentage*100:.0f}% pour le devis {self.invoice_number} - {self.client_info.name if self.client_info else 'Client'}",
        metadata={
          "invoice_number": self.invoice_number,
          "client_name": self.client_info.name if self.client_info else "",
          "company_name": self.company_info.name if self.company_info else "",
          "payment_percentage": str(self.payment_percentage),
          "total_amount": str(total_amount),
          "payment_amount": str(payment_amount)
        }
      )
      
      # Création du prix
      price = stripe.Price.create(
        unit_amount=amount_in_cents,
        currency="eur",
        product=product.id,
      )
      
      # Création du lien de paiement
      payment_link = stripe.PaymentLink.create(
        line_items=[{
          'price': price.id,
          'quantity': 1,
        }],
        metadata={
          "invoice_number": self.invoice_number,
          "client_email": self.client_info.email if self.client_info and self.client_info.email else "",
          "payment_percentage": str(self.payment_percentage),
        },
        allow_promotion_codes=True,
        billing_address_collection="auto",
        shipping_address_collection={
          "allowed_countries": ["FR", "BE", "CH", "LU", "MC"],
        },
        after_completion={
          "type": "hosted_confirmation",
          "hosted_confirmation": {
            "custom_message": f"Merci pour votre paiement de {self.payment_percentage*100:.0f}% du devis {self.invoice_number} ! Nous vous contacterons prochainement."
          }
        }
      )
      
      self.payment_link = payment_link.url
      print(f"✅ Lien de paiement Stripe créé : {payment_link.url}")
      print(f"💰 Montant demandé : {payment_amount:.2f}€ ({self.payment_percentage*100:.0f}% du total)")
      return payment_link.url
        
    except Exception as e:
      print(f"❌ Erreur lors de la création du lien Stripe : {e}")
      return None
  
  def _generate_qr_code(self, url: str) -> Optional[str]:
    """Génère un QR code à partir d'une URL et retourne le chemin du fichier"""
    if not url:
      return None
    
    try:
      # Configuration du QR code avec style sophistiqué
      qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
      )
      qr.add_data(url)
      qr.make(fit=True)
      
      # Création de l'image avec les couleurs de marque
      qr_image = qr.make_image(
        fill_color="#19376D",  # Couleur principale bleu marine
        back_color="white"
      )
      
      # Nom de fichier basé sur le numéro de devis ou timestamp
      if self.invoice_number:
        filename = f"qr_code_{self.invoice_number.replace('/', '_').replace('-', '_')}.png"
      else:
        from time import time
        filename = f"qr_code_{int(time())}.png"
      
      # Sauvegarde dans le dossier courant
      qr_path = os.path.join(os.getcwd(), filename)
      qr_image.save(qr_path)
      
      self.qr_code_path = qr_path
      print(f"✅ QR code généré : {qr_path}")
      return qr_path
        
    except Exception as e:
      print(f"❌ Erreur lors de la génération du QR code : {e}")
      return None
  
  def setup_stripe_payment(self) -> bool:
    """Configure le paiement Stripe avec QR code"""
    if not self.stripe_private_key:
      print("⚠️ Configuration Stripe requise. Définissez STRIPE_PRIVATE_KEY dans votre environnement.")
      return False
    
    # Création du lien de paiement
    payment_url = self._create_stripe_payment_link()
    if not payment_url:
      return False
    
    # Génération du QR code
    qr_path = self._generate_qr_code(payment_url)
    if not qr_path:
      return False
    
    print(f"🎯 Paiement Stripe configuré avec succès !")
    print(f"💳 Lien de paiement : {payment_url}")
    print(f"📱 QR code généré pour faciliter le paiement mobile")
    return True

  def _create_payment_section(self) -> List[Any]:
    """Crée la section de paiement avec QR code Stripe"""
    elements = []
    payment_section_elements = []  # Éléments à garder ensemble
    
    # Titre de la section paiement (toujours affiché)
    payment_title = Paragraph("◆ PAIEMENT SÉCURISÉ", self.styles['ElegantSubtitle'])
    payment_section_elements.append(payment_title)
    payment_section_elements.append(Spacer(1, 10))
    
    # Mode avec Stripe configuré
    if self.payment_link and self.qr_code_path:
      try:
        # QR Code
        qr_image = Image(self.qr_code_path, width=25*mm, height=25*mm, hAlign='LEFT')
        
        # Texte explicatif
        payment_text = f"""
        <font size="11" color="{self.ACCENT_COLOR.hexval()}"><b>Paiement en ligne sécurisé ({self.payment_percentage*100:.0f}% du montant total)</b></font><br/>
        <font size="9" color="{self.GREY_DARK.hexval()}">
        Scannez le QR code avec votre téléphone ou cliquez sur le lien ci-dessous pour procéder au paiement sécurisé via Stripe. 
        Il s'agit uniquement du paiement initial de {self.payment_percentage*100:.0f}% pour démarrer le projet.<br/><br/>
        
        <b>Moyens de paiement acceptés :</b><br/>
        • Cartes bancaires (Visa, Mastercard, American Express)<br/>
        • Virements SEPA<br/>
        • Apple Pay & Google Pay<br/><br/>
        
        <b>Sécurité garantie :</b> Paiement 100% sécurisé par Stripe<br/>
        <b>Confirmation :</b> Reçu automatique par email
        </font>
        """
        
        # Lien cliquable
        # Raccourcir l'affichage du lien pour une meilleure lisibilité
        display_link = self.payment_link
        if len(display_link) > 60:
            display_link = display_link[:50] + "..."
        
        link_text = f"""
        <font size="9" color="{self.PRIMARY_COLOR.hexval()}"><b>
        🌐 Lien de paiement direct (cliquable) :<br/>
        <link href="{self.payment_link}">{display_link}</link>
        </b></font>
        """
        
        # Organisation en tableau
        payment_data = [[
          qr_image,
          Paragraph(payment_text, self.styles['SophisticatedNormal'])
        ]]
        
        payment_table = Table(payment_data, colWidths=[35*mm, 145*mm])
        payment_table.setStyle(TableStyle([
          ('ALIGN', (0, 0), (0, 0), 'CENTER'),
          ('ALIGN', (1, 0), (1, 0), 'LEFT'),
          ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('BACKGROUND', (0, 0), (-1, -1), self.SECONDARY_COLOR),
          ('LEFTPADDING', (0, 0), (-1, -1), 15),
          ('RIGHTPADDING', (0, 0), (-1, -1), 15),
          ('TOPPADDING', (0, 0), (-1, -1), 15),
          ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
          ('ROUNDEDCORNERS', (0, 0), (-1, -1), [8, 8, 8, 8]),
          ('LINEABOVE', (0, 0), (-1, -1), 3, self.PRIMARY_COLOR),
        ]))
        
        payment_section_elements.append(payment_table)
        payment_section_elements.append(Spacer(1, 10))
        
        # Lien cliquable séparé (plus discret)
        link_data = [[Paragraph(link_text, self.styles['SophisticatedNormal'])]]
        link_table = Table(link_data, colWidths=[180*mm])
        link_table.setStyle(TableStyle([
          ('BACKGROUND', (0, 0), (-1, -1), self.GREY_LIGHT),
          ('LEFTPADDING', (0, 0), (-1, -1), 15),
          ('RIGHTPADDING', (0, 0), (-1, -1), 15),
          ('TOPPADDING', (0, 0), (-1, -1), 12),
          ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
          ('ROUNDEDCORNERS', (0, 0), (-1, -1), [5, 5, 5, 5]),
        ]))
        
        payment_section_elements.append(link_table)
          
      except Exception as e:
        print(f"⚠️ Erreur lors de la création de la section paiement : {e}")
        # Fallback avec section générique
        fallback_elements = self._create_payment_fallback()
        payment_section_elements.extend(fallback_elements)
    
    # Mode démo/fallback (sans Stripe configuré)
    else:
      print(f"📝 Mode démo : payment_link={bool(self.payment_link)}, qr_code={bool(self.qr_code_path)}")
      print(f"🔑 Stripe key configurée : {bool(self.stripe_private_key)}")
      fallback_elements = self._create_payment_fallback()
      payment_section_elements.extend(fallback_elements)
    
    # Encapsuler tout le bloc paiement dans KeepTogether
    elements.append(KeepTogether(payment_section_elements))
    elements.append(Spacer(1, 12))
    
    return elements
  
  def _create_payment_fallback(self) -> List[Any]:
    """Crée une section de paiement de démonstration ou fallback"""
    elements = []
    
    # QR Code de démonstration (générique)
    demo_url = "https://example.com/demo-payment"
    demo_qr_path = self._generate_qr_code(demo_url)
    
    try:
      if demo_qr_path and os.path.exists(demo_qr_path):
        qr_image = Image(demo_qr_path, width=25*mm, height=25*mm, hAlign='LEFT')
      else:
        # Placeholder si même le QR demo échoue
        qr_image = Paragraph("📱 QR", self.styles['SophisticatedNormal'])
      
      # Texte pour mode démo
      payment_text = f"""
      <font size="11" color="{self.ACCENT_COLOR.hexval()}"><b>🔒 PAIEMENT SÉCURISÉ</b></font><br/>
      <font size="9" color="{self.GREY_DARK.hexval()}">
      {'[MODE DÉMO - Configurez STRIPE_PRIVATE_KEY pour activer les paiements réels]' if not self.stripe_private_key else '[Erreur de configuration Stripe]'}<br/><br/>
      
      <b>💳 Moyens de paiement disponibles :</b><br/>
      • Cartes bancaires (Visa, Mastercard, American Express)<br/>
      • Virements SEPA & bancaires<br/>
      • Paiements mobiles (Apple Pay, Google Pay)<br/><br/>
      
      <b>🔐 Sécurité :</b> Transactions sécurisées et chiffrées<br/>
      <b>📧 Suivi :</b> Confirmation automatique par email
      </font>
      """
      
      # Organisation en tableau
      payment_data = [[
        qr_image,
        Paragraph(payment_text, self.styles['SophisticatedNormal'])
      ]]
      
      payment_table = Table(payment_data, colWidths=[35*mm, 145*mm])
      payment_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), self.SECONDARY_COLOR),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('ROUNDEDCORNERS', (0, 0), (-1, -1), [8, 8, 8, 8]),
        ('LINEABOVE', (0, 0), (-1, -1), 3, self.PRIMARY_COLOR),
      ]))
      
      elements.append(payment_table)
      elements.append(Spacer(1, 10))
      
      # Instructions de configuration
      if not self.stripe_private_key:
        config_text = f"""
        <font size="9" color="{self.PRIMARY_COLOR.hexval()}"><b>
        📋 Configuration requise :<br/>
        </b></font>
        <font size="8" color="{self.GREY_DARK.hexval()}">
        1. Créez un compte Stripe sur stripe.com<br/>
        2. Récupérez votre clé privée (sk_test_... ou sk_live_...)<br/>
        3. Copiez example.env vers .env et ajoutez votre clé<br/>
        4. Régénérez le PDF pour voir le QR code et lien actifs
        </font>
        """
        
        config_data = [[Paragraph(config_text, self.styles['SophisticatedNormal'])]]
        config_table = Table(config_data, colWidths=[180*mm])
        config_table.setStyle(TableStyle([
          ('BACKGROUND', (0, 0), (-1, -1), self.GREY_LIGHT),
          ('LEFTPADDING', (0, 0), (-1, -1), 15),
          ('RIGHTPADDING', (0, 0), (-1, -1), 15),
          ('TOPPADDING', (0, 0), (-1, -1), 12),
          ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
          ('ROUNDEDCORNERS', (0, 0), (-1, -1), [5, 5, 5, 5]),
        ]))
        
        elements.append(config_table)
      
      elements.append(Spacer(1, 20))
      
      # Note : on ne supprime plus automatiquement le QR de démo
      # car il peut être utile de le garder pour debug
                
    except Exception as e:
      print(f"⚠️ Erreur dans payment fallback : {e}")
      # Super fallback - juste du texte
      simple_text = f"""
      <font size="11" color="{self.ACCENT_COLOR.hexval()}"><b>🔒 PAIEMENT SÉCURISÉ</b></font><br/>
      <font size="10" color="{self.GREY_DARK.hexval()}">
      Section de paiement - Configurez STRIPE_PRIVATE_KEY pour activer les fonctionnalités complètes.
      </font>
      """
      elements.append(Paragraph(simple_text, self.styles['SophisticatedNormal']))
      elements.append(Spacer(1, 15))
    
    return elements
  
  def _create_rib_section(self) -> List[Any]:
    """Crée l'encart RIB sophistiqué"""
    if not (self.company_info.rib_iban or self.company_info.rib_bic):
      return []
    
    elements = []
    rib_section_elements = []  # Éléments à garder ensemble
    
    # Titre de la section RIB
    rib_title = Paragraph("◆ COORDONNÉES BANCAIRES", self.styles['ElegantSubtitle'])
    rib_section_elements.append(rib_title)
    rib_section_elements.append(Spacer(1, 8))
    
    # Contenu RIB
    rib_content = ""
    if self.company_info.rib_bank:
      rib_content += f"<b>Banque :</b> {self.company_info.rib_bank}<br/>"
    if self.company_info.rib_iban:
      rib_content += f"<b>IBAN :</b> {self.company_info.rib_iban}<br/>"
    if self.company_info.rib_bic:
      rib_content += f"<b>BIC :</b> {self.company_info.rib_bic}<br/>"
    
    rib_content += f"<br/><i>Domiciliation : {self.company_info.name}</i>"
    
    # Encadré RIB élégant
    rib_data = [[Paragraph(rib_content, self.styles['BoxedContent'])]]
    rib_table = Table(rib_data, colWidths=[180*mm])
    rib_table.setStyle(TableStyle([
      ('BACKGROUND', (0, 0), (-1, -1), self.SECONDARY_COLOR),
      ('LEFTPADDING', (0, 0), (-1, -1), 20),
      ('RIGHTPADDING', (0, 0), (-1, -1), 20),
      ('TOPPADDING', (0, 0), (-1, -1), 12),
      ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
      ('ROUNDEDCORNERS', (0, 0), (-1, -1), [8, 8, 8, 8]),
      ('LINEABOVE', (0, 0), (-1, -1), 2, self.PRIMARY_COLOR),
    ]))
    
    rib_section_elements.append(rib_table)
    
    # Encapsuler tout le bloc RIB dans KeepTogether
    elements.append(KeepTogether(rib_section_elements))
    elements.append(Spacer(1, 12))
    
    return elements
  
  def _create_footer(self) -> List[Any]:
    """Crée le pied de page sophistiqué"""
    elements = []
    
    if self.notes:
      elements.append(Spacer(1, 15))
      elements.append(self._create_elegant_separator())
      elements.append(Spacer(1, 15))
      
      # Éléments à garder ensemble (titre + début du contenu)
      footer_section_elements = []
      
      notes_title = Paragraph("◆ CONDITIONS & MENTIONS", self.styles['ElegantSubtitle'])
      footer_section_elements.append(notes_title)
      footer_section_elements.append(Spacer(1, 8))
      
      # Encadré pour les notes
      notes_data = [[Paragraph(self.notes, self.styles['SophisticatedNormal'])]]
      notes_table = Table(notes_data, colWidths=[180*mm])
      notes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), self.GREY_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('ROUNDEDCORNERS', (0, 0), (-1, -1), [5, 5, 5, 5]),
      ]))
      footer_section_elements.append(notes_table)
      
      # Encapsuler le titre et le contenu dans KeepTogether
      elements.append(KeepTogether(footer_section_elements))
    
    # Informations légales sophistiquées
    if self.company_info.siret:
      elements.append(Spacer(1, 10))  # Réduction de l'espace
      
      # Construction du texte TVA selon le statut
      if self.company_info.vat_status == "auto_entrepreneur":
        vat_text = "TVA non applicable - Article 293B du CGI"
      elif self.company_info.vat_status == "company_with_vat":
        if self.company_info.vat_number:
          vat_text = f"N° TVA intracommunautaire : {self.company_info.vat_number}"
        else:
          vat_text = "TVA en sus au taux en vigueur (20%)"
      elif self.company_info.vat_status == "company_exempt":
        vat_text = "TVA non applicable - Exonération"
      else:
        vat_text = "TVA non applicable - Article 293B du CGI"  # Fallback
      
      legal_info = f"SIRET : {self.company_info.siret} • {vat_text}"
      legal_paragraph = Paragraph(
        f'<font size="8" color="{self.GREY_MEDIUM.hexval()}"><i>{legal_info}</i></font>',
        self.styles['SophisticatedNormal']
      )
      elements.append(legal_paragraph)
      # Suppression de l'espace supplémentaire en fin de document
    
    return elements
  
  def generate_pdf(self, filename: str) -> str:
    """
    Génère le PDF du devis ultra-professionnel
    
    Args:
      filename: Nom du fichier PDF à créer
        
    Returns:
      Chemin vers le fichier créé
    """
    if not self.company_info or not self.client_info:
      raise ValueError("Les informations de l'entreprise et du client doivent être définies")
    
    if not self.item_groups:
      raise ValueError("Au moins un groupe d'items doit être ajouté")
    
    # Configuration automatique du paiement Stripe si la clé est disponible
    if self.stripe_private_key and not self.payment_link:
      print("🔄 Configuration automatique du paiement Stripe...")
      self.setup_stripe_payment()
    
    # Utilisation du template personnalisé avec texte en marge
    doc = InvoiceTemplate(
      filename,
      invoice_number=self.invoice_number,
      pagesize=A4,
      leftMargin=self.margin_left,
      rightMargin=self.margin_right,
      topMargin=self.margin_top,
      bottomMargin=self.margin_bottom,
      title=f"Devis Professionnel {self.invoice_number}",
      author=self.company_info.name,
      subject=f"Devis {self.invoice_number} - {self.client_info.name}",
      creator="Template Devis Ultra-Professionnel"
    )
    
    # Construction du document sophistiqué
    story = []
    
    # En-tête sophistiqué
    story.extend(self._create_header())
    
    # Titre et informations
    story.extend(self._create_invoice_title_and_info())
    
    # Section projet avec lorem ipsum
    story.extend(self._create_project_section())
    
    # Tableau des items ultra-stylé
    story.extend(self._create_items_table())
    
    # Tableau des frais de gestion récurrents
    story.extend(self._create_recurring_payments_table())
    
    # Section paiement avec QR code
    story.extend(self._create_payment_section())
    
    # Section RIB
    story.extend(self._create_rib_section())
    
    # Pied de page sophistiqué
    story.extend(self._create_footer())
    
    # Génération du PDF
    doc.build(story)
    
    # Nettoyage sélectif des fichiers QR code temporaires
    if self.qr_code_path and os.path.exists(self.qr_code_path):
      # On ne supprime que si c'est un QR code de paiement réel (avec payment_link)
      if self.payment_link and "example.com" not in self.payment_link:
        try:
          os.unlink(self.qr_code_path)
          print("🧹 Fichier QR code temporaire supprimé")
        except:
          pass
      else:
        print(f"📄 QR code de démo conservé : {self.qr_code_path}")
    
    return os.path.abspath(filename)