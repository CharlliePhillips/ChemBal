from math import*
fucked = False
#from operator import truediv
#https://integratedmlai.com/basic-linear-algebra-tools-in-pure-python-without-numpy-or-scipy/
def zeros_matrix(rows, cols):
    """
    Creates a matrix filled with zeros.
        :param rows: the number of rows the matrix should have
        :param cols: the number of columns the matrix should have
 
        :return: list of lists that form the matrix
    """
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)
 
    return M

#https://medium.com/math-for-data-science/math-for-data-science-lecture-02-elementary-row-operations-via-python-46885a33a84c
def rref(M):
    ## If M is empty, no need to proceed, and just return
    #if not M: return
    ## if rows are less than column, lead variable used to check that, for every row increment, lead incremented by 1 and if its value greater than or equal to column count, return    
    lead = 0
    ## No of rows in Matrix
    rowCount = len(M)
    ## No of columns in Matrix
    columnCount = len(M[0])
    ## Iterating row of Matrix
    for r in range(rowCount):
        if lead >= columnCount:
            return
        i = r
        ## If leading element of that row itself 0, check next row's leading element if its zero or not
        while M[i][lead] == 0.0:
            i += 1
            if i == rowCount:
                i = r
                lead += 1
                if columnCount == lead:
                    return M
        ## Swap Rows i and r --> will happen only if lead element M[i][lead] equal to 0 and i is not equal to rowCount
        M[i],M[r] = M[r],M[i]
        lv = M[r][lead]
        ## Making Lead Entry -- 1
        M[r] = [ mrx / float(lv) for mrx in M[r]]
        ## Each column will have single Non-Zero entry
        for i in range(rowCount):
            if i != r:
                lv = M[i][lead]
                M[i] = [ iv - lv*rv for rv,iv in zip(M[r],M[i])]
        lead += 1
    return M

def getVect(S, E, M):
    vect  = []
    for i in range(0,len(E)):
        vect.append(0)
    for i in range(0,len(S)):
         if(S[i] in E):
             vect[E.index(S[i])] = S[i + 1]
    if not (len(vect) == len(M)):
        for i in range(len(E)-1,len(M)):
            vect.append(0)
    return vect

def hasFree(M):
    k = 0.0
    for i in range(0,len(M[0])):
        k = k + M[len(M)-1][i]
    if(k == 0.0):
        return True
    return False

def makeVect(M,C):
    vect = []
    for i in range(0,len(M[0])-1):
        #print("CHECK IT",C-1)
        vect.append(M[i][C-1])
    #print("vect",vect)
    return vect

def notSquare(M,R,P):
    zs = 0
    for i in range(0,len(M[0])):
        #print("what", M)
        if(M[len(M)-1][i] == 0):
            zs += 1
    if(zs == len(M[0])):
        for i in range(0,len(R)):
           #print("re 1s")
            M[len(M)-1][i] = 1
        for i in range(len(R),len(R) + len(P)):
            #print("p 1s")
            M[len(M)-1][i] = -1
        M[len(M)-1][len(M[0])-1] = 3
        fucked = True
        return M
    else:
        return M
       
def augment(M):
    for i in range(0,len(M)):
        M[i].append(0) 
    return M

def makeCoef(coef,c4,free, isFree):
    if(isFree):
        for i in range(0,len(coef)-1):
            coef[i] = int(c4[i] * free * -1)
    coef.remove(0)
    return coef    
    
def checkZeroColumn(list):
    zeroCount = 0
    for i in range(0,len(list)):
        if(list[i][len(list[0])-1]==0):
            zeroCount += 1
    if(zeroCount == len(list)):
        return True
    else:
        return False
def deepCopy(ulist,clist):
    for i in range(0,len(ulist)):
        clist.append(ulist[i])

def everyOther(string):
    out = ""
    i = 0
    while i < len(string):
        #print("steppin",out + string[i])
        out = out+string[i]
        i += 2
    #print("out:",out)
    return out

def asIntegerRatio(N):
    #print("n",N)
    for i in range(2,100):
        for j in range(1,100):
            #print(j/i)
            if (-1*N == j/i):
                #print(j,i)
                return (j,i)
    return (N,1)

print("Number of reactants?")
numReactants = int(input())
reactList = []
for i in range(0,numReactants):
    print("Reactant "  + str(i + 1) + "?")
    reactList.append(input())
print("Number of products?")
numProd = int(input())
prodList = []
for i in range(0,numProd):
    print("Product "  + str(i + 1) + "?")
    prodList.append(input())
#print(reactList)
#print(prodList)
#print
elements = []
for i in range(0,len(reactList)):
    #print(reactList)
    for j in range(0,len(everyOther(reactList[i]))):
        if not(everyOther(reactList[i])[j] in elements):
            elements.append(everyOther(reactList[i])[j])
#print(elements)
theMatrix = zeros_matrix(len(prodList) + len(reactList),len(prodList) + len(reactList))
for i in range(0,len(theMatrix[0])):
    if(i < len(reactList)):
        for j in range(0,len(theMatrix)):
            theMatrix[j][i] = float(getVect(reactList[i],elements,theMatrix)[j])
    if(i >= len(reactList) and i < len(reactList) + len(prodList)):
        for j in range(0,len(theMatrix)):
            #if statment to avoid -0
            if(float(getVect(prodList[i-len(reactList)],elements,theMatrix)[j]) > 0.0):
                theMatrix[j][i] = -1 * float(getVect(prodList[i-len(reactList)],elements,theMatrix)[j])
            else:
                theMatrix[j][i] = float(getVect(prodList[i-len(reactList)],elements,theMatrix)[j])

#print(theMatrix)
theMatrix = augment(theMatrix)
theMatrix = notSquare(theMatrix,reactList,prodList)

#print(theMatrix)
#print(rref(theMatrix))
rrefTheMatrix = rref(theMatrix)
coef = []
for i in range(0,len(theMatrix[0])):
    coef.append(0)
    
if(hasFree(rrefTheMatrix)):
    fuckingWacky = False     
    isFree = True
    #print(checkZeroColumn(theMatrix))
    if(checkZeroColumn(theMatrix) == False):      
        c4 = makeVect(rrefTheMatrix,len(rrefTheMatrix[0]))
        c4s = makeVect(rrefTheMatrix,len(rrefTheMatrix[0]))
    else:
        c4 = makeVect(rrefTheMatrix,len(rrefTheMatrix[0])-1)
        c4s = makeVect(rrefTheMatrix,len(rrefTheMatrix[0])-1)
    c4s.sort()
    #print("c4",c4)
    #print("c4s ", c4s)
    least = c4s[len(c4s)-2]
    free = asIntegerRatio(least)[1]
    if(free > 1000000000000000):
        free = int(free/1000000000000000)
        fuckingWacky = True
    #print(free)
    coef[len(coef)-1] = free
    #for i in range(0,len(coef)-1):
    #    coef[i] = int(c4[i] * free * -1)
    coef = makeCoef(coef,c4,free,isFree)
    #print("HERE",coef)
    if(fuckingWacky):
        coefs = []
        deepCopy(coef,coefs)
        #coefs = coef
        coefs.sort()
        #print("sorted mf",coefs)
        great = gcd(coefs[0],coefs[len(coefs)-1])
        #print("great",great)
        for i in range(0,len(coef)):
            coef[i] = int(coef[i]/great) 
    #print("wus it at",coef)
#this is so dumb, why can't i just import the fraction library on the nspire bruh
else:
    if(checkZeroColumn(theMatrix) == False):      
        c4 = makeVect(rrefTheMatrix,len(rrefTheMatrix[0]))
        c4s = makeVect(rrefTheMatrix,len(rrefTheMatrix[0]))
        mult = c4s[len(c4s)-1]
    else:
        c4 = makeVect(rrefTheMatrix,len(rrefTheMatrix[0])-1)
        c4s = makeVect(rrefTheMatrix,len(rrefTheMatrix[0])-1)
        mult = c4s[len(c4s)-2]
        
    isFree = False
    coef = makeCoef(coef,c4,0,isFree)
    for i in range(0,len(coef)):
        coef[i] *= mult
#print("coef = ",coef)
print("Your Balanced Equation is:")
#finally print the balanced equation
for i in range(0,len(reactList)):
    if not (i == len(reactList)-1):
        print("(",coef[i],")",reactList[i],end = ' + ')
    else:
        print("(",coef[i],")",reactList[i],end = ' > ')
for i in range(0,len(prodList)):
    if not (i == len(prodList)-1):
        print("(",coef[i + len(reactList)],")",prodList[i],end = ' + ')
    else:
        print("(",coef[i + len(reactList)],")",prodList[i],end = '')