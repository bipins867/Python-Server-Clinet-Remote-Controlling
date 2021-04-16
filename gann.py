#GANN
#Genetic Algorithms with Neural Network

import NeuralNetwork as nn
import numpy as np
import copy
import random
import time

class Individual:

    def __init__(self):
        pass


    def genOffSpring(self,pn1,pn2):


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
    
                
    def crossOver(self,chro1,chro2):
        #chro1 chromosome-1
        #chro2 chromosome-2
        
        child=[]

        for c1,c2 in zip(chro1,chro2):
            prob=random.random()

            if prob<0.30:
                child.append(c1)
            elif prob<0.90:
                child.append(c2)
            else:
                data=random.uniform(-1,1)
                child.append(data)
        
        return child

    def mutate(self,chrom):
        length=len(chrom)-1

        r1=random.randint(0,length)
        r2=random.randint(0,length)

        a1=chrom[r1]
        chrom[r1]=chrom[r2]
        chrom[r2]=a1

        return chrom

    def getFitness1(self,n):

        return n.fitness1

    def getFitness2(self,n):
        return n.fitness2

    def getFitness3(self,n):
        return n.fitness3
    

class GeneticAlgorithm:

    def __init__(self,nnSample,populationSize=100,generation="Inf",function=None):

        self.function=function
        self.nnSample=copy.deepcopy(nnSample)
        self.populationSize=populationSize
        self.generation='Inf'
        self.genN=0
        self.population=[]
        self.found=False
        self.ind=Individual()
        self.current=0

    def initilizePop(self):
        for i in range(self.populationSize):
            n=nn.NeuralNetwork([self.nnSample.trained_input[0]],[self.nnSample.trained_output[0]],self.nnSample.no_of_hidden_layer,\
                               self.nnSample.perceptron_Array,1,self.nnSample.learning_rate,show_per=False)

            self.population.append(n)
            

    def changeGeneration(self):
        ind=self.ind
        pop=sorted(self.population,key=lambda x:ind.getFitness2(x))[::-1]

        pop=sorted(self.population,key=lambda x:ind.getFitness3(x))


        pop=sorted(self.population,key=lambda x:ind.getFitness1(x))[::-1]

        
        new_gen=[]
        
        
        s=int((10*self.populationSize)/100)
        new_gen.extend(pop[:s])

        s=int((90*self.populationSize)/100)

        for i in range(s):
            p1=copy.deepcopy(random.choice(pop[:50]))
        
            p2=copy.deepcopy(random.choice(pop[:50]))

            child=ind.genOffSpring(p1,p2)
            new_gen.append(child)
        

        self.genN=self.genN+1

        self.population=new_gen
        
    def startGeneration(self):

        genVal=self.generation

        if genVal=='Inf':
            while True:
                if self.genN%1000==0:
                    time.sleep(3)
                self.changeGeneration()

                if self.function is not None:
                    self.function(self.population)
        else:
            for i in range(self.genN,self.generation):
                self.changeGeneration()

                if self.function is not None:
                    self.function(self.population)
n=nn.NeuralNetwork(nn.trained_input,nn.trained_output,4,[80,80,80,80],1000,1)
trained_input=[[1,0,0,1],[0,1,1,1],[1,1,1,0],[1,0,1,1],[0,0,0,1]]
trained_output=[[1,1],[0,1],[1,0],[1,1],[0,1]]

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
		out=ind.think_only(trained_input).tolist()
		to=[]
		for i in out:
			s=nn.sep_listData(i,0,1,0.5)
			to.append(s)
		out=to
		sc=getScore(out,trained_output)
		ind.fitness1=sc
		population[fi]=ind
	#print(population[0].fitness)
	population[0].output=np.round(population[0].output,3)
	output=population[0].output.tolist()
	out=[]
	for i in output:
		out.append(nn.sep_listData(i,0,1,0.5))
	print(trained_output)
	print(out)
	print("---------------------------")
