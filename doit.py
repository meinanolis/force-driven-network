import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

class node():
    def __init__(self,name):
        self.name=name
        self.x=nodes.loc[self.name,'xPos']
        self.y=nodes.loc[self.name,'yPos']
        self.edges_index=[]
        self.edges_target=[]
        self.edges_weight=[]
        for i in edges.index:
            s=edges.loc[i,'source']
            t=edges.loc[i,'target']
            if s == self.name or t == self.name:
                self.edges_index.append(i)
                self.edges_weight.append(edges.loc[i,'weight'])
            if s == self.name:
                self.edges_target.append(t)
            if t == self.name:
                self.edges_target.append(s)
    def abstossung(self,k=1):
        ''' k - coulombkonstanten '''
        Fx=[]
        Fy=[]
        for i in nodes.index:
            if i != self.name:
                x2=nodes.loc[i,'xPos']
                y2=nodes.loc[i,'yPos']
                r=(np.abs(x2-self.x)+np.abs(y2-self.y))
                if r<5:
                    fx=k*(x2-self.x)/r**3
                    fy=k*(y2-self.y)/r**3
                    Fx.append(fx)
                    Fy.append(fy)
        return np.sum(Fx),np.sum(Fy)
    def anziehung(self, D=.5):
        ''' D - Federkonstante '''
        Fx=[0]
        Fy=[0]
        for i,t,w in zip(self.edges_index,self.edges_target,self.edges_weight):
            tx=nodes.loc[t,'xPos']
            ty=nodes.loc[t,'yPos']
            fx=w*D*(tx-self.x)
            fy=w*D*(ty-self.y)
            Fx.append(fx)
            Fy.append(fy)
        return np.sum(Fx),np.sum(Fy)
    def oneStep(self,dt=1,m=1):
        Fx,Fy=self.abstossung()
        Fx2,Fy2=self.anziehung()
        Fx-=Fx2
        Fy-=Fy2
        sx=-Fx*dt**2/(2*m)
        sy=-Fy*dt**2/(2*m)
        nodes.loc[self.name,'xPos']=self.x+sx
        nodes.loc[self.name,'yPos']=self.y+sy
        return sx+sy

nodes=pd.DataFrame([],index=['A','B','C','D','E','A2','B2','C2','D2','E2','A3','B3','C3','A4','B4','C4','D4','E4','A5','B5','C5'],columns=['xPos','yPos'])
nodes['xPos']=[1,2,3,4,5,6,7,8,9,0,1,2,3,1,2,3,4,5,6,7,8]
nodes['yPos']=[1,1,1,1,2,1,1,1,1,1,2,2,2,3,3,3,3,3,3,3,3]

edges=pd.DataFrame([['A','B',.1],
                    ['A','C',.5],
                    ['B','C',.8],
                    ['B','D',.8],
                    ['A','D',.8],
                    ['E','E2',.1],
                    ['E2','A2',.8],
                    ['A2','B2',.1],
                    ['E','C2',.1],
                    ['B2','C2',.8],
                    ['B2','D2',.8],
                    ['A2','D2',.8],
                    ['A2','C2',.4],
                    ['A3','D',.1],
                    ['A3','B3',.8],
                    ['A3','C3',.4],
                    ['A4','B4',.5],
                    ['A4','C4',.7],
                    ['B4','D4',.2],
                    ['C4','E4',.9],
                    ['A5','B5',.4],
                    ['B5','C5',.7],
                    ['A5','C5',1],
                    ['E','A',.1],
                    ['A4','B',.1],
                    ['A4','A3',.2],
                    ['C','A5',.1],
                    ], columns=['source','target','weight'])

ss=True
ii=0
while ss:
    s=0
    ii+=1
    for nn in nodes.index:
        n=node(nn)
        s+=np.abs(n.oneStep())
    plt.plot([n.x],[n.y],'.r')
    print(ii,s)
    ss=s>.2
    

for i in edges.index:
    s=edges.loc[i,'source']
    t=edges.loc[i,'target']
    w=edges.loc[i,'weight']
    sx=nodes.loc[s,'xPos']
    sy=nodes.loc[s,'yPos']
    tx=nodes.loc[t,'xPos']
    ty=nodes.loc[t,'yPos']
    plt.plot([sx,tx],[sy,ty],'-k',linewidth=w)

for i in nodes.index:
    x=nodes.loc[i,'xPos']
    y=nodes.loc[i,'yPos']
    plt.plot([x],[y],'ro')
    plt.text(x,y,i)
plt.axis('equal')
plt.show()