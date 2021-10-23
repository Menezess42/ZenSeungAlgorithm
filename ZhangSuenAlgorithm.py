    
    
import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List

Vector = List[int]
Matrix = List[List[int]]

def openImg(arqImg):
    """function que abre uma img"""
    img = cv2.imread(arqImg)
    return img

def luminancia(img):
    """function que converte uma img em grayScale"""
    rows,coluns,_ = img.shape
    img2 = np.zeros((img.shape[0],img.shape[1],1), dtype=np.uint8)
    for i in range(rows):
        for j in range(coluns): 
            img2[i][j][0] = int(img[i][j][0]*0.1140+img[i][j][1]*0.5870+img[i][j][2]*0.2990)
    return img2


def blackandWhite(img):
    """função para transformar uma img em preto e branco"""
    rows, coluns,_ = img.shape
    for i in range(rows):
        for j in range(coluns): 
            if img[i][j][0] >= 127:
                img[i][j][0] = 255
            else:
                img[i][j][0] = 0               
    return img



def zhang_suen_rule1(conjunto: Matrix) -> int:
    
    """confere a priemeira regra 1 do algoritmo zhang suen que define q só pode ocorrer uma conectividade no kn8"""
    """[[y0x0,y0x1,y0x2]
        [y1x0,pixe,y1x2]
        [y2x0,y2x1,y2x2]]"""
    conectividade=0
    for y in range(3):
        for x in range(3):
            if y==1 and x==1:
                continue
            else:
                if x==0 or x==1 and y==0:
                    if conjunto[y][x]!=conjunto[y][x+1]:
                        conectividade+=1
                elif y==0 or y==1 and x==2:
                    if conjunto[y][x]!=conjunto[y+1][x]:
                        conectividade+=1
                elif x==1 or x==2 and y==2:
                    if conjunto[y][x]!=conjunto[y][x-1]:
                        conectividade+=1
                elif y==2 or y==1 and x==0:
                    if conjunto[y][x]!=conjunto[y-1][x]:
                        conectividade+=1
                        
    if conectividade == 1:
        return 1
    else:
        return 0
               
def zhang_suen_rule2(conjunto: Matrix) -> int:
    """confere a segunda regra 2 do algoritmo zhang_suen na qual fala q tem q ter 2 ou mais e 6 ou menos vizinhos pretos"""
    n_black=0
    for y in range(3):
        for x in range(3):
            if conjunto[y][x]==0:
                n_black+=1
    
    if n_black >=2 and n_black<=6:
        return 1
    else:
        return 0                    
    
def zhang_suen_rule3(conjunto: Matrix,etapa: int) -> int:
    """confere a regra 3 da iteração A ou B do algoritmo zhang_suen na qual define q pelomenos um dos pixeis a seguir tem q ser fundo(branco)"""
    if etapa == 0:
        if conjunto[0][1]==255 or conjunto[1][0]==255 or conjunto[1][2]==255:
            return 1
        else:
            return 0
    if etapa == 1:
        if conjunto[0][1]==255 or conjunto[1][2]==255 or conjunto[2][1]==255:
            return 1
        else:
            return 0       

def zhang_suen_rule4(conjunto: Matrix,etapa: int) -> int:
    """confere a regra 3 da iteração A ou B do algoritmo zhang_suen na qual define q pelomenos um dos pixeis a seguir tem q ser fundo(branco)"""
    if etapa == 0:
        if conjunto[0][1]==255 or conjunto[1][0]==255 or conjunto[2][1]==255:
            return 1
        else:
            return 0
    if etapa == 1:
        if conjunto[1][0]==255 or conjunto[1][2]==255 or conjunto[2][1]==255:
            return 1
        else:
            return 0
        
def zhang_suen_exclude(img,y_list,x_list):
    """exclui todos os pixeis marcados para exclusão pela iteração do algoritmo zhang_suen(excluir significa pintar de branco(fundo))"""
    z = len(y_list)
    for i in range(z):
        img[y_list[i]][x_list[i]]=255
    return img
    
def zhang_suen_thinging(img):
    """algoritmo zhang_suen"""
    iteracao = 0
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
                    mark_4_exclude = mark_4_exclude * zhang_suen_rule1(matrix) * zhang_suen_rule2(matrix) * zhang_suen_rule3(matrix,iteracao) * zhang_suen_rule4(matrix,iteracao)
                    if mark_4_exclude==1:
                        y_list.append(y)
                        x_list.append(x)
        if y_list!=[]:
            img = zhang_suen_exclude(img,y_list,x_list)
        else:
            if iteracao==1:
                flag=0
        if flag!=0: 
            if iteracao==0:
                iteracao=1
            else:
                iteracao=0       
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
