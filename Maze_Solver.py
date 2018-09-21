import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import getpass
import time
import os
from PIL import Image
user=getpass.getuser()
user=str(user)
img=mpimg.imread('C:/Users/' + user + '/Desktop/MAZE.png')
im=Image.open('C:/Users/' + user + '/Desktop/MAZE.png')
pix=im.load()
dimensions=im.size

class data:
    start=[]
    end=[]
    endstr=''
    walls=[]
    dimension=dimensions
def pathfinder():
    start=data.start.copy()
    startstr=str(start[0])+'-'+str(start[1])
    digits={}
    walls=data.walls.copy()
    digits[0]=[0]
    coordint=0
    allcords=[startstr]
    while True:
        if len(digits[coordint])==0:
            return 'break'
        try:
            digits[coordint-1].clear()
        except:
            pass
        digits[coordint+1]=[]
        for id in digits[coordint]:
            x=0
            y=0
            for n in str(id):
                if n=='1':
                    x+=1
                if n=='3':
                    x-=1
                if n=='2':
                    y+=1
                if n=='4':
                    y-=1
            coord=[start[0]+x,start[1]+y]
            leftcordstr=str(coord[0]-1)+'-'+str(coord[1])
            rightcordstr=str(coord[0]+1)+'-'+str(coord[1])
            upcordstr=str(coord[0]) + '-' + str(coord[1]-1)
            downcordstr = str(coord[0]) + '-' + str(coord[1]+1)
            leftid=int(str(id)+'3')
            rightid=int(str(id)+'1')
            upid=int(str(id)+'4')
            downid=int(str(id)+'2')
            if coordint%2==0:
                if (coord[0]-1) <0:
                    pass
                elif leftcordstr not in allcords and leftcordstr not in walls and leftcordstr !=data.endstr:
                    digits[coordint+1].append(leftid)
                    allcords.append(leftcordstr)
                elif leftcordstr==data.endstr:
                    foundid = id
                    return  foundid
                if (coord[0]+1)>data.dimension[0]:
                    pass
                elif rightcordstr not in allcords and rightcordstr not in walls and rightcordstr !=data.endstr:
                    digits[coordint+1].append(rightid)
                    allcords.append(rightcordstr)
                elif rightcordstr==data.endstr:
                    foundid = id
                    return foundid
                if (coord[1]-1)<0:
                    pass
                elif upcordstr not in allcords and upcordstr not in walls and upcordstr !=data.endstr:
                    digits[coordint+1].append(upid)
                    allcords.append(upcordstr)
                elif upcordstr==data.endstr:
                    foundid = id
                    return foundid
                if (coord[1]+1)>data.dimension[1]:
                    pass
                elif downcordstr not in allcords and downcordstr not in walls and downcordstr !=data.endstr:
                    digits[coordint+1].append(downid)
                    allcords.append(downcordstr)
                elif downcordstr==data.endstr:
                    foundid = id
                    return foundid
            else:
                if upcordstr not in allcords and upcordstr not in walls and upcordstr !=data.endstr:
                    digits[coordint+1].append(upid)
                    allcords.append(upcordstr)
                elif upcordstr==data.endstr:
                    foundid = id
                    return foundid
                if downcordstr not in allcords and downcordstr not in walls and downcordstr !=data.endstr:
                    digits[coordint+1].append(downid)
                    allcords.append(downcordstr)
                elif downcordstr==data.endstr:
                    foundid = id
                    return foundid
                if leftcordstr not in allcords and leftcordstr not in walls and leftcordstr !=data.endstr:
                    digits[coordint+1].append(leftid)
                    allcords.append(leftcordstr)
                elif leftcordstr==data.endstr:
                    foundid = id
                    return  foundid
                if rightcordstr not in allcords and rightcordstr not in walls and rightcordstr !=data.endstr:
                    digits[coordint+1].append(rightid)
                    allcords.append(rightcordstr)
                elif rightcordstr==data.endstr:
                    foundid = id
                    return foundid
        coordint+=1
def drawmap(id):
    cords=data.start.copy()
    print(id)
    if id=='break':
        input("maze is unsolvable")
    else:
        for chara in str(id):
            if chara=='1':
                cords[0]+=1
                pix[cords[0], cords[1]] = (178, 0, 255)
            elif chara=='2':
                cords[1] += 1
                pix[cords[0], cords[1]] = (178, 0, 255)
            elif chara=='3':
                cords[0] -= 1
                pix[cords[0], cords[1]] = (178, 0, 255)
            elif chara=='4':
                cords[1] -= 1
                pix[cords[0], cords[1]] = (178, 0, 255)
    im.save('edit.png')

for i in range(data.dimension[0]):
    for j in range(data.dimension[1]):
        if pix[i, j][1] == 0 and pix[i, j][0] == 255 and pix[i, j][2] == 0:
            data.start = [i, j]
        elif pix[i, j][1] == 255 and pix[i, j][0] == 0 and pix[i, j][2] == 0:
            data.end = [i, j]
            data.endstr = (str(i) + '-' + str(j))
        elif pix[i, j][1] > 215 and pix[i, j][0] > 215 and pix[i, j][2] > 215:
            pass
        else:
            data.walls.append(str(i) + '-' + str(j))

id=pathfinder()
drawmap(id)
img=mpimg.imread('edit.png')

plt.imshow(img)
plt.show()

