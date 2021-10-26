import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List

Vector = List[int]
Matrix = List[List[int]]

def openImg(arqImg):
    """This function just opens a image file"""
    img = cv2.imread(arqImg)
    return img

def luminancia(img):
    """Converts a colorful image to a gray image"""
    rows,coluns,_ = img.shape
    img2 = np.zeros((img.shape[0],img.shape[1],1), dtype=np.uint8)
    for i in range(rows):
        for j in range(coluns): 
            img2[i][j][0] = int(img[i][j][0]*0.1140+img[i][j][1]*0.5870+img[i][j][2]*0.2990)
    return img2


def blackandWhite(img):
    """converts a gray maige to a back and white image"""
    rows, coluns,_ = img.shape
    for i in range(rows):
        for j in range(coluns): 
            if img[i][j][0] >= 127:
                img[i][j][0] = 255
            else:
                img[i][j][0] = 0               
    return img



def zhang_suen_rule1(pGroup: Matrix) -> int:
    """[this function is the first rule of the zhang suen algorithm, the first rule says that the selected pixel must have only one connection]

    Args:
        pGroup (Matrix): [is the matrix of pixels selected, the middle pixel is the pixel it has been evaluated and the others is the neighbors]

    Returns:
        int: [the returns is a binary ansewer, if the first rule is obeyed the return is one if not the return is zero]
    """
    connectivity=0
    for y in range(3):
        for x in range(3):
            if y==1 and x==1:
                continue
            else:
                if x==0 or x==1 and y==0:
                    if pGroup[y][x]!=pGroup[y][x+1]:
                        connectivity+=1
                elif y==0 or y==1 and x==2:
                    if pGroup[y][x]!=pGroup[y+1][x]:
                        connectivity+=1
                elif x==1 or x==2 and y==2:
                    if pGroup[y][x]!=pGroup[y][x-1]:
                        connectivity+=1
                elif y==2 or y==1 and x==0:
                    if pGroup[y][x]!=pGroup[y-1][x]:
                        connectivity+=1
                        
    if connectivity == 1:
        return 1
    else:
        return 0
               
def zhang_suen_rule2(pGroup: Matrix) -> int:
    """[this function is the second rule of the zhang suen algorithm, the second rule tells that the selected pixel must have two or more black neighbors and six
        or less]

    Args:
        pGroup (Matrix): [is the matrix of pixels selected, the middle pixel is the pixel it has been evaluated and the others is the neighbors]

    Returns:
        int: [the returns is a binary ansewer, if the first rule is obeyed the return is one if not the return is zero]
    """
    n_black=0
    for y in range(3):
        for x in range(3):
            if pGroup[y][x]==0:
                n_black+=1
    
    if n_black >=2 and n_black<=6:
        return 1
    else:
        return 0                    
    
def zhang_suen_rule3(pGroup: Matrix,etapa: int) -> int:
    """[this function is the third rule of the zhang suen algorithm, the third rule tells that one of the following pixels hass to be white(background),
        this function change the evaluated pixel depending on suen sub interaction]
    Args:
        pGroup (Matrix): [is the matrix of pixels selected, the middle pixel is the pixel it has been evaluated and the others is the neighbors]
        etapa (int): [telss if the zhang suen is runing the first or the second interaction, the accepted values are zero or one, zero is the first interaction and one is the second interaction]
    
    Returns:
        int: [the returns is a binary ansewer, if the first rule is obeyed the return is one if not the return is zero]
    """
    if etapa == 0:
        if pGroup[0][1]==255 or pGroup[1][0]==255 or pGroup[1][2]==255:
            return 1
        else:
            return 0
    if etapa == 1:
        if pGroup[0][1]==255 or pGroup[1][2]==255 or pGroup[2][1]==255:
            return 1
        else:
            return 0       

def zhang_suen_rule4(pGroup: Matrix,etapa: int) -> int:
    """[this function is the fourth rule of the zhang suen algorithm, the fourth rule tells that one of the following pixels hass to be white(background),
        this function change the evaluated pixel depending on suen sub interaction]
    Args:
        pGroup (Matrix): [is the matrix of pixels selected, the middle pixel is the pixel it has been evaluated and the others is the neighbors]
        etapa (int): [telss if the zhang suen is runing the first or the second interaction, the accepted values are zero or one, zero is the first interaction and one is the second interaction]
    
    Returns:
        int: [the returns is a binary ansewer, if the first rule is obeyed the return is one if not the return is zero]
    """
    if etapa == 0:
        if pGroup[0][1]==255 or pGroup[1][0]==255 or pGroup[2][1]==255:
            return 1
        else:
            return 0
    if etapa == 1:
        if pGroup[1][0]==255 or pGroup[1][2]==255 or pGroup[2][1]==255:
            return 1
        else:
            return 0
        
def zhang_suen_exclude(img,y_list,x_list):
    """exclui todos os pixeis marcados para exclusão pela iteração do algoritmo zhang_suen(excluir significa pintar de branco(fundo))"""
    """[recive an image and the two lists of coordinates Y and X, exclude the marked for exclude pixel by reading the coordinates x and y in the lists]

    Returns:
        img[matix]: [return the image file more thin]
    """
    z = len(y_list)
    for i in range(z):
        img[y_list[i]][x_list[i]]=255
    return img
    
def zhang_suen_thinging(img):
    """algorithm zhang_suen"""
    interaction = 0
    matrix = [[255,255,255],
              [255,255,255],
              [255,255,255]]
    y_list = []
    x_list = []
    rows,coluns,_ = img.shape
    mark_4_exclude=1
    flag=1
    while(flag==1):
        for y in range(rows):
            for x in range(coluns):
                if img[y][x]==0:
                    matrix[0][0]==img[y-1][x-1]
                    matrix[0][1]==img[y-1][x]
                    matrix[0][2]==img[y-1][x+1]
                    matrix[1][0]==img[y][x-1]
                    matrix[1][1]==img[y][x]
                    matrix[1][2]==img[y][x+1]
                    matrix[2][0]==img[y+1][x-1]
                    matrix[2][1]==img[y+1][x]
                    matrix[2][2]==img[y+1][x+1]
                    mark_4_exclude = mark_4_exclude * zhang_suen_rule1(matrix) * zhang_suen_rule2(matrix) * zhang_suen_rule3(matrix,interaction) * zhang_suen_rule4(matrix,interaction)
                    if mark_4_exclude==1:
                        y_list.append(y)
                        x_list.append(x)
        if y_list!=[]:
            img = zhang_suen_exclude(img,y_list,x_list)
        else:
            if interaction==1:
                flag=0
        if flag!=0: 
            if interaction==0:
                interaction=1
            else:
                interaction=0       
            matrix =[[255,255,255],
              [255,255,255],
              [255,255,255]]
            y_list = []
            x_list = []               
            mark_4_exclude=1  
    return img             

def main():
    img=openImg('letraforma.jpg')
    img=luminancia(img)
    img=blackandWhite(img)
    img= zhang_suen_thinging(img)
    cv2.imshow("afinamento Zhang_suen",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()
