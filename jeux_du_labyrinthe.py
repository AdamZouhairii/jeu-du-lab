import pygame,sys,random

pygame.init()

largeur, hauteur = 800, 600

fenetre = pygame.display.set_mode((largeur, hauteur))

icon = pygame.image.load('C:/Users/Adame/Desktop/jeu du lab/labyrinthe.png')

pygame.display.set_icon(icon)

pygame.display.set_caption("Jeu du Labyrinthe")
rouge= (255, 0, 0)
noir = (0, 0, 0)
blanc = (255, 255, 255)

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(rouge)
        self.rect = self.image.get_rect()
        self.rect.center = (largeur // 2, hauteur // 2)
        self.vitesse = 3

class Labyrinthe:
    def __init__(self):
        self.grille = [
            "XXXXXXXXXXXXXX XXXX",
            "X     X           X",
            "X XXXXX XXXXXXX XXX",
            "X X O X       XXXXX",
            "X X XXX XXXXX XXXXX",
            "X X X     O    X  X",
            "X X XXXXXXX X XXXXX",
            "X X         X     X",
            "X XXXXXXXXX XXXXX X",
            "X                 X",
            "XXXXXXXXXXXXXX  XXX",
        ]

def afficher_labyrinthe(labyrinthe, fenetre):
    for ligne, row in enumerate(labyrinthe.grille):
        for col, case in enumerate(row):
            if case == "X":
                pygame.draw.rect(fenetre, noir, (col * 40, ligne * 40, 40, 40))
            elif case == " ":
                pygame.draw.rect(fenetre, blanc, (col * 40, ligne * 40, 40, 40))

def collision_avec_murs(joueur_temp_rect, labyrinthe):
    for ligne, row in enumerate(labyrinthe.grille):
        for col, case in enumerate(row):
            if case == "X":
                mur_rect = pygame.Rect(col * 40, ligne * 40, 40, 40)
                if joueur_temp_rect.colliderect(mur_rect):
                    return True
    return False


def main():
    labyrinthe = Labyrinthe()
    joueur = Joueur()

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

        # Créez un nouveau rect temporaire pour le joueur(adam oublie pas)
        joueur_temp_rect = joueur.rect.copy()
        joueur_temp_rect.x = joueur_x
        joueur_temp_rect.y = joueur_y

        if not collision_avec_murs(joueur_temp_rect, labyrinthe):
            joueur.rect = joueur_temp_rect

        fenetre.fill((0, 0, 0))
        afficher_labyrinthe(labyrinthe, fenetre)
        fenetre.blit(joueur.image, joueur.rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
