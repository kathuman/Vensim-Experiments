from vpython import *
from random import *
# this code was writen by Paulo H. Acioli from 
# the Department of Physics and Astronomy
# of Northeastern Illinois University
# any use and publications that use this code or modifications
# should cite the manuscript arXiv:2003.11449 [physics.ed-ph]
# or the Published Version as Paulo H. Acioli, Am. J. Phys. XX, XXXX (2020).

def gasdev():
    g = 0
    while g == 0:
        v1 = 2.*random()-1.
        v2 = 2.*random()-1.
        r = v1**2 + v2**2
        if r <= 1. and r !=0:
            fac = sqrt(-2.*log(r)/r)
            gx = v1*fac
            gy = v2*fac
            g = 1
    return gx,gy
hab={}
nblocks = int(input('enter the number of simulations'))
nsteps = int(input('enter the total number of steps '))
rho  = float(input('enter the pop density hab/m^2 '))
Npop = int(input('enter the total population '))
D    = float(input('enter the diffusion constant '))
prob = float(input('enter prob of infection '))
rsafe = float(input('enter the safe distance'))
tinc  = float(input('enter incubation period in days'))
dt    = float(input('entertime step in units of day'))
# compute the size of the simulation cell
L = sqrt(Npop/rho)
scene = canvas(title='Corona',center=[L/2,L/2,0],background=color.white,width=800,height=800)
scene.range = L/2+20
cell = curve(pos=[(0,0,0),(0,L,0),(L,L,0),(L,0,0),(0,0,0)],color=color.black,thickness=0.1)

# create the population at random

avh = [0. for i in range(90)]
avi = [0. for i in range(90)]
avr = [0. for i in range(90)]
avh2 = [0. for i in range(90)]
avi2 = [0. for i in range(90)]
avr2 = [0. for i in range(90)]
for iblock in range(nblocks):
    healthy = []
    nhealthy =0
    nrec = 0
    for i in range(Npop):
        x = L*random()
        y = L*random()
        if iblock==0:
            hab[i] = sphere(pos=(x,y,0),radius=0.015*L)
        else:
            hab[i].color=color.white
        hab[i].health = 0
        hab[i].timeinf = 0.
        healthy.append(i)
        nhealthy +=1
    # chose at random 1% individuals in the population to be sick
    Nsick0 = int(0.01*Npop)
    sick = []
    ninf = 0
    for isick in range(Nsick0):
        ih = int(Npop*random())
        hab[ih].heath = 1
        hab[ih].color = color.red
        hab[ih].timeinf=tinc
        t = 0.
        if ih not in sick:
            sick.append(ih)
            healthy.remove(ih)
            nhealthy -=1
            ninf += 1
    for istep in range(nsteps):
        # move every individual and calculate their distances
        for i in range(Npop):
            xp = gasdev()
            hab[i].pos[0] = abs(hab[i].pos[0]+sqrt(2*D*dt)*xp[0])
            hab[i].pos[1] = abs(hab[i].pos[1]+sqrt(2*D*dt)*xp[1])
            if(hab[i].pos[0] > L): hab[i].pos[0] -= 2*sqrt(2*D*dt)*xp[0]
            if(hab[i].pos[1] > L): hab[i].pos[1] -= 2*sqrt(2*D*dt)*xp[1]
        for i in sick:
            hab[i].timeinf -= dt
            for j in healthy:
                dist = mag(hab[i].pos-hab[j].pos)
                if dist < rsafe:  # test if individuals are less than the safe distance
                    xt = random()
                    if xt < prob:
                        hab[j].heath = 1
                        hab[j].timeinf = tinc
                        hab[j].color = color.red
                        sick.append(j)
                        healthy.remove(j)
                        ninf += 1
                        nhealthy -= 1
            if hab[i].timeinf <=0:
                hab[i].health = 2
                hab[i].timeinf = 0
                hab[i].color=color.green
                sick.remove(i)
                nrec +=1
        if istep%100 ==0:
            ibox = int(istep/100)
            avh[ibox] += nhealthy
            avi[ibox] += ninf
            avr[ibox] += nrec
            avh2[ibox] += nhealthy**2
            avi2[ibox] += ninf**2
            avr2[ibox] += nrec**2
            
        t += dt
    print('Finished block %.0f of %.0f days'%(iblock,nsteps*dt))
print("Day  Heathy  Infec  Cured  sigma(H)  sigma(Inf) Sigma(cured)")
for i in range(90):
    stdevh = sqrt(avh2[i]/nblocks-(avh[i]/nblocks)**2)/sqrt(nblocks)
    stdevi = sqrt(avi2[i]/nblocks-(avi[i]/nblocks)**2)/sqrt(nblocks)
    stdevr = sqrt(avr2[i]/nblocks-(avr[i]/nblocks)**2)/sqrt(nblocks)
    print('%.0f %.3f %.3f %.3f %.3f %.3f %.3f' % (i , avh[i]/nblocks
                                                  , avi[i]/nblocks , avr[i]/nblocks,
                                                  stdevh,stdevi,stdevr))