# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2021

import copy
import numpy as np

class Polynomial2:
    def __init__(self,coeffs):
        self.coeffs = coeffs
        self.length = len(self.coeffs)

    def add(self,p2):
        
        p2_length = len(p2.coeffs)
        shorter_len = min(self.length, p2_length)
        new_coeffs = []

        for i in range(shorter_len):
            new_coeff = self.coeffs[i]^p2.coeffs[i]
            new_coeffs.append(new_coeff)

        index = shorter_len
        while index<p2_length:
            new_coeffs.append(p2.coeffs[index])
            index+=1
        
        while index<self.length:
            new_coeffs.append(self.coeffs[index])
            index+=1

        return Polynomial2(new_coeffs)


    # same as add since -1 is congruent to 1 mod 2
    def sub(self,p2):
        p2_length = len(p2.coeffs)
        shorter_len = min(self.length, p2_length)
        new_coeffs = []

        for i in range(shorter_len):
            new_coeff = self.coeffs[i]^p2.coeffs[i]
            new_coeffs.append(new_coeff)

        index = shorter_len
        while index<p2_length:
            new_coeffs.append(p2.coeffs[index])
            index+=1
        
        while index<self.length:
            new_coeffs.append(self.coeffs[index])
            index+=1

        return Polynomial2(new_coeffs)


    def mul(self,p2,modp=None):

        output = []
        intermediate = np.polynomial.polynomial.polymul(self.coeffs, p2.coeffs)
        intermediate = [1 if x%2==1 else 0 for x in list(intermediate)]
        if modp == None:
            return Polynomial2(list(intermediate))

        else:
            # do reduction
            # returns (quotient, remainder)
            if len(list(intermediate)) == 0:
                return Polynomial2([0])
            else:
                output = np.polynomial.polynomial.polydiv(list(intermediate), modp.coeffs)
                remainder = output[1]
                remainder = [1 if x%2==1 else 0 for x in remainder]
                return Polynomial2(remainder)
        
    def div(self,p2):
        q, r = np.polynomial.polynomial.polydiv(self.coeffs, p2.coeffs)
        q = [1 if x%2==1 else 0 for x in list(q)]
        r = [1 if x%2==1 else 0 for x in list(r)]
        return Polynomial2(q), Polynomial2(r)

    def __str__(self):

        output = ''
        # the reduction in each function will take care of the 
        # negative coefficients
        for i in range(self.length-1, -1, -1):
            if self.coeffs[i]>0:
                if output == '':
                    if i == 1:
                        if self.coeffs[i]>1:
                            output+= f"{self.coeffs[i]}x"
                        else:
                            output+= "x"
                    elif i == 0:
                        if self.coeffs[i]>1:
                            output+= f"{self.coeffs[i]}"
                        else:
                            output+= "1"
                    else:
                        if self.coeffs[i]>1:
                            output+= f"{self.coeffs[i]}x^{i}"
                        else:
                            output+= f"x^{i}"
                else:
                    if i == 1:
                        if self.coeffs[i]>1:
                            output+= f" + {self.coeffs[i]}x"
                        else:
                            output+= " + x"
                    elif i == 0:
                        if self.coeffs[i]>1:
                            output+= f" + {self.coeffs[i]}"
                        else:
                            output+= " + 1"
                    else:
                        if self.coeffs[i]>1:
                            output+= f" + {self.coeffs[i]}x^{i}"
                        else:
                            output+= f" + x^{i}"
        return output

    def getInt(p):
        # assuming that the msb is the coefficient of the highest power element
        if p.coeffs == []:
            return 0
        else:
            binary_string = "".join([str(x) for x in reversed(p.coeffs)])
            return int(binary_string,2)


class GF2N:
    affinemat=[[1,0,0,0,1,1,1,1],
               [1,1,0,0,0,1,1,1],
               [1,1,1,0,0,0,1,1],
               [1,1,1,1,0,0,0,1],
               [1,1,1,1,1,0,0,0],
               [0,1,1,1,1,1,0,0],
               [0,0,1,1,1,1,1,0],
               [0,0,0,1,1,1,1,1]]

    def __init__(self,x,n=8,ip=Polynomial2([1,1,0,1,1,0,0,0,1])):
        self.x = x
        self.n = n
        self.ip = ip
        self.p = self.getPolynomial2() # store number as polynomial2

    def add(self,g2):
        output = self.p.add(g2.p)
        return GF2N(output.getInt(), self.n, self.ip)

    def sub(self,g2):
        output = self.p.sub(g2.p)
        return GF2N(output.getInt(), self.n, self.ip)
    
    def mul(self,g2):
        if g2.p.getInt()==0 or self.p.getInt()==0:
            return GF2N(0, self.n, self.ip)
        else:
            output = self.p.mul(g2.p, modp = self.ip)
            return GF2N(output.getInt(), self.n, self.ip)

    def div(self,g2):
        q, r = self.p.div(g2.p)
        return GF2N(q.getInt(), self.n, self.ip), GF2N(r.getInt(), self.n, self.ip)

    def getPolynomial2(self):
        binary_x = bin(self.x).lstrip("0b")
        coeffs = [int(char) for char in reversed(binary_x)]
        return Polynomial2(coeffs)


    def __str__(self):
        return str(self.getInt())

    def getInt(self):
        return self.p.getInt()

    def mulInv(self):
        a = self.ip
        b = self.p
        t1 = Polynomial2([0])
        t2 =  Polynomial2([1])

        while b.getInt()>0:
            q, r = a.div(b)
            # t = t1 -t2 * q
            t = t1.sub(t2.mul(q, self.ip))
            a = copy.deepcopy(b)
            b = copy.deepcopy(r)
            t1 = copy.deepcopy(t2)
            t2 = t
        return GF2N(t1.getInt(), self.n, self.ip)

    def affineMap(self):
        coeffs = copy.deepcopy(self.p.coeffs)
        # make len of maxtrix = 8 by adding 0s
        for i in range(len(coeffs), 8):
            coeffs.append(0)

        intermediate = []
        # matrix multiplication of affinemat and coeffs
        for i in range(8):
            value = 0
            for j in range(8):
                value += self.affinemat[i][j] * coeffs[j]
            intermediate.append(value % 2)

        # add with (1, 1, 0, 0, 0, 1, 1, 0) mod 2
        p3 = Polynomial2(intermediate).add(Polynomial2([1, 1, 0, 0, 0, 1, 1, 0]))
        return GF2N(p3.getInt(), self.n, self.ip)

# with open('table1.txt', "w") as fout:
# 2^4 = 16
# table will be 16x16
table1 = [[] for i in range(16)]
for i in range(16):
    for j in range(16):
        table1[i].append(GF2N(i, n=4, ip=Polynomial2([1, 0, 0, 1, 1])).add(GF2N(j, n=4,ip=Polynomial2([1, 0, 0, 1, 1]))).getInt())

table2 = [[] for i in range(16)]
for i in range(16):
    for j in range(16):
        table2[i].append(GF2N(i, n=4, ip=Polynomial2([1, 0, 0, 1, 1])).mul(GF2N(j, n=4,ip=Polynomial2([1, 0, 0, 1, 1]))).getInt())

# using numpy to format the table
np.savetxt('table1_addition.txt', table1, fmt='% 3d', header="Addition")
np.savetxt('table1_multiplication.txt', table2, fmt='% 3d', header="Multiplication")

print('\nTest 1')
print('======')
print('p1=x^5+x^2+x')
print('p2=x^3+x^2+1')
p1=Polynomial2([0,1,1,0,0,1])
p2=Polynomial2([1,0,1,1])
p3=p1.add(p2)
print('p3= p1+p2 = ',p3)

print('\nTest 2')
print('======')
print('p4=x^7+x^4+x^3+x^2+x')
print('modp=x^8+x^7+x^5+x^4+1')
p4=Polynomial2([0,1,1,1,1,0,0,1])
# modp=Polynomial2([1,1,0,1,1,0,0,0,1])
modp=Polynomial2([1,0,0,0,1,1,0,1,1])
p5=p1.mul(p4,modp)
print('p5=p1*p4 mod (modp)=',p5)

print('\nTest 3')
print('======')
print('p6=x^12+x^7+x^2')
print('p7=x^8+x^4+x^3+x+1')
p6=Polynomial2([0,0,1,0,0,0,0,1,0,0,0,0,1])    
p7=Polynomial2([1,1,0,1,1,0,0,0,1])
p8q,p8r=p6.div(p7)
print('q for p6/p7=',p8q)
print('r for p6/p7=',p8r)

print ('\nTest 4')
print ('======')
g1=GF2N(100)
g2=GF2N(5)
print('g1 = ',g1.getPolynomial2())
print('g2 = ',g2.getPolynomial2())
g3=g1.add(g2)
print('g1+g2 = ',g3)

print ('\nTest 5')
print ('======')
ip=Polynomial2([1,1,0,0,1])
print ('irreducible polynomial',ip)
g4=GF2N(0b1101,4,ip)
g5=GF2N(0b110,4,ip)
print ('g4 = ',g4.getPolynomial2())
print ('g5 = ',g5.getPolynomial2())
g6=g4.mul(g5)
print ('g4 x g5 = ',g6.p)

print ('\nTest 6')
print ('======')
g7=GF2N(0b1000010000100,13,None)
g8=GF2N(0b100011011,13,None)
print ('g7 = ',g7.getPolynomial2())
print ('g8 = ',g8.getPolynomial2())
q,r=g7.div(g8)
print ('g7/g8 =')
print ('q = ',q.getPolynomial2())
print ('r = ',r.getPolynomial2())

print ('\nTest 7')
print ('======')
ip=Polynomial2([1,1,0,0,1])
print ('irreducible polynomial',ip)
g9=GF2N(0b101,4,ip)
print ('g9 = ',g9.getPolynomial2())
print ('inverse of g9 =',g9.mulInv().getPolynomial2())

print ('\nTest 8')
print ('======')
ip=Polynomial2([1,1,0,1,1,0,0,0,1])
print ('irreducible polynomial',ip)
g10=GF2N(0xc2,8,ip)
print ('g10 = 0xc2')
g11=g10.mulInv()
print ('inverse of g10 = g11 =', hex(g11.getInt()))
g12=g11.affineMap()
print ('affine map of g11 =',hex(g12.getInt()))
