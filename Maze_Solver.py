import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import getpass
from PIL import Image

#READ ME:::::

# This program fails to work with maze pics that have transparent pixels. If program fails it might be because you...
#...need to convert the image to a jpeg first to get rid of the transparency.
#Please convert image to black and white, or draw over all color pictures on image that may ruin it. See why below.
#Once done, Add a SINGLE PURE RED (255,0,0) Pixel to act as the starting point.
#Add a SINGLE PURE GREEN (0,255,0) pixel to act as the end point. If there's multiple end points u can give each a pixel
#BORDER OFF THE START OF THE MAZE AND THE END (WITH A COLOR OTHER THAN PURE RED OR GREEN). THIS PREVENTS THE SOLVER FROM
#GOING OUTSIDE OR AROUND THE MAZE!!!
#The reason to draw over color pictures on the maze/convert to black and white is so it doesnt falsley think a picture
#is a start point or an end point.

#SOLVE TIMES: (dependent on complication of the maze as well as size)
#for small pics (think 50x50) it is almost instantly solved.
#for medium pics (think 200x200) it is solved in under a minute.
#for larger pics (think 500x500) it is solved in upwards of 20 minutes. to find a directions to ur local Wegmans
#it will take a week or so, although i have not tried.



#In notes i mention 'String Coordinates'. this means i store the coordinates in string format
#E.G if the coord is [x,y] the string coordinate is "x-y". Its easier to find repeated coords that way in a list.

# Three Functions. pathfinder solves. main calls. and drawmap draws.
class data:
    # stores data for all the functions.
    # 'start' is the pixel coordsinates of the Pure red pixel (the start point of the maze) e.g [5,6] x=5 y=6
    # 'endstr'= list of the mazes end string coordinates. Usually only one value, but a maze might have multiple exits.
    # 'walls' stores the string coordinates of the walls the program scans.
    # dimension stores the pixel dimensions of the image.
    start=[]
    endstr=[]
    walls=[]
    dimension=[]

def pathfinder():
    #the function that solves the maze. called in def main():.
    #starting from the start co-ord, it expands pixel by pixel over whitespace. Each pixel  expansion is assigned an...
    #...Unique ID. a 1 means right, 2 means down, 3 means right, 4 means up. For example, starting from a start...
    #...coordinate, the pixel to the left of that is 3, above is 4, right is 1, down is 2. It stores all of these one...
    #...digit ids in a list. It then goes through all the one digit ids and does the same. So for id 1, the pixel  to...
    #...its right is 11, above it is 14, below is 12. for id 3, above it 34, below it is 32, to its left is 33.
    #it then deletes the previous digits list and focuses on all 2 digit id's. This creates a blob of sorts. it is...
    # ...blocked by walls. it expands until it reaches one of/the endpoint and returns the endpoints I.D.
    #If the ID was '332134' that means from the start co-ord go left left down right left up' to get to the end!
    start=data.start.copy() #quickly stores the start co-ordinate
    startstr=str(start[0])+'-'+str(start[1]) #stores this start co-ord as a string coordinate
    digits={} #where the I.ds of each digit are stored.
    walls=data.walls.copy() #quickly grabs the list of all walls co-ord strings
    digits[0]=[0]  #sets the '0'th digit's id to 0 (the starting point)
    coordint=0 #counts iterations. The iterations tell us what number digit we are on.
    endpoints=data.endstr.copy()
    ids=[]
    allcords=[startstr] #while all the ids are stored in the dictionary in respective digit lists, its easier to...
    #...accesss which I'ds we'e already taken if they're all in a list.
    while True: #makes blob expand until it either finds the green pixel/end point, or runs out of space to expand...
        #... which means its unsolvable as the end point is unreachable
        if len(digits[coordint])==0 and len(endpoints)!=0:
            #this means that for the current digit, there are no ids stored. I.E it ran out of room to expand.
            return 'break' #it is unsolvable!
        if len(endpoints)==0:
            return ids
        try: #to save room (I think) it deletes all the id's not in use in the digits dictionary
            digits[coordint-1].clear()
        except:
            pass
        digits[coordint+1]=[] #creates a list to append the new id's to
        for id in digits[coordint]: #for each id that is coordint digits long
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
            coord=[start[0]+x,start[1]+y] #ok so from the id we can actually get the co-ordinates of the id.
            leftcordstr=str(coord[0]-1)+'-'+str(coord[1])
            rightcordstr=str(coord[0]+1)+'-'+str(coord[1])
            upcordstr=str(coord[0]) + '-' + str(coord[1]-1)
            downcordstr = str(coord[0]) + '-' + str(coord[1]+1) #stores the cords left,rright,above,below, as strings
            leftid=int(str(id)+'3')
            rightid=int(str(id)+'1')
            upid=int(str(id)+'4')
            downid=int(str(id)+'2') #creates a new id for each possible expansion. not all will be used.
            if coordint%2==0: #Ill get into this at the end <-
                if (coord[0]-1) <0: #that means the pixel is off the picture and DNE, pass
                    pass
                # these statements checkif the bordering coords are walls, endpoints, are already  expanded on
                elif leftcordstr not in allcords and leftcordstr not in walls and leftcordstr not in endpoints:
                    digits[coordint+1].append(leftid)
                    # if its not a wall, not an endpoint, and not already expanded onto, expand here. store id.
                    allcords.append(leftcordstr)
                    #keeps track of which coords have been expanded on by adding new expaneded string coords to the list
                elif leftcordstr in endpoints: #This means it found the endpoint
                    ids.append(id)
                    endpoints.remove(leftcordstr)
                if (coord[0]+1)>data.dimension[0]:
                    pass
                elif rightcordstr not in allcords and rightcordstr not in walls and rightcordstr not in endpoints:
                    digits[coordint+1].append(rightid)
                    allcords.append(rightcordstr)
                elif rightcordstr in endpoints:
                    ids.append(id)
                    endpoints.remove(rightcordstr)
                if (coord[1]-1)<0:
                    pass
                elif upcordstr not in allcords and upcordstr not in walls and upcordstr not in endpoints:
                    digits[coordint+1].append(upid)
                    allcords.append(upcordstr)
                elif upcordstr in endpoints:
                    ids.append(id)
                    endpoints.remove(upcordstr)
                if (coord[1]+1)>data.dimension[1]:
                    pass
                elif downcordstr not in allcords and downcordstr not in walls and downcordstr not in endpoints:
                    digits[coordint+1].append(downid)
                    allcords.append(downcordstr)
                elif downcordstr in endpoints:
                    ids.append(id)
                    endpoints.remove(downcordstr)
            else:
                if (coord[1]-1)<0:
                    pass
                elif upcordstr not in allcords and upcordstr not in walls and upcordstr not in endpoints:
                    digits[coordint+1].append(upid)
                    allcords.append(upcordstr)
                elif upcordstr in endpoints:
                    ids.append(id)
                    endpoints.remove(upcordstr)
                if (coord[1]+1)>data.dimension[1]:
                    pass
                elif downcordstr not in allcords and downcordstr not in walls and downcordstr not in endpoints:
                    digits[coordint+1].append(downid)
                    allcords.append(downcordstr)
                elif downcordstr in endpoints:
                    ids.append(id)
                    endpoints.remove(downcordstr)
                if (coord[0]-1) <0:
                    pass
                elif leftcordstr not in allcords and leftcordstr not in walls and leftcordstr not in endpoints:
                    digits[coordint+1].append(leftid)
                    allcords.append(leftcordstr)
                elif leftcordstr in endpoints:
                    ids.append(id)
                    endpoints.remove(leftcordstr)
                if (coord[0]+1)>data.dimension[0]:
                    pass
                elif rightcordstr not in allcords and rightcordstr not in walls and rightcordstr not in endpoints:
                    digits[coordint+1].append(rightid)
                    allcords.append(rightcordstr)
                elif rightcordstr in endpoints:
                    ids.append(id)
                    endpoints.remove(rightcordstr)

        coordint+=1 #goes to next digit
        #Ok so the reason for the 'if coordint%2==0:' is so that the pattern of expansion alternates, and careates...
        #...a diagnal path!
def drawmap(ids,im,pix): #id=the id returned by def pathfinder.  im is the image (so it can edit). pix is the image data.
    #called in def main().
    for id in ids:
        cords = data.start.copy()
        if id == 'break':
            input("maze is unsolvable")
            break
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
        im.save('edit.png') #goes through each direction of the I.D, draws it purple. Saves new image.


def main():
    #User gets the user of the computer to use in the path to find the image.
    user = getpass.getuser()
    user = str(user)
    #asks user for the file name, attempts to find file on desktop and load.
    while True:
        picture_name=input("Please Enter the exact name of the Maze file on your desktop you want to read (include .jpg, .png, etc)\n>> ")
        try:
            im = Image.open('C:/Users/' + user + '/Desktop/'+str(picture_name)) #opens image
            pix = im.load() #loads pixel data to pix
            break
        except:
            print("Error. Either couldn't find file on Desktop, or file type is not usable. try again...")
    #Grabs and stores the Dimensions of the picture in class data
    data.dimension = im.size
    for i in range(data.dimension[0]):
        for j in range(data.dimension[1]):  #these go pixel by pixel to scan for walls, startpoint, endpoint.
            if pix[i, j][1] == 0 and pix[i, j][0] == 255 and pix[i, j][2] == 0: #if pixel is pure red; startpoint
                data.start = [i, j]
            elif pix[i, j][1] == 255 and pix[i, j][0] == 0 and pix[i, j][2] == 0: #if pure green; stores as endpoint
                data.endstr.append(str(i) + '-' + str(j))
            elif pix[i, j][1] > 215 and pix[i, j][0] > 215 and pix[i, j][2] > 215: #if it is slightly white; nothing
                pass
            else: #any pixel not pure green, pure red, or slightly white is considered a wall.
                data.walls.append(str(i) + '-' + str(j))
    ids=pathfinder() #grabs the ID for to get to endpoint
    drawmap(ids,im,pix)  #draws path to pic stored as edit.png
    img=mpimg.imread('edit.png')   #rereads pic
    plt.imshow(img)
    plt.show() #displays picture with path drawn on.

main() #Thats it!
