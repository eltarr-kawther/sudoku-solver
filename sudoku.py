# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 10:34:49 2020

@author: straw
"""
import numpy as np
import pygame

pygame.init()

class Sudoku:
    def __init__(self, path):
        self.path = path
        self.grid = self.__parser()
        self.width = 800
        self.height = 900
        self.gap = self.width/9
        self.window = None
    
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
        """
        

        Parameters
        ----------
        nb : TYPE
            DESCRIPTION.
        pos : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            valid move or not.

        """
        
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
        """

        Returns
        -------
        bool
            solved sudoku or not.

        """
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
        """
        If the sudoku solver has been called, export results into text file
        Returns
        -------
        None.

        """
        if self.solver():
            np.savetxt("solved_sudoku.txt", self.grid, fmt="%s |")
        else:
            np.savetxt("solved_sudoku.txt", self.grid, fmt="%s |")
    
    def display_numbers(self, font):
        """
        Display Sudoku's numbers in grid

        Parameters
        ----------
        font : pygame.font.Font
            font of numbers.

        Returns
        -------
        None.

        """
        for i in range(0, 9):
            for j in range(0, 9):
                x = i*self.gap
                y = j*self.gap
                if self.grid[j,i] == 0:
                    display = font.render("", 1, (0,0,0))
                    self.window.blit(display,(x + (self.gap/2 - display.get_width()/2), y + (self.gap/2 - display.get_height()/2)))
                else:   
                    display = font.render("{}".format(self.grid[j,i]), 1, (0,0,0))
                    self.window.blit(display,(x + (self.gap/2 - display.get_width()/2), y + (self.gap/2 - display.get_height()/2)))

    def display_rect(self):
        color = (200, 255, 255)
        for row in range(0, 9):
            for column in range(9):
                if self.grid[row][column] == 0:
                    pygame.draw.rect(self.window,
                    color,
                    [self.gap*column,
                    self.gap*row,
                    self.gap,
                    self.gap])
            

    def display_solver(self):
        """
        Displays Sudoku solver

        Returns
        -------
        None.

        """
        self.window = pygame.display.set_mode((self.width, self.height))
        # Set title of screen
        pygame.display.set_caption("Sudoku Solver")
                
        font = pygame.font.SysFont("comicsans", 40)

        self.window.fill((255, 255, 255))
        
        self.display_rect()
        self.display_numbers(font)
        
        run = True
        while run :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos() 
                    if self.width/2-46 <= pos[0] <= self.width/2+46 and self.width+((self.height-self.width)/2)-46 <= pos[1] <= self.width+((self.height-self.width)/2)+46: 
                        self.solver()
                        self.display_numbers(font)

            # Draw Grid Lines
            for k in range(0, 9):
                if k % 3 == 0 and k != 0:
                    thick = 5
                else:
                    thick = 2
                pygame.draw.line(self.window, (0, 0, 0), (0, k*self.gap), (self.width, k*self.gap), thick)
                pygame.draw.line(self.window, (0, 0, 0), (k*self.gap, 0), (k*self.gap, self.width), thick)
            pygame.draw.line(self.window, (0, 0, 0), (0, 9*self.gap), (9*self.gap, self.width), thick)
            pygame.draw.circle(self.window, (0, 0, 0), (round(self.width/2), round(self.width+((self.height-self.width)/2))), 46, 46)
            text = font.render("Solve", 1, (255, 255, 255))
            self.window.blit(text,(round(self.width/2)-35, round(self.width+((self.height-self.width)/2)-14)))
            pygame.display.update()
        pygame.quit()
    
if __name__ == '__main__':
    print()
    s = Sudoku(path="sudoku.txt")
    print('Sudoku grid before solving')
    s.print_grid()
    print()
    s.display_solver()
    print('Sudoku grid after solving')
    s.print_grid()
    s.export_grid()



