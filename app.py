import sys
import pygame

# Initialisation de Pygame
pygame.init()

# Dimensions du Launcher
LARGEUR, HAUTEUR = 1200, 700
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("ULC 27 Launcher - L&B Studio")

HORLOGE = pygame.time.Clock()
FPS = 60

# --- COULEURS ---
BG_DARK = (14, 18, 28)
PANEL_BG = (22, 28, 42)
OR_FM = (242, 201, 76)
BLANC = (255, 255, 255)
GRIS_TEXTE = (160, 175, 200)

# --- POLICES SÉCURISÉES ---
police_titre = pygame.font.SysFont(None, 24)
police_texte = pygame.font.SysFont(None, 18)

# --- BOUCLE PRINCIPALE DU LAUNCHER ---
en_cours = True
while en_cours:
  HORLOGE.tick(FPS)
  souris_pos = pygame.mouse.get_pos()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      en_cours = False

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      # Bouton Quitter
      rect_quitter = pygame.Rect(20, HAUTEUR - 50, 120, 35)
      if rect_quitter.collidepoint(souris_pos):
        en_cours = False

  # --- RENDU GRAPHIQUE ---
  ecran.fill(BG_DARK)

  # En-tête
  pygame.draw.rect(ecran, PANEL_BG, (0, 0, LARGEUR, 60))
  txt_logo = police_titre.render("ULC 27 // MANAGER PORTAL", True, OR_FM)
  ecran.blit(txt_logo, (20, 20))

  # Panneau central d'information
  pygame.draw.rect(ecran, PANEL_BG, (50, 100, 500, 500), border_radius=8)
  txt_titre_panel = police_titre.render(
      "Statut du serveur : Hors-ligne", True, BLANC
  )
  ecran.blit(txt_titre_panel, (70, 120))

  txt_desc = police_texte.render(
      "Prêt pour la configuration d'Oracle Cloud !", True, GRIS_TEXTE
  )
  ecran.blit(txt_desc, (70, 160))

  # Bouton Quitter
  rect_quitter = pygame.Rect(20, HAUTEUR - 50, 120, 35)
  pygame.draw.rect(ecran, (180, 50, 50), rect_quitter, border_radius=6)
  ecran.blit(police_texte.render("Quitter", True, BLANC), (rect_quitter.x + 35, rect_quitter.y + 10))

  pygame.display.flip()

pygame.quit()
sys.exit()