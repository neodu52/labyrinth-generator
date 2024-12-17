# labyrinthe.py
import random
import time

def creer_grille(x, y):
    """Créer une grille pleine de murs (1)."""
    return [[1 for _ in range(x)] for _ in range(y)]

def generer_labyrinthe_parfait(grille, x, y, progress_callback=None):
    """Génère un labyrinthe parfait avec une callback pour le suivi de progression."""
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    grille[y][x] = 0
    pile = [(x, y)]
    total_cases = len(grille) * len(grille[0])
    cases_visitees = 1

    while pile:
        cx, cy = pile[-1]
        voisins = [(cx + dx, cy + dy, dx // 2, dy // 2) for dx, dy in directions
                   if 0 <= cx + dx < len(grille[0]) and 0 <= cy + dy < len(grille) and grille[cy + dy][cx + dx] == 1]
        
        if voisins:
            nx, ny, wall_x, wall_y = random.choice(voisins)
            grille[cy + wall_y][cx + wall_x] = 0
            grille[ny][nx] = 0
            pile.append((nx, ny))
            cases_visitees += 1
        else:
            pile.pop()

        # Calcul du pourcentage de progression
        if progress_callback:
            pourcentage = int((cases_visitees / total_cases) * 100 * 6.25)
            progress_callback(pourcentage)  # Mettre à jour la progression

    return grille

def sauvegarder_labyrinthe(grille, fichier):
    """Sauvegarde le labyrinthe dans un fichier texte avec ses dimensions."""
    x = len(grille[0])
    y = len(grille)
    with open(fichier, 'w') as f:
        f.write(f"{x} {y}\n")
        for ligne in grille:
            f.write("".join(str(cell) for cell in ligne) + "\n")