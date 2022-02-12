#!/usr/bin/env python
# coding: utf-8

# # Fintech Homework3
# Author: alanhc(曾宏鈞)
# 
# ID: r10944007
# 
# Date: 11/25
# ## env
# - python=3.9
# - sagemath

# ## Use the elliptic curve “secp256k1” as Bitcoin and Ethereum. Let G be the base point in the standard. Let d be the last 4 digits of your student ID number.

# <img src="../img/secp256k1.png" alt="drawing" width="50%"/>

# In[10]:


"""
參考上課ppt，使用uncompressed form建構橢圓曲線（y^2 = x^3 + 7）
"""
d = 4007
## prime field size
p = 2^256-2^32-2^9-2^8-2^7-2^6-2^4-1
## 橢圓曲線係數
a = 0
b = 7

EC = EllipticCurve(GF(p), [a,b])
print(EC)
## 定義base point
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798  #前128位元
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8  #後128位元
G = EC(GX, GY)


# ## 1. Evaluate 4G.
# 

# In[11]:


print("1. 4G:\n", 4*G)


# ## 2. Evaluate 5G.

# In[12]:


print("2. 5G:\n", 5*G)


# ## 3. Evaluate Q = dG, d=944007

# In[13]:


Q = d*G
print("3. dG:\n", Q)


# ## 4. With standard Double-and Add algorithm for scalar multiplications, how many doubles and additions respectively are required to evaluate dG?

# In[14]:


print(d, "binary:", bin(d)[2:])
_double = 0
_add = 0
# 從左到右，第一位不看
# 遇到1 double & add
# 遇到0 double
for i in str(bin(d))[3:]:
    if (i=='1'):
        _double+=1
        _add+=1
    else:
        _double+=1
print("double:", _double)
print("add:", _add)


# ## 5. Note that it is effortless to find −P from any P on a curve. If the addition of an inverse point is allowed, try your best to evaluate dG as fast as possible. Hint: 31P = 2(2(2(2(2P)))) −P.

# In[15]:


"""
根據Hint:
(原本)
31 = (11111)
這樣會做 4(double)+4(add)
但若是化簡成32-1，會變成
5(double) - 1
因為減法比加法快（直接算-P）
所以演算法為
1. 找到大於n的最大2的次方 2^max_n
2. 2^max_n - n  = remain
3. 使用remain找小於remain的2次方相減，直到remain = 0
"""
myID_bin = str(bin(d))[2:]
max_digit = len(myID_bin)

diff = 1<<max_digit 
diff -= d
diff_b = str(bin(diff))[2:]
ans_sub = []
i=len(diff_b)-1
for c in diff_b:
    if (c=="1"):
        ans_sub.append(i)
    i-=1

print("double:", max_digit)
print("substract:", len(ans_sub))
print("2^%s - 2^%s"%(max_digit,ans_sub))
ans = 0
for i in ans_sub:
    ans+=2^i
2^20 - ans


# ## Take a [Bitcoin transaction](https://www.blockchain.com/btc/tx/2b923c531fb2bb07bebdd160867c61ffce3a355988b17eae068cdf4b9f5eac6f) as you wish. 
# <img src="../img/transaction.PNG" alt="drawing" width="80%"/>
# 
# ## 6. Sign the transaction with a random number k and your private key d
# 

# <img src="../img/signing.PNG" alt="drawing" width="50%"/>

# In[16]:


import hashlib
from sage.rings.finite_rings.integer_mod import IntegerMod

n = G.order()
m = b"R10944007"
# step 1
my_e = hashlib.sha256(m).hexdigest()
e = 0x2b923c531fb2bb07bebdd160867c61ffce3a355988b17eae068cdf4b9f5eac6f  #上面截圖的hash
# step 2 找最左邊Ln個bit
Ln = 44
z = bin(e)[2:2+Ln]
# step 3
while(True):    
    k = ZZ.random_element(n)
    # step 4
    x1, y1, _ = k*G
    # step 5 (r = x1 mod n)
    r = IntegerMod(GF(n), x1)
    # step 6
    k_inver = pow(k, -1, n)
    s = IntegerMod(GF(n), k_inver * (int(z, 2)+r*d))
    if r!=0 and s!=0:
        print("result: (r,s)=(\n%s,\n%s\n)"%(hex(r), hex(s)))
        break


# <img src="../img/verification.png" alt="drawing" width="50%"/>

# ## 7. Verify the digital signature with your public key Q.

# In[17]:


# step 1
if (r<1 or r>n-1 or
    s<1 or s>n-1 ):
    print("error")
# step 2
e = 0x2b923c531fb2bb07bebdd160867c61ffce3a355988b17eae068cdf4b9f5eac6f
# step 3
Ln = 44
z = bin(e)[2:2+Ln]
# step 4
w = pow(s, -1, n) # 計算乘法反元素s^-1 mod n
# step 5
u1 = int(z,2)*w % n #IntegerMod(GF(n), int(z,2)*w)
u2 = r*w % n #IntegerMod(GF(n), r*w)
# step 6
x1, x2, _ = int(u1)*G+int(u2)*Q
# step 7
if (r == IntegerMod(GF(n), x1)):
    print("succeed!")
else:
    print("faild...")


# <img src="../img/lagrange.png" alt="drawing" width="50%"/>
# <img src="../img/lagrange2.png" alt="drawing" width="50%"/>

# ## 8. Over Z10007, construct the quadratic polynomial p(x) with p(1) = 10, p(2) = 100, and p(3) = 944007.

# In[18]:


points = [(1,10), (2,100), (3,d)]
print(points)
F = GF(10007) # 有限體
R = F['x']
R.lagrange_polynomial(points) # 用 sage內建 lagrange_polynomial 解


# ## ref
# - https://en.bitcoin.it/wiki/Secp256k1
# - https://ask.sagemath.org/question/39732/lagrange-interpolation-over-a-finite-field/
