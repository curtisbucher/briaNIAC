#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:54:15 2019

@author: curtisbucher
"""

import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
done = False

scorefont = pygame.font.SysFont("Arial", 200)
playerfont = pygame.font.SysFont("Arial", 100)

scoreA = 17
scoreB = 21
playerA = "Curtis"
playerB = "Jonathan"

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            scoreA += 1
    
    screen.fill((0,0,0))
    
    playerAtext = playerfont.render(playerA, True, (255,255,255))
    playerBtext = playerfont.render(playerB, True, (255,255,255))
    
    scoretext = scorefont.render(str(scoreA) + "     " + str(scoreB), True, (255,255,255))
    screen.blit(scoretext,((screen.get_width() - text.get_width()) // 2,( screen.get_height() - text.get_height() )// 2))
    
    pygame.display.flip()
    clock.tick(60)
os._exit(0)