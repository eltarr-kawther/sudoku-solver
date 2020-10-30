# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 10:34:49 2020

@author: straw
"""
import os
import numpy as np
import pygame

pygame.init()

#os.chdir(r'C:\Users\straw\Desktop\AIS\ProjectPool 1\Sudoku')

class Sudoku:
    def __init__(self, path):
        self.path = path
        self.grid = self.__parser()
    
    def __load_file(self):
        """
        This function loads the sudoku file for a given path

        Returns
        -------
        content : str
            loaded file's content.

        """
        file = open(self.path, "r")
        content = file.read()
        file.close()
        return content
    
    def __parser(self):
        """
        This function parses sudoku content and saves it to a grid
        
        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self.grid = np.zeros((9,9))
        content = self.__load_file()
        content = content.translate({ord('\n'): None})
        content = content.replace("_", "0")
        if len(content) != 81:
            raise ValueError('The selected sudoku does\'nt have the right format.')
        else:
            rows = []
            for i in range(0, len(content), 9):
                rows.append(content[i:i+9])
            for r in range(0, len(rows)):
                self.grid[r,:] = np.array(list(rows[r]))
            self.grid = self.grid.astype(int)
        return self.grid
    
    def print_grid(self):
        """
        This function print the sudoku grid

        Returns
        -------
        None.

        """
        print()
        for i in range(0, len(self.grid)):
            if i % 3 == 0 and i != 0:
                print("---------------------")
            for j in range(0, len(self.grid)):
                if j % 3 == 0 and j != 0:
                    print('| ', end="")
                if j == 8:
                    print(self.grid[i,j])
                else:
                    print(str(self.grid[i,j]) + " ", end="")
    
    def __get_empty_box(self):
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None
    
    def __check_move_validity(self, nb, pos):
        
        # Find square and check it
        r_square = pos[0] // 3
        c_square = pos[1] // 3
        for r in range(r_square*3, r_square*3 + 3):
            for c in range(c_square*3, c_square*3 + 3):
                if self.grid[r,c] == nb and (r,c) != pos :
                    return False
        
        # Set row check columns
        for j in range(0, len(self.grid)):
            if self.grid[pos[0],j] == nb and j != pos[1]:
                return False
        # Set column check rows
        for i in range(0, len(self.grid)):
            if self.grid[i,pos[1]] == nb and i != pos[0]:
                return False
        
        return True
    
    def solver(self):
        empty = self.__get_empty_box()
        if empty == None:
            return True
        else:
            for n in [1,2,3,4,5,6,7,8,9]:
                if self.__check_move_validity(n, empty):
                    self.grid[empty[0], empty[1]] = n
                    if self.solver():
                        return True
                    self.grid[empty[0], empty[1]] = 0
        return False
    
    def export_grid(self):
        self.solver()
        np.savetxt("solved_sudoku.txt", self.grid, fmt="%s |")
        
    
    def display_solver(self):
        width = 800
        height = 1000
        size = (width, height)
        window = pygame.display.set_mode(size)
        gap = width/9
        
        # Set title of screen
        pygame.display.set_caption("Sudoku Solver")
        
        font = pygame.font.SysFont("comicsans", 40)

        window.fill((255, 255, 255))

        for i in range(0, 9):
            for j in range(0, 9):
                x = i*gap
                y = j*gap
                display = font.render("{}".format(self.grid[j,i]), 1, (0,0,0))
                window.blit(display,(x + (gap/2 - display.get_width()/2), y + (gap/2 - display.get_width()/2)))
        run = True
        while run :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                #if event.type == pygame.MOUSEBUTTONDOWN:
            # Draw Grid Lines
            for k in range(0, 9):
                if k % 3 == 0 and k != 0:
                    thick = 5
                else:
                    thick = 2
                pygame.draw.line(window, (0, 0, 0), (0, k*gap), (800, k*gap), thick)
                pygame.draw.line(window, (0, 0, 0), (k*gap, 0), (k* gap, 800), thick)
        
            pygame.display.flip()
        pygame.quit()

    
if __name__ == '__main__':
    print()
    s = Sudoku(path="sudoku.txt")
    print('Sudoku grid before solving')
    s.print_grid()
    print()
    #s.display_solver()
    s.solver()
    print('Sudoku grid after solving')
    s.print_grid()
    s.display_solver()
    #s.export_grid()


