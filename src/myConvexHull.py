from cmath import sqrt
import numpy as np
from math import sqrt, acos

class myConvexHull:
    
    def __init__ (self, points):

        self.points = points
        self.simplices = []
        self.sortedidx = self.quickSort([i for i in range(len(self.points))], 0, len(self.points)-1)
        n = len(self.sortedidx)
        self.Hull(self.sortedidx[0], self.sortedidx[n-1], self.sortedidx[1:n-1], True, True)

    def quickSort(self, idx, i, j):
        
        idx1 = [0 for l in range(len(idx))]
        for l in range(len(idx)):
            idx1[l] = idx[l]
        if i<j:
            idx1,k = self.Partisi(idx1, i, j)
            if (j!=k or idx!=idx1):
                idx1 = self.quickSort(idx1, i, k)
            if (i!=k+1 or idx!=idx1):
                idx1 = self.quickSort(idx1, k+1, j)
        return idx1

    def Partisi(self, idx, i, j):
        
        pivotx = self.points[idx[(i+j) // 2]][0]
        pivoty = self.points[idx[(i+j) // 2]][1]
        p = i
        q = j

        while (self.points[idx[p]][0] < pivotx) or (self.points[idx[p]][0] == pivotx and self.points[idx[p]][1] < pivoty):
            p = p + 1
        while (self.points[idx[q]][0] > pivotx) or (self.points[idx[q]][0] == pivotx and self.points[idx[q]][1] > pivoty):
            q = q - 1
        if p <= q:
            temp = idx[p]
            idx[p] = idx[q]
            idx[q] = temp
            p += 1
            q -= 1

        while (p<=q):
            while (self.points[idx[p]][0] < pivotx) or (self.points[idx[p]][0] == pivotx and self.points[idx[p]][1] < pivoty):
                p = p + 1
            while (self.points[idx[q]][0] > pivotx) or (self.points[idx[q]][0] == pivotx and self.points[idx[q]][1] > pivoty):
                q = q - 1
            if p <= q:
                temp = idx[p]
                idx[p] = idx[q]
                idx[q] = temp
                p += 1
                q -= 1

        return idx,q
    
    def Hull(self, i, j, idp, left, right): # i = idx[0] , j = idx[n] , idp = idx[1..n-1]
        if left:
            kiri = []
            for k in range(len(idp)):
                if self.det(i, j, idp[k])>0:
                    kiri.append(idp[k])
            if len(kiri)==0:
                self.addsimplices(i, j)
            else:
                p1 = np.array(self.points[i])
                p2 = np.array(self.points[j])
                p3 = np.array(self.points[kiri[0]])
                maxidx = 0 # in kiri
                maxd = abs(np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1))
                maxangle = self.angle(kiri[0], j, i)
                for k in range(1,len(kiri)):
                    p3 = np.array(self.points[kiri[k]])
                    p3distance = abs(np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1))
                    p3angle = self.angle(kiri[k], j, i)
                    if (p3distance > maxd) or (p3distance == maxd and p3angle > maxangle):
                        maxidx = k #in kiri
                        maxd = p3distance
                        maxangle = p3angle
                newkiri = []
                for l in range(len(kiri)):
                    if l!=maxidx:
                        newkiri.append(kiri[l])
                self.Hull(i, kiri[maxidx], newkiri, True, False)
                self.Hull(kiri[maxidx], j, newkiri, True, False)
        if right:
            kanan = []
            for k in range(len(idp)):
                if self.det(i, j, idp[k])<0:
                    kanan.append(idp[k])
            if len(kanan)==0:
                self.addsimplices(i, j)
            else:
                p1 = np.array(self.points[i])
                p2 = np.array(self.points[j])
                p3 = np.array(self.points[kanan[0]])
                maxidx = 0 # in kanan
                maxd = abs(np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1))
                maxangle = self.angle(kanan[0], j, i)
                for k in range(1,len(kanan)):
                    p3 = np.array(self.points[kanan[k]])
                    p3distance = abs(np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1))
                    p3angle = self.angle(kanan[k], j, i)
                    if (p3distance > maxd) or (p3distance == maxd and p3angle > maxangle):
                        maxidx = k #in kanan
                        maxd = p3distance
                        maxangle = p3angle
                newkanan = []
                for l in range(len(kanan)):
                    if l!=maxidx:
                        newkanan.append(kanan[l])
                self.Hull(i, kanan[maxidx], newkanan, False, True)
                self.Hull(kanan[maxidx], j, newkanan, False, True)
        return
            

    def det(self, i, j, k):
        ret = self.points[i][0]*self.points[j][1]
        ret += self.points[k][0]*self.points[i][1]
        ret += self.points[j][0]*self.points[k][1]
        ret -= self.points[k][0]*self.points[j][1]
        ret -= self.points[j][0]*self.points[i][1]
        ret -= self.points[i][0]*self.points[k][1]
        return ret

    def addsimplices(self, a, b): # a,b = idx[...]
        line = []
        line.append(a)
        line.append(b)
        self.simplices.append(line)

    def angle(self, i, j, k): # i,j,k = idx[...] , ret angle at k
        a = sqrt((self.points[i][0]-self.points[j][0])**2 + (self.points[i][1]-self.points[j][1])**2)
        b = sqrt((self.points[j][0]-self.points[k][0])**2 + (self.points[j][1]-self.points[k][1])**2)
        c = sqrt((self.points[k][0]-self.points[i][0])**2 + (self.points[k][1]-self.points[i][1])**2)
        temp = (b**2+c**2-a**2)/(2*b*c)
        if (round(temp,6)==1):
            temp = 1
        return abs(acos(temp))
        