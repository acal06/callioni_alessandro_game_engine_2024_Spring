import pygame

def draw_heath_bar(surf, x, y, pct):
    if pct <0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(suf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)