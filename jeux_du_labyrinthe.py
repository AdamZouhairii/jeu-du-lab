import pygame
import sys
import pygame.font

pygame.init()

largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame_icon = pygame.image.load("C:/Users/Adame/Desktop/jeu du lab/labyrinthe.png")
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Jeu du Labyrinthe")

rouge = (255, 0, 0)
noir = (0, 0, 0)
blanc = (255, 255, 255)

class Joueur(pygame.sprite.Sprite):
    def __init__(self,x=560 ,y=410):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(rouge)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vitesse = 3

class Labyrinthe:
    def __init__(self):
        self.grille = [
            "XXXXXXXXXXXXXXVXXXX",
            "X     X           X",
            "X XXXXX XXXXXXX XXX",
            "X X O X       XXXXX",
            "X X XXX XXXXX XXXXX",
            "X X X     O    X  X",
            "X X XXXXXXX X XXXXX",
            "X X         X     X",
            "X XXXXXXXXX XXXXX X",
            "X                 X",
            "XXXXXXXXXXXXXXDXXXX",
        ]

def afficher_labyrinthe(labyrinthe, fenetre):
    for ligne, row in enumerate(labyrinthe.grille):
        for col, case in enumerate(row):
            if case == "X":
                pygame.draw.rect(fenetre, noir, (col * 40, ligne * 40, 40, 40))
            elif case == " ":
                pygame.draw.rect(fenetre, blanc, (col * 40, ligne * 40, 40, 40))
            elif case == "V":
                pygame.draw.rect(fenetre, rouge, (col * 40, ligne * 40, 40, 40))

def collision_avec_murs(joueur_temp_rect, labyrinthe):
    for ligne, row in enumerate(labyrinthe.grille):
        for col, case in enumerate(row):
            if case == "X":
                mur_rect = pygame.Rect(col * 40, ligne * 40, 40, 40)
                if joueur_temp_rect.colliderect(mur_rect):
                    return True
    return False

def victoire(joueur_rect, labyrinthe):
    for ligne, row in enumerate(labyrinthe.grille):
        for col, case in enumerate(row):
            if case == "V":
                victoire_rect = pygame.Rect(col * 40, ligne * 40, 40, 40)
                if joueur_rect.colliderect(victoire_rect):
                    return True
    return False

def afficher_message_victoire(fenetre):
    font = pygame.font.Font(None, 36)
    text = font.render("Victoire !", True, (200,200,200))
    fenetre.blit(text,(300,250))

def main():
    labyrinthe = Labyrinthe()
    joueur = Joueur()
    victoire_affichee = False
    victoire_timer=None

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

        if not collision_avec_murs(joueur_temp_rect, labyrinthe):
            joueur.rect = joueur_temp_rect

        fenetre.fill((0, 0, 0))
        afficher_labyrinthe(labyrinthe, fenetre)
        fenetre.blit(joueur.image, joueur.rect)

        if victoire(joueur.rect, labyrinthe) and not victoire_affichee:
            victoire_affichee = True
            victoire_timer = pygame.time.get_ticks()

        if victoire_affichee:
            if pygame.time.get_ticks()-victoire_timer>= 1000:
                pygame.quit()
                sys.exit()
            else:
                afficher_message_victoire(fenetre)

        pygame.display.flip()
        clock.tick(60)

def menu():
    while True:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Affichage du menu
        fenetre.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        
        # Modifier le titre
        title_text = font.render("Labyrinthe", True, (255, 255, 255))
        fenetre.blit(title_text, (largeur/2 - title_text.get_width()/2, 50))
        
        # Ajouter un bouton "Jouer"
        jouer_text = font.render("Jouer", True, (255, 255, 255))
        jouer_rect = jouer_text.get_rect(center=(largeur/2, 150))
        fenetre.blit(jouer_text, jouer_rect)

        # Ajouter un bouton "Quitter"
        quitter_text = font.render("Quitter", True, (255, 0, 0))
        quitter_rect = quitter_text.get_rect(center=(largeur/2, 200))
        fenetre.blit(quitter_text, quitter_rect)

        # Vérification des clics de souris
        mx, my = pygame.mouse.get_pos()

        if jouer_rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                main()  # Lancer la fonction main()

        if quitter_rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    menu()
