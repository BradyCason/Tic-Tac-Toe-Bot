import sys
import pygame
from random import randint
import copy
pygame.font.init()
XOFont = pygame.font.SysFont('Comic Sans MS', 150)
WLFont = pygame.font.SysFont('Comic Sans MS', 35)

class Settings():
    def __init__(self):
        #Initialize Pygame and create Screen
        pygame.init()
        self.screen = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("Tic Tac Toe")
        
    
        #set variables
        self.bg_color = (0,255,100)
        self.gameOver = True
        
        self.pieces = ["","","","","","","","","",]
        pos1 = 150
        pos2 = 350
        pos3 = 550
        self.piecePositions = {0:(pos1,pos1),1:(pos2,pos1),2:(pos3,pos1),3:(pos1,pos2),4:(pos2,pos2),5:(pos3,pos2),6:(pos1,pos3),7:(pos2,pos3),8:(pos3,pos3)}
        self.turnNum = 1
        self.turn = 0
        self.winCoordinates = [[0,1,2],[0,4,8],[0,3,6],[1,4,7],[2,4,6],[2,5,8],[3,4,5],[6,7,8]]
        #double win coordinates: [set 1, set 1, in both sets, set 2, set 2]
        self.doubleWinCoordinates = [[0,1,2,5,8],[0,2,1,4,7],[1,2,0,3,6],[1,2,0,4,8],[0,1,2,4,6],[4,5,3,0,6],[3,5,4,2,7],[3,4,5,2,8],[3,5,4,0,8],[3,5,4,2,6],
                [7,8,6,0,3],[6,8,7,1,4],[6,7,8,2,5],[7,8,6,2,4],[6,7,8,0,4],[3,6,0,4,8],[0,3,6,2,4],[1,7,4,0,8],[1,7,4,2,6],[2,5,8,0,4],[5,8,2,4,6],[0,8,4,2,6]]
        self.piecesLeft = [0,1,2,3,4,5,6,7,8]
        self.computerMoves = {tuple(["","","","","","","","",""]):[0,2,6,8],
        
                tuple(["x","","","","","","","",""]):[4],tuple(["","","x","","","","","",""]):[4],tuple(["","","","","","","x","",""]):[4],
                tuple(["","","","","","","","","x"]):[4],tuple(["","","","","x","","","",""]):[0,2,6,8]}
                
        '''tuple(["o","x","","","","","","",""]):[6],tuple(["o","","x","","","","","",""]):[6],tuple(["o","","","x","","","","",""]):[2],
        tuple(["o","","","","x","","","",""]):[8],tuple(["o","","","","","x","","",""]):[6],tuple(["o","","","","","","x","",""]):[2],
        tuple(["o","","","","","","","x",""]):[2],tuple(["o","","","","","","","","x"]):[2,6],
        tuple(["x","","o","","","","","",""]):[8],tuple(["","x","o","","","","","",""]):[8],tuple(["","","o","x","","","","",""]):[8],
        tuple(["","","o","","x","","","",""]):[6],tuple(["","","o","","","x","","",""]):[0],tuple(["","","o","","","","x","",""]):[0,8],
        tuple(["","","o","","","","","x",""]):[0],tuple(["","","o","","","","","","x"]):[0],
        tuple(["x","","","","","","o","",""]):[8],tuple(["","x","","","","","o","",""]):[8],tuple(["","","x","","","","o","",""]):[0,8],
        tuple(["","","","x","","","o","",""]):[8],tuple(["","","","","x","","o","",""]):[2],tuple(["","","","","","x","o","",""]):[0],
        tuple(["","","","","","","o","x",""]):[0],tuple(["","","","","","","o","","x"]):[0],
        tuple(["x","","","","","","","","o"]):[2,6],tuple(["","x","","","","","","","o"]):[6],tuple(["","","x","","","","","","o"]):[6],
        tuple(["","","","x","","","","","o"]):[2],tuple(["","","","","x","","","","o"]):[0],tuple(["","","","","","x","","","o"]):[6],
        tuple(["","","","","","","x","","o"]):[2],tuple(["","","","","","","","x","o"]):[2],
                
        tuple(["x","","","","o","","","","x"]):[1,3,5,7],tuple(["","","x","","o","","x","",""]):[1,3,5,7],
                
        tuple(["o","x","","x","","","o","",""]):[4,8],tuple(["o","","x","x","","","o","",""]):[8],tuple(["o","x","o","x","","","","",""]):[4,8],
        tuple(["o","x","o","","","","x","",""]):[4,8],tuple(["o","x","o","","","","","","x"]):[6],tuple(["o","","","x","","","o","","x"]):[2],
        tuple(["x","","o","","","x","","","o"]):[6],tuple(["","x","o","","","x","","","o"]):[4,6],tuple(["o","x","o","","","x","","",""]):[4,6],
        tuple(["o","x","o","","","","x","",""]):[4,8],tuple(["","","o","","","x","x","","o"]):[0],tuple(["o","x","o","","","","","","x"]):[6],
        tuple(["x","","","","","","o","x","o"]):[2],tuple(["o","","x","x","","","o","",""]):[8],tuple(["","","x","","","","o","x","o"]):[0],
        tuple(["","","","x","","","o","x","o"]):[2,4],tuple(["o","","","x","","","o","x",""]):[2,4],tuple(["o","","","x","","","o","","x"]):[2],
        tuple(["x","","o","","","x","","","o"]):[6],tuple(["x","","","","","","o","x","o"]):[2],tuple(["","","x","","","","o","x","o"]):[0],
        tuple(["","","","","","x","o","x","o"]):[0,4],tuple(["","","o","","","x","x","","o"]):[0],tuple(["","","o","","","x","","x","o"]):[0,4]}'''

class Button():
    def __init__(self, screen, msg, bg_color, font_size=20, top=0, color=(255,255,255)):
        """initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        #Set the dimensions and properties of the button
        self.width, self.height = 300, 100
        self.button_color = bg_color
        self.text_color = color
        self.font = pygame.font.SysFont("Comic Sans MS",font_size)
        
        #Build the button's rect object and center it.
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.left = 10
        self.rect.top = top
        self.rect.center = self.screen_rect.center
        self.rect.top = top
        
        #The button message needs to be prepped only once.
        self.prep_msg(msg)
        
    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        
        self.msg = msg
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        #Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        
    def check_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_clicked = self.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked:
            return True

def check_for_input(s):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and s.gameOver and playButton.check_button():
            s.gameOver = False
            s.pieces = ["","","","","","","","","",]
            s.piecesLeft = [0,1,2,3,4,5,6,7,8]
            s.turn = randint(0,1)
            s.turnNum = 1
        elif event.type == pygame.MOUSEBUTTONDOWN and s.turn == 0 and s.turnNum < 10 and s.gameOver == False:
            mouseX, mouseY = pygame.mouse.get_pos()
            closestDist = 1000
            for i in range(len(s.pieces)):
                if s.pieces[i] == "":
                    dist = ((s.piecePositions[i][0] - mouseX)**2 + (s.piecePositions[i][1] - mouseY)**2)**0.5
                    if dist < closestDist:
                        closestDist = dist
                        closestSquare = i
            s.pieces[closestSquare] = "x"
            s.piecesLeft.remove(closestSquare)
            s.turn = 1
            s.turnNum += 1

def check_for_win(s):
    for coordinate in s.winCoordinates:
        if s.pieces[coordinate[0]] != "" and s.pieces[coordinate[0]] == s.pieces[coordinate[1]] == s.pieces[coordinate[2]]:
            s.gameOver = True
            if s.pieces[coordinate[0]] == "x":
                textSurface = WLFont.render('You won! How have you done this?', False, (0,0,0))
                textRect = textSurface.get_rect(center=(350,25))
                s.screen.blit(textSurface,textRect)
            else:
                textSurface = WLFont.render('You lost to an inanamate object, dummy.', False, (0,0,0))
                textRect = textSurface.get_rect(center=(350,25))
                s.screen.blit(textSurface,textRect)
    if s.turnNum > 9:
        s.gameOver = True

def draw_board(s):
    s.screen.fill(s.bg_color)
    pygame.draw.rect(s.screen, (0,0,0), (245, 50, 10, 600))
    pygame.draw.rect(s.screen, (0,0,0), (445, 50, 10, 600))
    pygame.draw.rect(s.screen, (0,0,0), (50, 245, 600, 10))
    pygame.draw.rect(s.screen, (0,0,0), (50, 445, 600, 10))
    
    for i in range(len(s.pieces)):
        if s.pieces[i] == "x":
            textSurface = XOFont.render('X', False, (100,0,0))
            textRect = textSurface.get_rect(center=s.piecePositions[i])
            s.screen.blit(textSurface,textRect)
        if s.pieces[i] == "o":
            textSurface = XOFont.render('O', False, (100,0,0))
            textRect = textSurface.get_rect(center=s.piecePositions[i])
            s.screen.blit(textSurface,textRect)
    
    if s.gameOver:
        playButton.draw_button()
            
def computer_turn(s):
    if s.turn == 1 and s.turnNum < 10 and s.gameOver == False:
        i = ""
        piecesLeftOnTurn = copy.copy(s.piecesLeft)
        
        #if 2 in a row
        for coordinate in s.winCoordinates:
            if s.pieces[coordinate[0]] == "" and s.pieces[coordinate[1]] == "o" and s.pieces[coordinate[2]] == "o":
                i = coordinate[0]
            elif s.pieces[coordinate[0]] == "o" and s.pieces[coordinate[1]] == "" and s.pieces[coordinate[2]] == "o":
                i = coordinate[1]
            elif s.pieces[coordinate[0]] == "o" and s.pieces[coordinate[1]] == "o" and s.pieces[coordinate[2]] == "":
                i = coordinate[2]
        if i == "":
            #If enemy has 2 in a row
            for coordinate in s.winCoordinates:
                if s.pieces[coordinate[0]] == "" and s.pieces[coordinate[1]] == "x" and s.pieces[coordinate[2]] == "x":
                    if i == "":
                        piecesLeftOnTurn = [coordinate[0]]
                        i = piecesLeftOnTurn[randint(0,len(piecesLeftOnTurn)-1)]
                    else:
                        piecesLeftOnTurn.append(coordinate[0])
                        i = piecesLeftOnTurn[randint(0,len(piecesLeftOnTurn)-1)]
                elif s.pieces[coordinate[0]] == "x" and s.pieces[coordinate[1]] == "" and s.pieces[coordinate[2]] == "x":
                    if i == "":
                        piecesLeftOnTurn = [coordinate[1]]
                        i = piecesLeftOnTurn[randint(0,len(piecesLeftOnTurn)-1)]
                    else:
                        piecesLeftOnTurn.append(coordinate[1])
                        i = piecesLeftOnTurn[randint(0,len(piecesLeftOnTurn)-1)]
                elif s.pieces[coordinate[0]] == "x" and s.pieces[coordinate[1]] == "x" and s.pieces[coordinate[2]] == "":
                    if i == "":
                        piecesLeftOnTurn = [coordinate[2]]
                        i = piecesLeftOnTurn[randint(0,len(piecesLeftOnTurn)-1)]
                    else:
                        piecesLeftOnTurn.append(coordinate[2])
                        i = piecesLeftOnTurn[randint(0,len(piecesLeftOnTurn)-1)]
        if i == "":
            #If can make a double winning opportunity
            #double win coordinates: [set 1, set 1, in both sets, set 2, set 2]
            for coordinate in s.doubleWinCoordinates:
                if (s.pieces[coordinate[2]] == "") and ((s.pieces[coordinate[0]] == "o" and s.pieces[coordinate[1]] == "") or (s.pieces[coordinate[0]] == "" and s.pieces[coordinate[1]] == "o")) and ((s.pieces[coordinate[3]] == "o" and s.pieces[coordinate[4]] == "") or (s.pieces[coordinate[3]] == "" and s.pieces[coordinate[4]] == "o")):
                    if i == "":
                        piecesLeftOnTurn = [coordinate[2]]
                    else:
                        piecesLeftOnTurn.append(coordinate[2])
                    i = piecesLeftOnTurn[randint(0,len(piecesLeftOnTurn)-1)]
        
        if i == "":
            #If opponent can make a double winning oportunity, block it unless it makes another.
            for coordinate in s.doubleWinCoordinates:
                if (s.pieces[coordinate[2]] == "") and ((s.pieces[coordinate[0]] == "x" and s.pieces[coordinate[1]] == "") or (s.pieces[coordinate[0]] == "" and s.pieces[coordinate[1]] == "x")) and ((s.pieces[coordinate[3]] == "x" and s.pieces[coordinate[4]] == "") or (s.pieces[coordinate[3]] == "" and s.pieces[coordinate[4]] == "x")):
                    s.pieces[coordinate[2]] = "o"
                    notDouble = True
                    for coordinate1 in s.doubleWinCoordinates:
                        if (coordinate1 != coordinate) and ((s.pieces[coordinate1[2]] == "") and ((s.pieces[coordinate1[0]] == "x" and s.pieces[coordinate1[1]] == "") or (s.pieces[coordinate1[0]] == "" and s.pieces[coordinate1[1]] == "x")) and ((s.pieces[coordinate1[3]] == "x" and s.pieces[coordinate1[4]] == "") or (s.pieces[coordinate1[3]] == "" and s.pieces[coordinate1[4]] == "x"))):
                            notDouble = False
                    s.pieces[coordinate[2]] = ""
                    if notDouble:
                        i = coordinate[2]
                    else:
                        piecesLeftOnTurn.remove(coordinate[2])
                        
        if i == "":
            #If can make a move that forces them to play in a place and give oportunity to make double winning oportunity
            for firstMove in s.piecesLeft:
                s.pieces[firstMove] = "o"
                #Check if forces them to play
                forcesPlay = False
                for coordinate in s.winCoordinates:
                    if (firstMove == coordinate[0] and ((s.pieces[coordinate[1]] == "o" and s.pieces[coordinate[2]] == "") or (s.pieces[coordinate[1]] == "" and s.pieces[coordinate[2]] == "o"))) or (firstMove == coordinate[1] and ((s.pieces[coordinate[0]] == "o" and s.pieces[coordinate[2]] == "") or (s.pieces[coordinate[0]] == "" and s.pieces[coordinate[2]] == "o"))) or (firstMove == coordinate[2] and ((s.pieces[coordinate[1]] == "o" and s.pieces[coordinate[0]] == "") or (s.pieces[coordinate[1]] == "" and s.pieces[coordinate[0]] == "o"))):
                        forcesPlay = True
                        if s.pieces[coordinate[0]] == "":
                            secondMove = coordinate[0]
                        elif s.pieces[coordinate[1]] == "":
                            secondMove = coordinate[1]
                        else:
                            secondMove = coordinate[2]
                        s.pieces[secondMove] = "x"
                
                #if gives opportunity for double winning opportunity
                if forcesPlay:
                    for coordinate in s.doubleWinCoordinates:
                        if (s.pieces[coordinate[2]] == "") and ((s.pieces[coordinate[0]] == "o" and s.pieces[coordinate[1]] == "") or (s.pieces[coordinate[0]] == "" and s.pieces[coordinate[1]] == "o")) and ((s.pieces[coordinate[3]] == "o" and s.pieces[coordinate[4]] == "") or (s.pieces[coordinate[3]] == "" and s.pieces[coordinate[4]] == "o")):
                            if i == "":
                                piecesLeftOnTurn = [coordinate[2]]
                            else:
                                piecesLeftOnTurn.append(coordinate[2])
                            i = piecesLeftOnTurn[randint(0,len(piecesLeftOnTurn)-1)]
                    
                    s.pieces[secondMove] = ""
                s.pieces[firstMove] = ""
            
        if i == "":
            try:
                #Preprogramed move
                i = s.computerMoves[tuple(s.pieces)][randint(0,len(s.computerMoves[tuple(s.pieces)])-1)]
            except:
                #Random space
                if len(piecesLeftOnTurn) >= 1:
                    i = piecesLeftOnTurn[randint(0,len(piecesLeftOnTurn)-1)]
                else:
                    i = s.piecesLeft[randint(0,len(s.piecesLeft)-1)]
                
        s.pieces[i] = "o"
        s.piecesLeft.remove(i)
        
        s.turn = 0
        s.turnNum += 1

s = Settings()
playButton = Button(s.screen, "Play", bg_color = (50,50,50), font_size=70,top=300, color=(255,255,255))
while True:
    draw_board(s)
    check_for_input(s)
    check_for_win(s)
    computer_turn(s)
    check_for_win(s)
    
    pygame.display.flip()
