import pygame

# Paramètres de couleur
COULEUR_MUR = (0, 255, 0)
COULEUR_CHEMIN = (0, 0, 0)
COULEUR_DEPART = (255, 0, 0)
COULEUR_ARRIVEE = (0, 0, 255)

# Paramètres de taille de la case
TAILLE_CASE_MAX = 50  # Taille maximale d'une case (en pixels)
TAILLE_CASE_MIN = 2   # Taille minimale d'une case (en pixels)

def afficher_labyrinthe(labyrinthe, x, y):
    pygame.init()

    # Obtenir la résolution de l'écran
    info_ecran = pygame.display.Info()
    largeur_ecran, hauteur_ecran = info_ecran.current_w, info_ecran.current_h

    # Calculer la taille de case dynamique
    taille_case = min(
        max(largeur_ecran // x, hauteur_ecran // y, TAILLE_CASE_MIN), 
        TAILLE_CASE_MAX
    )

    # Calculer la taille de la fenêtre en fonction de la taille de l'écran
    largeur_fenetre = min(x * taille_case, largeur_ecran)
    hauteur_fenetre = min(y * taille_case, hauteur_ecran)

    # Créer la fenêtre avec des dimensions ajustées
    fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
    pygame.display.set_caption("Labyrinthe")

    # Variables pour suivre la portion affichée
    offset_x, offset_y = 0, 0
    scrolling_speed = taille_case * 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Défilement avec les touches du clavier
                if event.key == pygame.K_LEFT:
                    offset_x = max(0, offset_x - scrolling_speed)
                elif event.key == pygame.K_RIGHT:
                    offset_x = min(x - largeur_fenetre // taille_case, offset_x + scrolling_speed)
                elif event.key == pygame.K_UP:
                    offset_y = max(0, offset_y - scrolling_speed)
                elif event.key == pygame.K_DOWN:
                    offset_y = min(y - hauteur_fenetre // taille_case, offset_y + scrolling_speed)

        fenetre.fill(COULEUR_CHEMIN)

        # Dessiner une portion du labyrinthe
        for yi in range(offset_y, min(offset_y + hauteur_fenetre // taille_case, y)):
            for xi in range(offset_x, min(offset_x + largeur_fenetre // taille_case, x)):
                case = labyrinthe[yi][xi]
                if case == '1':  # Mur
                    couleur = COULEUR_MUR
                elif case == 'D':  # Départ
                    couleur = COULEUR_DEPART
                elif case == 'A':  # Arrivée
                    couleur = COULEUR_ARRIVEE
                else:
                    continue

                pygame.draw.rect(
                    fenetre,
                    couleur,
                    (int((xi - offset_x) * taille_case), int((yi - offset_y) * taille_case), taille_case, taille_case)
                )

        pygame.display.flip()

    pygame.quit()

def charger_labyrinthe(fichier):
    with open(fichier, 'r') as f:
        dimensions = f.readline().strip()
        x, y = map(int, dimensions.split())
        labyrinthe = [list(f.readline().strip()) for _ in range(y)]
    return labyrinthe, x, y

def afficher_labyrinthe_process(fichier_labyrinthe):
    labyrinthe, x, y = charger_labyrinthe(fichier_labyrinthe)
    afficher_labyrinthe(labyrinthe, x, y)
