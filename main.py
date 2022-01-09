import turtle as tr
import pickle
import time
import copy
'''
---------------------------GENERAL------------------------------------------
#Finished adding the separators between thefunctions for a clearer display
#fixed all the "arrive" into "arrivee" (typo)
#Finished fixing the useless "in range (0,n)" with "in range (n)"
#Added a little V after some separators for the functions that don't need to be touched again
-------------------FUNCTION MODIFICATIONS-----------------------------------
-"reccolor":
#Replaced the lines identical to the "rec" function
-"listscoreboard":
#fixed a typo for the "listscoreboard" function (it was "lits" instead of "list")
-"move":
#Made a "move" function replacing the repetition of up>goto>down
-"verifier_deplacement":
#It wasn't used at all, so I implemented it where it should be (in the "jouer_un_coup" function)
#modified the "verifier_deplacement" function so it's the only required boolean for
the first test of "jouer_un_coup"
#It also now check if the inputs are between 0 and 2
#now prints error messages corresponding to the wrong moves(for a lighter "jouer_un_coup" function)
-"dessine_plateau":
#ONLY IN THIS FILE: put the "plus_grand" variable outside of the for loop because its value is fixed
#replaced that weird ("Tour"+' '+) with just ("Tour "+)
-"dessine_disque":
#got rid of the unnecessary loop for the "a" variable because the value is fixed and
we know what it's going to be(value of the last parameter of range-1).
-"lire_coords":
#added ": " after "depart" and "arrivee" for a better UI
#got rid of the "tourarrivee" variable which isn't used at all in the function
#with the comments in the "verifier_deplacement", the "lire_coords" function is
lighter and display error messages accordingly
-"Dernier_coup":
#added the missing scenario where dernier=avant_dernier leading to a message
error if the user was doing a move, undoing it, then doing the same move and then
try to undo it again
-"annuler_dernier_coup":
#Change the return value of list(coups[coup]) into a deep copy
so we don't need to make a deepcopy of it in the "boucle_jeu" function
#Added "coup" as a second return value, so we don't need to
change it in the "boucle_jeu" function, it's automatic
------------------"boucle_jeu":---------------------------------------------------
#Change the initial value of "coup" from 1 to 0(the starting setup isn't a move)
#Changed the "reflect" variable, so if we start with 0 move and print the solution, it doesn't create
an error because of a division by 0 (due to the previous comment)
#Changed the placement of the "coup" incrementation in the while loop accordingly to the previous comment
#Fixed the "coups" dictionary being initialised manually instead of using the "init" function
#Fixed the limit of moves being 20, because it makes it impossible to win with a lot of disks
#Changed the value from 20 to ((2**n)-1)+3*n with (2**n)-1 being the minimum amount of moves to win(perfect play)
and 3*n being our margin of error, increasing or decreasing depending on the difficulty for fairness
#Got rid of the "win" variable/boolean and replaced it with "verifier_victoire" function call
#ONLY IN THIS FILE: got rid of the "a" variable being unecessary (a=deepcopy then coups=a is
just equal to coups=deepcopy)
#ONLY IN THIS FILE: got rid of the "tr.listen()" that I added, I will use it once I understand buttons or key inputs
#With the changes of the "annuler_dernier_coup" function, the undo part of "boucle_jeu" is lighter with plateau and
coup-1 being the return values of "annuler_dernier_coup"
#Changed the time_play and reflect time to a rounded value (rounded at the hundredth of second)
-------------------------MAIN PROG---------------------------------------------
#Changed the main prog so if we just print the solution, it doesn't save it in the score files
'''

#A-1: Initialisation--------------------------V
def init(n):
    t0=[]
    t1=[]
    t2=[]
    for k in range (n,0,-1):
        t0.append(k)
    plateau=[t0,t1,t2]
    return plateau
#A-2: Number of disks on selected tower--------------------------V
def nombre_disques(plateau,numtour):
    tower=plateau[numtour]
    return len(tower)
#A-3: Top disk of selected tower--------------------------V
def disque_superieur(plateau,numtour):
    if nombre_disques(plateau,numtour)!=0:
        tower=plateau[numtour]
        return tower[-1]
    return -1
#A-4: Position of a certain disk on the board--------------------------V
def position_disque(plateau,numdisque):
    for k in range (3):
        if numdisque in plateau[k]:
            return k
#A-5:Move verification--------------------------V
def verifier_deplacement(plateau,nt1,nt2):
    if not (0<=nt1<=2 and 0<=nt2<=2):
        print("Selected towers out of range, please select towers between 0 and 2.")
        return False
    dt1=disque_superieur(plateau,nt1)
    if dt1==-1:
        print("The starting tower has no disk, select another one.")
        return False
    dt2=disque_superieur(plateau,nt2)
    if dt2==-1:
            return True
    return dt1<dt2
#A-6:Victory check--------------------------V
def verifier_victoire(plateau,n):
    debut=init(n)
    return debut[0]==plateau[2]
#B:Turtle Move no drawing-------------------------V
def move(x,y):
    tr.up()
    tr.goto(x,y)
    tr.down()
#B:Draw a rectangle-----------------------------V
def rec(a,b):
    for i in range(2):
        tr.forward(a)
        tr.left(90)
        tr.forward(b)
        tr.left(90)
#B:Draw a rectangle with a specific color------------------------V
def reccolor(a,b,pencolor,color):
    tr.begin_fill()
    tr.color(pencolor,color)
    rec(a,b)
    tr.end_fill()  
#B-1:Draw the towers-----------------------------
def dessine_barre(indtour,n,level):
    tour=indtour+1
    plus_grand=(40+30*(n-1))
    go_to_which_tour=20*tour + plus_grand * ( tour -1)
    move(-300 + go_to_which_tour + (plus_grand-10)/2,-200+20+level*20)
    rec(10,20*n+20-level*20)
#Draw the board-----------------------------------
def dessine_plateau(n):
    move(-300,-200)
    reccolor(20*4 + (40+30*(n-1))*3,20,'black','blue')
    plus_grand=(n-1)*30+40
    for tour in range(1,4):
        move(-300+20*tour + plus_grand * (tour-1)+(plus_grand-10)/2+5 ,-200+10)
        tr.write("Tour "+str(tour-1),align='center',font=("Comic Sans MS", 20, "bold"))
#B-2:Draw a disk------------------------
def dessine_disque(nd, plateau, n):
    plus_grand= (n-1)*30+40  
    tour=position_disque(plateau,nd)+1
    go_to_which_tour=20*tour + plus_grand * ( tour -1 )
    difference_between_2_disques= 15*(n-nd)
    a=plateau[position_disque(plateau,nd)].index(nd) #all the disques below
    move(-300 +go_to_which_tour+ difference_between_2_disques, -200+20+20*a)
    reccolor(40+(nd-1)*30,20,'black','green')
#B-3:Erase a disk-----------------------------------
def efface_disque(nd, plateau, n):
    dessine_disque(nd,plateau,n)
    reccolor(40+(nd-1)*30,20,'white','white')
    tour=plateau[position_disque(plateau,nd)]
    tr.pencolor('black')
    if len(tour)==1:
        dessine_plateau(n)#if the tower just has 1 disque, we have to redraw the plateau
    else:
        dessine_disque(tour[tour.index(nd)-1],plateau,n)#redraw thing below
    a=tour.index(nd)
    dessine_barre(position_disque(plateau,nd),n,a) #redraw barre
#B-4:Draw the board setup-----------------------------------
def dessine_config(plateau, n):
    for i in range(3):
        dessine_barre(i,n,0)
    for i in range(1,n+1):
        dessine_disque(i,plateau,n)
    for tour in range(1,4):
        plus_grand=(n-1)*30+40
        move(-300+20*tour + plus_grand * (tour-1)+(plus_grand-10)/2+5 ,-200+10)
        tr.write("Tour "+str(tour-1),align='center',font=("Comic Sans MS", 20, "bold"))
#B-5:Erase Everything-----------------------------------------
def efface_tout(plateau, n):
    for i in range(1,n+1):
        efface_disque(i,plateau,n)
    dessine_plateau(n)
#C-1: Valid inputs and move--------------------------
def lire_coords(plateau):
    depart=int(input('Depart: '))
    arrivee=int(input('Arrivee: '))
    tourdepart = plateau[depart]
    while not verifier_deplacement(plateau,depart,arrivee):
        print("Ce coup est impossible.")
        depart=int(input('Depart: '))
        arrivee=int(input('Arrivee: '))
        tourdepart = plateau[depart]
    return depart,arrivee
#C-2:Make a move---------------------------------
def jouer_un_coup(plateau,n):
        dep,end=lire_coords(plateau)
        nd=disque_superieur(plateau,dep)
        efface_disque(nd,plateau,n)
        tdep=plateau[dep]
        tend=plateau[end]
        tend.append(tdep.pop(-1))
        dessine_disque(nd,plateau,n)
        tr.update()
        return dep,end
#D-1:Return the Last Move--------------------------------------
def dernier_coup(coups,coup):
    dernier=coups[coup]
    avantdernier=coups[coup-1]
    if dernier==avantdernier:
        return coups[coup][0],coups[coup][1]
    for i in range(3):
        if len(dernier[i])> len(avantdernier[i]):#If my tower went from nb to nb+1, it's my end tower
            end=i
        if len(dernier[i])< len(avantdernier[i]):#If my tower went from nb to nb-1, it's my starting tower
            dep=i
    return dep,end
#D-2:Cancel the last move--------------------------------
def annuler_dernier_coup(coups,coup):
    tourend,tourdep=dernier_coup(coups,coup)
    nd=disque_superieur(coups[coup],tourdep)
    efface_disque(nd,coups[coup],n)
    tdep=coups[coup][tourdep]
    tend=coups[coup][tourend]
    tend.append(tdep.pop(-1))
    dessine_disque(nd,coups[coup],n)
    coup=coup-1
    coups.popitem()
    return copy.deepcopy(list(coups[coup])),coup
#C-3:Game Loop----------------------------------------------
def boucle_jeu(plateau,n):
    start_time=time.time()
    coup=0
    restant=((2**n)-1)+3*(n-1)
    coups={coup:init(n)}
    while coup<restant and not verifier_victoire(plateau,n):
        coup=coup+1
        print('Coup numero',coup)
        print("Coups restants:",restant-coup)
        dep,end=jouer_un_coup(plateau,n)
        nd=disque_superieur(plateau,end)
        coups[coup]=copy.deepcopy(plateau)
        print('Je deplace le disque',nd,'de la tour',dep,'a la tour',end)
        undo=input('undo?')
        if undo=='yes' or 'oui':
            plateau,coup=annuler_dernier_coup(coups,coup)
        tr.update()
    time_play=round((time.time()-start_time),2)
    if coup!=0:
        reflect=round((time_play/coup),2)
    else:
        reflect=0
    return coup,verifier_victoire(plateau,n),coups,time_play,reflect
#SAVE 1 NEW ENTRY IN THE SCOREBOARD------------------------------------------------------------
def save(nom,n,coup,date,time_play,liste,reflect):
    liste.append({'nom':nom,'n':n,'coup':coup,'date':date,'time_play':time_play,'reflect_time':reflect})
    sorted_list=sortscoreboard(liste)
    with open('scores', 'wb') as handle:
        pickle.dump(sorted_list, handle)
#LIST OF THE ENTIRE SCOREBOARD-----------------------------------------------------------
def listcoreboard():
    with open('scores', 'rb') as a:
        list_score_board = pickle.load(a)
    nom=[]
    disque=[]
    date=[]
    time_play=[]
    coup=[]
    reflect=[]
    for i in list_score_board:
        nom.append(i['nom'])
        disque.append(i['n'])
        coup.append(i['coup'])
        date.append(i['date'])
        time_play.append(i['time_play'])
        reflect.append(i['reflect_time'])
    maxlennom=0
    for e in nom:
        if len(e)>=maxlennom:
            maxlennom=len(e)
    print('Nom',' '*(maxlennom),end='')
    print('Disque',' '*3,'Coup',' '*10,'Date',' '*10,'Timeplay',' '*3,'Relect time')
    for k in range(len(nom)):   
        print(nom[k],' '*(maxlennom+3-len(nom[k])),end='  ')
        print(disque[k],' '*7,coup[k],' '*2,date[k],' '*2,time_play[k],' '*7,reflect[k])
#SORT THE SCOREBOARD----------------------------------------------------------------
def sortscoreboard(liste):
    a=sorted(liste, key = lambda x : x['n'],reverse=True)
    b=sorted(a,key=lambda y: y['coup'])
    return b
#RECURSIVE FUNCTION FOR SOLUTION-----------------------------------------------
def automatique(n,dep,end,aux,listautomatique):
    if n==1:
        listautomatique.append([int(dep),int(end)])
    else:
        automatique(n-1,dep,aux,end,listautomatique)
        automatique(1,dep,end,aux,listautomatique)
        automatique(n-1,aux,end,dep,listautomatique)
    return listautomatique
#SOLUTION ONE MOVE AFTER ANOTHER (moves in a list)--------------------------------
def solution(li,n,plateau):
    tr.clear()
    dessine_plateau(n)
    dessine_config(plateau,n)
    print("Press Enter to see the next move")
    for i in li:
        input()
        dep=i[0]
        end=i[1]
        nd=disque_superieur(plateau,dep)
        print("Moving the disk #",nd," from ",dep," to ",end,sep="")
        time.sleep(0.2)
        efface_disque(nd,plateau,n)
        tr.update()
        tdep=plateau[dep]
        tend=plateau[end]
        tend.append(tdep.pop(-1))
        time.sleep(0.3)
        dessine_disque(nd,plateau,n)
        tr.update()
    print("Done!")
#INTERACTIVE SOLUTION OPTION----------------------------------------------
def seesolution(n):
    listautomatique=[]
    plateau=init(n)
    ans=input('Do you want to see the solution? \n')
    if (ans=='yes' or ans=='oui'):
        lll=automatique(n,0,2,1,listautomatique)
        solution(lll,n,plateau)
    return ans=='yes'
#MAIN PROG----------------------------------------------------------
print('Bienvenue dans les Tours de Hanoi ')
n=int(input('Combien de disques? \n'))
tr.tracer(0)
p=init(n)
tr.setworldcoordinates(-300-5, -200, -300+20*4 + (40+30*(n-1))*3, -200+20*(n+2))
dessine_plateau(n)
dessine_config(p,n)
sol=seesolution(n)
if not sol:
    tr.hideturtle()
    coup,win,coups,time_play,reflect=boucle_jeu(p,n)
    with open('Scores', 'rb') as a:
        scoreboard = pickle.load(a)
    if win:
        print('You win after',coup,'moves')
        time=time.ctime()
        tr.clear()
        move((-305+(-300+20*4 + (40+30*(n-1))*3))/2,(-200+(-200+20*(n+2)))/2)
        tr.write("YOU WON! ",align='center',font=("Comic Sans MS", 60, "bold"))
        nom=input('your name? ')
        save(nom,n,coup,str(time),str(time_play),scoreboard,reflect)
        listcoreboard()    
    else:
        print('out of moves')
        tr.clear()
        move((-305+(-300+20*4 + (40+30*(n-1))*3))/2,(-200+(-200+20*(n+2)))/2)
        tr.write("YOU LOST! ",align='center',font=("Comic Sans MS", 60, "bold"))
        seesolution(n)

