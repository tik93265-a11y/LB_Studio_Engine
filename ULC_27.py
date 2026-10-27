import sys
import math
import pygame

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1280, 720
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("ULC 27 // LB 3D Engine (L&B Studio)")

HORLOGE = pygame.time.Clock()

# --- COULEURS ---
BLEU_FOND = (10, 14, 26)
BLEU_PANEL = (20, 30, 50)
BLEU_CLAIR_PANEL = (30, 45, 75)
OR_LB = (242, 201, 76)
BLANC = (255, 255, 255)
VERT_CUBE = (35, 120, 60)
GRIS_TEXTE = (150, 165, 190)
ROUGE_SUAREZ = (220, 40, 40)

# --- POLICES ---
police_titre = pygame.font.SysFont("Arial", 32, bold=True)
police_grand = pygame.font.SysFont("Arial", 50, bold=True)
police_texte = pygame.font.SysFont("Arial", 20)
police_fps = pygame.font.SysFont("Consolas", 18, bold=True)

# --- ÉTATS DU JEU ---
ETAT_MENU = 1
ETAT_MODES = 2
ETAT_MATCH_3D = 3
ETAT_OPTIONS = 4
ETAT_PAUSE = 5
ETAT_EASTER_EGG = 6
etat_actuel = ETAT_MENU

# --- OPTIONS DU MENU PRINCIPAL ---
options_menu = ["JOUER (MODES DE JEU)", "OPTIONS", "QUITTER"]
index_option = 0

# --- MODES DE JEU ---
modes_jeu = [
    "COUP D'ENVOI (FC 27)",
    "INTERNATIONAL CUP",
    "WORLD CUP",
    "CLUB WORLD CUP",
    "LIGUES NATIONALES",
    "RETOUR AU MENU"
]
index_mode = 0

# --- OPTIONS DU MENU PAUSE ---
options_pause = [
    "REPRENDRE LE MATCH",
    "PARAMÈTRES DU MATCH",
    "RECOMMENCER",
    "QUITTER AU MENU PRINCIPAL"
]
index_pause = 0

# --- OPTIONS DU SYSTÈME (FPS et Plein Écran) ---
fps_limite = 60  # Peut passer à 30 ou 60
options_parametres = ["FPS : 60", "PLEIN ÉCRAN : OFF", "RETOUR"]
index_param = 0
plein_ecran = False

# --- VARIABLES EASTER EGG (SUÁREZ GUITARE) ---
clics_logo_ulc = 0

# --- CONFIGURATION DU MOTEUR LB 3D (Cube optimisé) ---
points_3d = [
    [-100, -100, -100],  # 0
    [100, -100, -100],   # 1
    [100, 100, -100],    # 2
    [-100, 100, -100],   # 3
    [-100, -100, 100],   # 4
    [100, -100, 100],    # 5
    [100, 100, 100],     # 6
    [-100, 100, 100],    # 7
]

faces = [
    (0, 1, 2, 3),  # Arrière
    (4, 5, 6, 7),  # Avant
    (0, 4, 7, 3),  # Gauche
    (1, 5, 6, 2),  # Droite
    (0, 1, 5, 4),  # Dessus
    (3, 2, 6, 7)   # Dessous
]

angle_x, angle_y = 0, 0
score_dom, score_ext = 0, 0

# --- BOUCLE PRINCIPALE ---
en_cours = True
while en_cours:
    HORLOGE.tick(fps_limite)
    souris_pos = pygame.mouse.get_pos()

    # 1. GESTION DES ÉVÉNEMENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
            
        # --- CLICS SOURIS ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            # --- EASTER EGG : Logo ULC ---
            rect_logo_ulc = pygame.Rect(95, 210, 350, 60)
            if etat_actuel == ETAT_MENU and rect_logo_ulc.collidepoint(souris_pos):
                clics_logo_ulc += 1
                if clics_logo_ulc >= 5:
                    clics_logo_ulc = 0
                    etat_actuel = ETAT_EASTER_EGG

            if etat_actuel == ETAT_MENU:
                for i, option in enumerate(options_menu):
                    y_pos = 320 + (i * 75)
                    rect_bouton = pygame.Rect(100, y_pos, 450, 60)
                    if rect_bouton.collidepoint(souris_pos):
                        index_option = i
                        if index_option == 0:
                            etat_actuel = ETAT_MODES
                        elif index_option == 1:
                            etat_actuel = ETAT_OPTIONS
                        elif index_option == 2:
                            en_cours = False

            elif etat_actuel == ETAT_MODES:
                for i, mode in enumerate(modes_jeu):
                    y_pos = 180 + (i * 75)
                    rect_mode = pygame.Rect(100, y_pos, 550, 60)
                    if rect_mode.collidepoint(souris_pos):
                        index_mode = i
                        if i == len(modes_jeu) - 1:
                            etat_actuel = ETAT_MENU
                        else:
                            score_dom, score_ext = 0, 0
                            etat_actuel = ETAT_MATCH_3D

            elif etat_actuel == ETAT_OPTIONS:
                for i, opt in enumerate(options_parametres):
                    y_pos = 280 + (i * 70)
                    rect_opt = pygame.Rect(100, y_pos, 500, 55)
                    if rect_opt.collidepoint(souris_pos):
                        index_param = i
                        if i == 0:  # Changement FPS (30 ou 60)
                            if fps_limite == 60:
                                fps_limite = 30
                                options_parametres[0] = "FPS : 30"
                            else:
                                fps_limite = 60
                                options_parametres[0] = "FPS : 60"
                        elif i == 1:  # Plein écran
                            plein_ecran = not plein_ecran
                            if plein_ecran:
                                ecran = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.FULLSCREEN | pygame.SCALED)
                                options_parametres[1] = "PLEIN ÉCRAN : ON"
                            else:
                                ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
                                options_parametres[1] = "PLEIN ÉCRAN : OFF"
                        elif i == 2:
                            etat_actuel = ETAT_MENU

            elif etat_actuel == ETAT_PAUSE:
                for i, opt_pause in enumerate(options_pause):
                    y_pos = 280 + (i * 75)
                    rect_pause_opt = pygame.Rect(LARGEUR // 2 - 250, y_pos, 500, 60)
                    if rect_pause_opt.collidepoint(souris_pos):
                        index_pause = i
                        if i == 0:
                            etat_actuel = ETAT_MATCH_3D
                        elif i == 2:
                            score_dom, score_ext = 0, 0
                            etat_actuel = ETAT_MATCH_3D
                        elif i == 3:
                            etat_actuel = ETAT_MENU

            elif etat_actuel == ETAT_EASTER_EGG:
                etat_actuel = ETAT_MENU

        # --- CLAVIER ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if etat_actuel == ETAT_MATCH_3D:
                    etat_actuel = ETAT_PAUSE
                elif etat_actuel == ETAT_PAUSE:
                    etat_actuel = ETAT_MATCH_3D
                elif etat_actuel in [ETAT_MODES, ETAT_OPTIONS, ETAT_EASTER_EGG]:
                    etat_actuel = ETAT_MENU
                else:
                    en_cours = False

            if etat_actuel == ETAT_MENU:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    index_option = (index_option + 1) % len(options_menu)
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    index_option = (index_option - 1) % len(options_menu)
                if event.key == pygame.K_RETURN:
                    if index_option == 0:
                        etat_actuel = ETAT_MODES
                    elif index_option == 1:
                        etat_actuel = ETAT_OPTIONS
                    elif index_option == 2:
                        en_cours = False

            elif etat_actuel == ETAT_MODES:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    index_mode = (index_mode + 1) % len(modes_jeu)
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    index_mode = (index_mode - 1) % len(modes_jeu)
                if event.key == pygame.K_RETURN:
                    if index_mode == len(modes_jeu) - 1:
                        etat_actuel = ETAT_MENU
                    else:
                        score_dom, score_ext = 0, 0
                        etat_actuel = ETAT_MATCH_3D

            elif etat_actuel == ETAT_PAUSE:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    index_pause = (index_pause + 1) % len(options_pause)
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    index_pause = (index_pause - 1) % len(options_pause)
                if event.key == pygame.K_RETURN:
                    if index_pause == 0:
                        etat_actuel = ETAT_MATCH_3D
                    elif index_pause == 2:
                        score_dom, score_ext = 0, 0
                        etat_actuel = ETAT_MATCH_3D
                    elif index_pause == 3:
                        etat_actuel = ETAT_MENU

            elif etat_actuel == ETAT_EASTER_EGG:
                etat_actuel = ETAT_MENU

            elif etat_actuel == ETAT_OPTIONS:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    index_param = (index_param + 1) % len(options_parametres)
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    index_param = (index_param - 1) % len(options_parametres)
                if event.key == pygame.K_RETURN:
                    if index_param == 0:
                        if fps_limite == 60:
                            fps_limite = 30
                            options_parametres[0] = "FPS : 30"
                        else:
                            fps_limite = 60
                            options_parametres[0] = "FPS : 60"
                    elif index_param == 1:
                        plein_ecran = not plein_ecran
                        if plein_ecran:
                            ecran = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.FULLSCREEN | pygame.SCALED)
                            options_parametres[1] = "PLEIN ÉCRAN : ON"
                        else:
                            ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
                            options_parametres[1] = "PLEIN ÉCRAN : OFF"
                    elif index_param == 2:
                        etat_actuel = ETAT_MENU

            elif etat_actuel == ETAT_MATCH_3D:
                if event.key == pygame.K_SPACE:
                    score_dom += 1

    # 2. LOGIQUE MOTEUR 3D
    if etat_actuel == ETAT_MATCH_3D:
        angle_x += 0.02
        angle_y += 0.025
        points_2d = []
        for point in points_3d:
            x, y, z = point
            cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
            x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y
            cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
            y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
            z += 450
            focal = 500
            if z != 0:
                proj_x = int(LARGEUR / 2 + (x * focal) / z)
                proj_y = int((HAUTEUR / 2) + (y * focal) / z)
                points_2d.append((proj_x, proj_y))
            else:
                points_2d.append((0, 0))

    # ==========================================
    # 3. AFFICHAGE
    # ==========================================
    ecran.fill(BLEU_FOND)

    # --- MENU PRINCIPAL ---
    if etat_actuel == ETAT_MENU:
        titre_studio = police_texte.render("L&B STUDIO PRESENTE", True, OR_LB)
        ecran.blit(titre_studio, (100, 180))

        titre_jeu = police_grand.render("ULC 27 // LB 3D", True, BLANC)
        ecran.blit(titre_jeu, (100, 215))

        indice_ee = police_texte.render("(Clique 5 fois sur le titre...)", True, (80, 95, 120))
        ecran.blit(indice_ee, (420, 230))

        for i, option in enumerate(options_menu):
            y_pos = 320 + (i * 75)
            rect_bouton = pygame.Rect(100, y_pos, 450, 60)
            survol = rect_bouton.collidepoint(souris_pos)
            is_selected = (i == index_option) or survol
            
            couleur_fond = BLEU_PANEL if not is_selected else OR_LB
            couleur_texte = BLANC if not is_selected else BLEU_FOND
            
            pygame.draw.rect(ecran, couleur_fond, rect_bouton, border_radius=8)
            if is_selected:
                pygame.draw.rect(ecran, BLANC, rect_bouton, 2, border_radius=8)
                
            txt_opt = police_titre.render(option, True, couleur_texte)
            ecran.blit(txt_opt, (130, y_pos + 14))

        aide = police_texte.render("[ Souris / Clavier ] Naviguer | [ Clic / Entrée ] Valider", True, GRIS_TEXTE)
        ecran.blit(aide, (100, HAUTEUR - 60))

    # --- SÉLECTION DES MODES DE JEU ---
    elif etat_actuel == ETAT_MODES:
        titre_m = police_grand.render("CHOISIR UN MODE DE JEU", True, BLANC)
        ecran.blit(titre_m, (100, 80))

        for i, mode in enumerate(modes_jeu):
            y_pos = 180 + (i * 75)
            rect_mode = pygame.Rect(100, y_pos, 550, 60)
            survol = rect_mode.collidepoint(souris_pos)
            is_selected = (i == index_mode) or survol

            c_fond = BLEU_PANEL if not is_selected else OR_LB
            c_txt = BLANC if not is_selected else BLEU_FOND

            pygame.draw.rect(ecran, c_fond, rect_mode, border_radius=8)
            if is_selected:
                pygame.draw.rect(ecran, BLANC, rect_mode, 2, border_radius=8)

            txt_mod = police_titre.render(mode, True, c_txt)
            ecran.blit(txt_mod, (130, y_pos + 14))

        aide_modes = police_texte.render("[ Z / S ] Naviguer | [ ENTRÉE / Clic ] Sélectionner", True, GRIS_TEXTE)
        ecran.blit(aide_modes, (100, HAUTEUR - 60))

    # --- MATCH / MOTEUR 3D (Style FC 27 Épuré) ---
    elif etat_actuel == ETAT_MATCH_3D:
        pygame.draw.rect(ecran, BLEU_PANEL, (0, 0, LARGEUR, 70))
        pygame.draw.line(ecran, OR_LB, (0, 70), (LARGEUR, 70), 3)

        # Mode de jeu affiché proprement à gauche
        txt_titre = police_titre.render(f"FC 27 // {modes_jeu[index_mode]}", True, BLANC)
        ecran.blit(txt_titre, (30, 18))

        # Score style FC 27 épuré (Home vs Away) sans texte parasite
        score_box_w, score_box_h = 220, 44
        score_box_x = LARGEUR // 2 - score_box_w // 2
        score_box_y = 13
        pygame.draw.rect(ecran, (15, 22, 38), (score_box_x, score_box_y, score_box_w, score_box_h), border_radius=6)
        pygame.draw.rect(ecran, OR_LB, (score_box_x, score_box_y, score_box_w, score_box_h), 2, border_radius=6)
        
        txt_score = police_titre.render(f"HOM {score_dom} - {score_ext} AWY", True, OR_LB)
        ecran.blit(txt_score, (score_box_x + 22, score_box_y + 5))

        # Compteur FPS discret
        fps_actuels = int(HORLOGE.get_fps())
        txt_fps = police_fps.render(f"FPS: {fps_actuels}", True, (50, 255, 50))
        ecran.blit(txt_fps, (LARGEUR - 130, 24))

        for face in faces:
            pts_face = [points_2d[i] for i in face]
            pygame.draw.polygon(ecran, VERT_CUBE, pts_face)
            pygame.draw.polygon(ecran, OR_LB, pts_face, 2)

        pygame.draw.rect(ecran, BLEU_PANEL, (0, HAUTEUR - 60, LARGEUR, 60))
        txt_hud = police_texte.render("[ ESPACE ] Marquer un but | [ ÉCHAP ] Menu Pause", True, BLANC)
        ecran.blit(txt_hud, (30, HAUTEUR - 40))

    # --- MENU OPTIONS ---
    elif etat_actuel == ETAT_OPTIONS:
        titre_opt = police_grand.render("OPTIONS DU SYSTÈME", True, BLANC)
        ecran.blit(titre_opt, (100, 100))

        for i, opt in enumerate(options_parametres):
            y_pos = 280 + (i * 70)
            rect_opt = pygame.Rect(100, y_pos, 500, 55)
            survol = rect_opt.collidepoint(souris_pos)
            is_selected = (i == index_param) or survol

            c_fond = BLEU_PANEL if not is_selected else OR_LB
            c_txt = BLANC if not is_selected else BLEU_FOND

            pygame.draw.rect(ecran, c_fond, rect_opt, border_radius=8)
            if is_selected:
                pygame.draw.rect(ecran, BLANC, rect_opt, 2, border_radius=8)

            txt_o = police_titre.render(opt, True, c_txt)
            ecran.blit(txt_o, (rect_opt.x + 20, rect_opt.y + 10))

        aide_opt = police_texte.render("[ Z / S ] Naviguer | [ ENTRÉE / Clic ] Modifier", True, GRIS_TEXTE)
        ecran.blit(aide_opt, (100, HAUTEUR - 60))

    # --- EASTER EGG : LOUIS SUÁREZ GUITAR HERO ---
    elif etat_actuel == ETAT_EASTER_EGG:
        ecran.fill((30, 10, 25))

        txt_ee_titre = police_grand.render("🎸 SECRET DÉBLOQUÉ : LOUIS SUÁREZ ACOUSTIC TOUR 🎸", True, OR_LB)
        ecran.blit(txt_ee_titre, (LARGEUR // 2 - txt_ee_titre.get_width() // 2, 80))

        pygame.draw.circle(ecran, (245, 205, 175), (LARGEUR // 2, 260), 65)
        pygame.draw.circle(ecran, (30, 20, 10), (LARGEUR // 2, 235), 60)
        pygame.draw.rect(ecran, ROUGE_SUAREZ, (LARGEUR // 2 - 90, 325, 180, 220), border_radius=15)
        pygame.draw.ellipse(ecran, (180, 120, 60), (LARGEUR // 2 - 140, 380, 140, 180))
        pygame.draw.rect(ecran, (130, 80, 30), (LARGEUR // 2 - 80, 290, 20, 140))

        txt_note1 = police_titre.render("♪", True, OR_LB)
        txt_note2 = police_titre.render("♫", True, BLANC)
        txt_note3 = police_titre.render("♪", True, OR_LB)
        ecran.blit(txt_note1, (LARGEUR // 2 - 200, 200))
        ecran.blit(txt_note2, (LARGEUR // 2 + 180, 250))
        ecran.blit(txt_note3, (LARGEUR // 2 + 220, 150))

        txt_desc = police_titre.render("« El Pistolero a laissé tomber ses crampons pour un concert rock ! »", True, BLANC)
        ecran.blit(txt_desc, (LARGEUR // 2 - txt_desc.get_width() // 2, 590))

        txt_quitter_ee = police_texte.render("[ Clique ou appuie sur une touche pour revenir au menu ]", True, GRIS_TEXTE)
        ecran.blit(txt_quitter_ee, (LARGEUR // 2 - txt_quitter_ee.get_width() // 2, 650))

    # --- MENU PAUSE ---
    elif etat_actuel == ETAT_PAUSE:
        s = pygame.Surface((LARGEUR, HAUTEUR))
        s.set_alpha(200)
        s.fill((5, 8, 15))
        ecran.blit(s, (0, 0))

        pause_w, pause_h = 600, 420
        pause_x, pause_y = (LARGEUR - pause_w) // 2, (HAUTEUR - pause_h) // 2
        
        pygame.draw.rect(ecran, BLEU_PANEL, (pause_x, pause_y, pause_w, pause_h), border_radius=12)
        pygame.draw.rect(ecran, OR_LB, (pause_x, pause_y, pause_w, pause_h), 3, border_radius=12)

        txt_p = police_grand.render("PAUSE DU MATCH", True, BLANC)
        ecran.blit(txt_p, (pause_x + 30, pause_y + 25))
        
        txt_mode_actuel = police_texte.render(modes_jeu[index_mode], True, OR_LB)
        ecran.blit(txt_mode_actuel, (pause_x + 30, pause_y + 80))

        for i, opt_pause in enumerate(options_pause):
            y_pos = pause_y + 130 + (i * 65)
            rect_opt = pygame.Rect(pause_x + 30, y_pos, pause_w - 60, 50)
            survol = rect_opt.collidepoint(souris_pos)
            is_selected = (i == index_pause) or survol

            c_fond = BLEU_CLAIR_PANEL if not is_selected else OR_LB
            c_txt = BLANC if not is_selected else BLEU_FOND

            pygame.draw.rect(ecran, c_fond, rect_opt, border_radius=8)
            if is_selected:
                pygame.draw.rect(ecran, BLANC, rect_opt, 2, border_radius=8)

            txt_o = police_titre.render(opt_pause, True, c_txt)
            ecran.blit(txt_o, (rect_opt.x + 20, rect_opt.y + 10))

    pygame.display.flip()

pygame.quit()
sys.exit()