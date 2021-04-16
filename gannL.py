#GeneticAlgorithm
import random
import numpy as np
import copy
import myStringLib as ms
import time
import NeuralNetwork as nn
import MathS as mas

class Crossover:

    def __init__(self,genes='randN',ranges=(-1,1),types='float'):
        self.genes=genes
        self.ranges=ranges
        self.types=types


    def getRandomGens(self,genes='randN',ranges=(-1,1),types='int'):

        if genes=='randN':
            if types=='int':
                return random.randint(ranges[0],ranges[1])
            elif types=='float':
                return random.uniform(ranges[0],ranges[1])
            else:
                return random.uniform(ranges[0],ranges[1])
        else:
            return random.choice(genes)
    

    def one_point(self,parent1,parent2):

        length=len(parent1)
        if length>1:
            r=random.randint(1,length-1)

            c1=[]
            #c2=[]

            c1.extend(parent1[:r])
            #c2.extend(parent2[:r])

            c1.extend(parent2[r:])
            #c2.extend(parent1[r:])

            return c1
        else:
            r=random.randint(0,1)
            if r==0:
                return parent1
            else:
                return parent2

    def two_point(self,parent1,parent2):
        length=len(parent1)

        if length>3:
                
            r1=random.randint(1,int(length/2)-1)
            r2=random.randint(int(length/2),length)

            c1=[]
            c2=[]
            
            c1.extend(parent1[:r1])
            #c2.extend(parent2[:r1])

            
            c1.extend(parent2[r1:r2])
            #c2.extend(parent1[r1:r2])

            
            c1.extend(parent1[r2:])
            #c2.extend(parent2[r2:])

            
            return c1
        else:
            return self.one_point(parent1,parent2)
        
    def uniform_point(self,parent1,parent2):

        length=len(parent1)

        c1=[]
        #c2=[]
        for i in range(length):
            d1=parent1[i]
            d2=parent2[i]
            if i%2==0:
                c1.append(d1)
                #c2.append(d2)
            else:
                c1.append(d2)
                #c2.append(d1)

        return c1
    
    def whole_arithmetic(self,parent1,parent2):

        c1=[]
        
        
        for d1,d2 in zip(parent1,parent2):

            d3=(d1+d2)/2
            
            c1.append(d3)
        #c2=copy.deepcopy(c1)
        return c1
    

    def self_generator(self,parent1,parent2):
        length=len(parent1)

        c1=[]
        #c2=[]

        for i in range(length):
            r=random.randint(0,1)
            if r==0:
                c1.append(parent1[i])
                #c2.append(parent2[i])
            else:
                c1.append(parent2[i])
                #c2.append(parent1[i])

        return c1

    def self_generator2(self,parent1,parent2):
        length=len(parent1)

        c1=[]
        #c2=[]        

        for i in range(length):
            r=random.randint(0,2)
            if r==0:
                c1.append(parent1[i])
                #c2.append(parent2[i])
            elif r==1:
                d=self.getRandomGens(self.genes,self.ranges,self.types)
                c1.append(d)
                #c2.append(d)
            else:
                c1.append(parent2[i])
                #c2.append(parent1[i])
        return c1
c=Crossover()


class Mutation:

    def __init__(self,genes='randN',ranges=(-1,1),types='float'):
        self.genes=genes
        self.ranges=ranges
        self.types=types


    def getRandomGens(self,genes='randN',ranges=(-1,1),types='float'):

        if genes=='randN':
            if types=='int':
                return random.randint(ranges[0],ranges[1])
            elif types=='float':
                return random.uniform(ranges[0],ranges[1])
            else:
                return random.uniform(ranges[0],ranges[1])
        else:
            return random.choice(genes)

    def bit_flip(self,chrom):
        length=len(chrom)

        r=random.randint(0,length-1)


        chrom[r]=self.getRandomGens(self.genes,self.ranges,self.types)

        return chrom


    def random_all_reset(self,chrom):
        ch=[]

        for i in chrom:
            r=random.randint(0,1)

            if r==0:
                ch.append(i)
            else:
                ch.append(self.getRandomGenes(self.genes,self.ranges,self.types))

        return ch

    def swap(self,chrom):

        length=len(chrom)

        r1=random.randint(0,length-1)
        r2=random.randint(0,length-1)

        temp1=chrom[r1]
        chrom[r1]=chrom[r2]
        chrom[r2]=temp1

        return chrom
    





    def scramble(self,chrom):
        random.shuffle(chrom,random.random)

        return chrom
    
    def inverse(self,chrom):

        return chrom[::-1]




    
m=Mutation()


class OffSpring:

    def __init__(self):
        self.c=Crossover()
        self.m=Mutation()

        self.cFun=None
        self.mFun=None
    


    def genOffSpring(self,pn1,pn2,gens,cFun=None,mFun=None):
        self.cFun=cFun
        self.mFun=mFun

        self.c=Crossover(gens)
        self.m=Mutation(gens)
        
        chrom=self.crossOver(pn1,pn2)
        mut=self.mutate(chrom)
        return mut
        
        

    def genOffSpringNN(self,pn1,pn2,cFun=None,mFun=None):
        self.cFun=cFun
        self.mFun=mFun
        

        ob1=pn1.output_bias
        ow1=pn1.output_weight

        ob2=pn2.output_bias
        ow2=pn2.output_weight

        newPn=nn.NeuralNetwork([pn1.trained_input[0]]\
                               ,[pn1.trained_output[0]]\
                               ,pn1.no_of_hidden_layer,\
                               pn1.perceptron_Array,2,pn1.learning_rate,show_per=False)
        
        

        self.cMhb(pn1,pn2,newPn)
        self.cMhw(pn1,pn2,newPn)
        self.cMob(pn1,pn2,newPn)
        self.cMow(pn1,pn2,newPn)


        return newPn

    def crossOver(self,p1,p2):
        if self.cFun==None:
            d=self.c.self_generator(p1,p2)
            return d
        else:
            return self.cFun(p1,p2)

    def mutate(self,co):
        if self.mFun==None:
            f=self.m.bit_flip(co)
            return f
        else:
            return self.mFun(co)

    def cMhb(self,p1,p2,n1):
        hb1=p1.hidden_bias
        hb2=p2.hidden_bias
        for i in range(len(hb1)):
            bias=hb1[i]
            for j in range(len(bias)):
                p1=hb1[i][j]
                p2=hb2[i][j]
                co=self.crossOver(p1,p2)
                mut=np.array(self.mutate(co))

                n1.hidden_bias[i][j]=mut

    def cMhw(self,p1,p2,n1):
        hb1=p1.hidden_weight
        hb2=p2.hidden_weight
        for i in range(len(hb1)):
            bias=hb1[i]
            for j in range(len(bias)):
                p1=hb1[i][j]
                p2=hb2[i][j]
                co=self.crossOver(p1,p2)
                mut=np.array(self.mutate(co))

                n1.hidden_weight[i][j]=mut


    def cMob(self,p1,p2,n1):
        b1=p1.output_bias
        b2=p2.output_bias

        for i in range(len(b1)):
            db1=b1[i]
            db2=b2[i]

            co=self.crossOver(db1,db2)
            mut=np.array(self.mutate(co))
            n1.output_bias[i]=mut

    def cMow(self,p1,p2,n1):
        b1=p1.output_weight
        b2=p2.output_weight

        for i in range(len(b1)):
            db1=b1[i]
            db2=b2[i]

            co=self.crossOver(db1,db2)
            mut=np.array(self.mutate(co))
            n1.output_weight[i]=mut
    
                

class Fitness:

    def __init__(self):
        pass

    def fitness(self,target,solution):
        score=0
        for i ,j in zip(target,solution):
            if i==j:
                score=score+1

        return score

    def fitnessNN(self,n):

        return n.fitness1

class GeneticAlgorithm:

    def __init__(self,generation="Inf",function=None):

        self.function=function

        
        self.o=OffSpring()
        self.f=Fitness()
        
        self.generation='Inf'
        self.genN=0
        self.population=[]
        self.found=False
        
        self.current=0
        

    def initPop(self,gens,target,populationSize):
        self.populationSize=populationSize
        self.gens=gens
        self.target=target
        self.c=Crossover(gens)
        length=len(self.target)
        for i in range(self.populationSize):

            c=[self.c.getRandomGens(gens) for d in range(length)]
            self.population.append(c)

    def initNNPop(self,nns,populationSize):
        self.nnSample=copy.deepcopy(nns)
        self.populationSize=populationSize
        for i in range(self.populationSize):
            
            n=nn.NeuralNetwork([self.nnSample.trained_input[0]],[self.nnSample.trained_output[0]],self.nnSample.no_of_hidden_layer,\
                               self.nnSample.perceptron_Array,1,self.nnSample.learning_rate,show_per=False)

            self.population.append(n)
        

    def changeGenNN(self,parentNum=10):
        pop=sorted(self.population,key=lambda x:self.f.fitnessNN(x))[::-1]

        new_gen=[]
        
        
        print('generation',self.genN)
        new_gen.extend(pop[:parentNum])

        

        

        for i in range(len(self.population)-parentNum):

            p1=copy.deepcopy(random.choice(self.population[:parentNum]))
            p2=copy.deepcopy(random.choice(self.population[:parentNum]))

            child=self.o.genOffSpringNN(p1,p2)
            new_gen.append(child)
        
        
        
        
        self.genN=self.genN+1

        self.population=new_gen

    def changeGen(self):
        pop=sorted(self.population,key=lambda x:self.f.fitness(x,self.target))[::-1]

        new_gen=[]
        
        
        s=int((10*self.populationSize)/100)
        new_gen.extend(pop[:s])

        s=int((90*self.populationSize)/100)

        

        for i in range(s):
            #Why selection of previs makes difference
            p1=copy.deepcopy(random.choice(pop[:50]))
            p2=copy.deepcopy(random.choice(pop[:50]))

            child=self.o.genOffSpring(p1,p2,self.gens)
            new_gen.append(child)
        

        self.genN=self.genN+1

        self.population=new_gen
        
    def startGenNN(self):

        genVal=self.generation
        
        
        if genVal=='Inf':
            while True:
                if self.genN%1000==0:
                    time.sleep(3)
                self.changeGenNN()

                if self.function is not None:
                    s=self.function(self.population)
                    if s:
                        print("GOTTED")
                        break
        else:
            for i in range(self.genN,self.generation):
                self.changeGenNN()

                if self.function is not None:
                    s=self.function(self.population)
                    if s:
                        print("GOTTED")
                        break

    def startGen(self):

        genVal=self.generation

        if genVal=='Inf':
            while True:
                if self.genN%1000==0:
                    time.sleep(3)
                self.changeGen()
                d=self.population[0]

                if ms.mergeInString(d,'')==self.target:
                    print("Gotted the target")
                    break
                if self.function is not None:
                    self.function(self.population)
        else:
            for i in range(self.genN,self.generation):
                self.changeGen()
                d=self.population[0]

                if ms.mergeInString(d,'')==self.target:
                    print("Gotted the target")
                    break

                if self.function is not None:
                    self.function(self.population)



n=nn.NeuralNetwork([[1, 1, 1, 1, 1, 0, 1, 0, 0, 0]],[[0,1]],1,[15],1000,1)
#trained_input=[[1,0,0,1],[0,1,1,1],[1,1,1,0],[1,0,1,1],[0,0,0,1]]
#trained_output=[[1,1],[0,1],[1,0],[1,1],[0,1]]

def getScore(out1,out2):
    score=0
    for f1,f2 in zip(out1,out2):
        for i,j in zip(f1,f2):
            if i==j:
                score=score+1
    return score
    



def function(population):

    for fi in range(len(population)):
        ind=population[fi]
        value=random.randint(3,1000)
        trained_input=nn.convert_binary(value)
        out=ind.think_only(trained_input).tolist()[0]
        maxi=max(out)
        p=mas.checkPrime(value)
        index=out.index(maxi)

        if index==0:
            if p:
                sc=1
            else:
                sc=0
        else:
            if p:
                sc=0
            else:
                sc=1

        ind.fitness=sc
        print(value,index ==0,p)
        population[fi]=ind
    print()
    print("---------------------------------x-------------------------------------------")
    allScore=0
    for i in population:
        allScore=allScore+i.fitness
    if allScore==0:
        print(kkr)
    print(allScore)
    print()
    

    return False
