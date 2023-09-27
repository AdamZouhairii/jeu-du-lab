import pygame
import sys
import pygame.font
# Adam.z et Rawad
# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu du Labyrinthe")

# Définition des couleurs
rouge = (255, 0, 0)
noir = (0, 0, 0)
blanc = (255, 255, 255)
bleu = (0, 0, 150)


# Classe du joueur
class Joueur(pygame.sprite.Sprite):
    def __init__(self, x=560, y=410):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(rouge)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vitesse = 3



# Classe du labyrinthe
class Labyrinthe:
    def __init__(self):
        self.grille = [
            "XXXXXXXXXXXXXXVXXXX",
            "X     X           X",
            "X XXXXX XXXXXXX XXX",
            "X X O X       XXXXX",
            "X X XXX XXXXX XXXXX",
            "X X X     O  P    X",
            "X X XXXXXXX   XXXXX",
            "X X         X     X",
            "X XXXXXXXXX XXXXX X",
            "X                 X",
            "XXXXXXXXXXXXXXDXXXX",
        ]



# Fonction pour afficher le labyrinthe
def afficher_labyrinthe(labyrinthe, fenetre):
    for ligne, row in enumerate(labyrinthe.grille):
        for col, case in enumerate(row):
            if case == "X":
                pygame.draw.rect(fenetre, bleu, (col * 40, ligne * 40, 40, 40))
            elif case == " ":
                pygame.draw.rect(fenetre, blanc, (col * 40, ligne * 40, 40, 40))
            elif case == "V":
                pygame.draw.rect(fenetre, rouge, (col * 40, ligne * 40, 40, 40))
            elif case == "O":
                pygame.draw.rect(fenetre, bleu, (col * 40, ligne * 40, 40, 40))
            elif case == "P":
                pygame.draw.rect(fenetre, blanc, (col * 40, ligne * 40, 40, 40))



# Fonction pour détecter la collision avec les murs
def collision_avec_murs(joueur_temp_rect, labyrinthe):
    for ligne, row in enumerate(labyrinthe.grille):
        for col, case in enumerate(row):
            if case == "X":
                mur_rect = pygame.Rect(col * 40, ligne * 40, 40, 40)
                if joueur_temp_rect.colliderect(mur_rect):
                    return True
    return False

def collision_avec_piege(joueur_rect, labyrinthe):
    for ligne, row in enumerate(labyrinthe.grille):
        for col, case in enumerate(row):
            if case == "P":
                piege_rect = pygame.Rect(col * 40, ligne * 40, 40, 40)
                if joueur_rect.colliderect(piege_rect):
                    return True
    return False


# Fonction pour détecter la victoire
def victoire(joueur_rect, labyrinthe):
    for ligne, row in enumerate(labyrinthe.grille):
        for col, case in enumerate(row):
            if case == "V":
                victoire_rect = pygame.Rect(col * 40, ligne * 40, 40, 40)
                if joueur_rect.colliderect(victoire_rect):
                    return True
    return False



# Fonction pour afficher un message de victoire
def afficher_message_victoire(fenetre):
    font = pygame.font.Font(None, 36)
    text = font.render("Victoire !", True, (230, 230, 230))
    fenetre.blit(text, (300, 250))


# Fonction pour résoudre le labyrinthe
def resoudre_labyrinthe(labyrinthe, joueur_rect):
    def dfs(x, y):
        if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]) or grid[x][y] == "X" or grid[x][y] == "P":
            return False
        if grid[x][y] == "V":
            return True
        grid[x][y] = "P"  

       
        if dfs(x - 1, y) or dfs(x + 1, y) or dfs(x, y - 1) or dfs(x, y + 1):
            return True

        return False

   
    grid = [list(row) for row in labyrinthe.grille]

    x = joueur_rect.y // 40
    y = joueur_rect.x // 40

    if dfs(x, y):
        for i in range(len(labyrinthe.grille)):
            for j in range(len(labyrinthe.grille[i])):
                if grid[i][j] == "P":
                    grid[i][j] = 'b'

    for i in range(len(labyrinthe.grille)):
        labyrinthe.grille[i] = "".join(grid[i])


# Fonction pour afficher "Perdu !"
def afficher_message_perdu(fenetre):
    font = pygame.font.Font(None, 36)
    text = font.render("Perdu !", True, (230, 0, 0))  # Couleur rouge pour "Perdu !"
    fenetre.blit(text, (300, 250))

# Fonction principale du jeu
def main():
    labyrinthe = Labyrinthe()
    joueur = Joueur()
    victoire_affichee = False
    game_over_affiche = False
    victoire_timer = None
    game_over_timer = None

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        touches = pygame.key.get_pressed()
        joueur_x, joueur_y = joueur.rect.x, joueur.rect.y

        if touches[pygame.K_LEFT]:
            joueur_x -= joueur.vitesse
        if touches[pygame.K_RIGHT]:
            joueur_x += joueur.vitesse
        if touches[pygame.K_UP]:
            joueur_y -= joueur.vitesse
        if touches[pygame.K_DOWN]:
            joueur_y += joueur.vitesse

        joueur_temp_rect = joueur.rect.copy()
        joueur_temp_rect.x = joueur_x
        joueur_temp_rect.y = joueur_y

        if collision_avec_piege(joueur_temp_rect, labyrinthe):
        # Le joueur a marché sur le piège, afficher "Perdu !" et redémarrer le jeu
            game_over_affiche = True
            game_over_timer = pygame.time.get_ticks()
            joueur.rect.x = 560
            joueur.rect.y = 410

        elif not collision_avec_murs(joueur_temp_rect, labyrinthe):
            joueur.rect = joueur_temp_rect
        else:
            # Le joueur a touché un mur, afficher "Perdu !" et redémarrer le jeu
            game_over_affiche = True
            game_over_timer = pygame.time.get_ticks()
            joueur.rect.x = 560
            joueur.rect.y = 410

        fenetre.fill((0, 0, 0))
        afficher_labyrinthe(labyrinthe, fenetre)
        fenetre.blit(joueur.image, joueur.rect)

        if victoire(joueur.rect, labyrinthe) and not victoire_affichee:
            victoire_affichee = True
            victoire_timer = pygame.time.get_ticks()

        if victoire_affichee:
            if pygame.time.get_ticks() - victoire_timer >= 1000:
                pygame.quit()
                sys.exit()
            else:
                afficher_message_victoire(fenetre)

        if game_over_affiche:
            if pygame.time.get_ticks() - game_over_timer >= 500:
                # Redémarrer le jeu après 1 seconde
                game_over_affiche = False
                joueur.rect.x = 560
                joueur.rect.y = 410
                # Afficher "Perdu !" pendant 1 seconde
                afficher_message_perdu(fenetre)
                pygame.display.flip()
                pygame.time.wait(1000)  # Attendre 1 seconde

        if touches[pygame.K_h]:
            resoudre_labyrinthe(labyrinthe, joueur.rect)

        pygame.display.flip()
        clock.tick(60)



# Fonction du menu principal
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fenetre.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)

        title_text = font.render("Labyrinthe", True, (255, 255, 255))
        fenetre.blit(title_text, (largeur/2 - title_text.get_width()/2, 50))

        jouer_text = font.render("Jouer", True, (255, 255, 255))
        jouer_rect = jouer_text.get_rect(center=(largeur/2, 150))
        fenetre.blit(jouer_text, jouer_rect)

        quitter_text = font.render("Quitter", True, (255, 0, 0))
        quitter_rect = quitter_text.get_rect(center=(largeur/2, 200))
        fenetre.blit(quitter_text, quitter_rect)

        mx, my = pygame.mouse.get_pos()

        if jouer_rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                main()

        if quitter_rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Lance le code menu
if __name__ == "__main__":
    menu()