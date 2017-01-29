# Shredder - Unshredder
#
# As a response to Instagram Engineering Challenge:
# https://engineering.instagram.com/instagram-engineering-challenge-the-unshredder-7ef3f7323ab1#.dsmknhvq6
#
# The script intelligently detects shred width from supplied shredded image. No assumptions and hardcodings!
# Unshredder uses a simple SSD match to find the best fit to jigsaw puzzle.
#
# Debaditya Basak
# 01/28/2017
#
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt

#shredder

def mostCommon(l):
	d = {}
	for i in l:
		if i in d:
			d[i] += 1
		else:
			d[i] = 1
	idx = sorted(d, key = d.get, reverse = True)[0]
	print idx, float(d[idx])/l.size*100
	return np.asarray(([idx, float(d[idx])/l.size*100]), dtype='uint8')

cnt = 64
cntr = 0
im1 = cv2.imread('/Users/dbasak/Downloads/workspace_py/cvip/duck_gs.png',cv2.IMREAD_GRAYSCALE)
out = im1[::1,:im1.shape[1]-(im1.shape[1]%cnt)+1:1]
for i in random.sample(xrange(0,cnt),cnt):
	disp = out[::1,i*(out.shape[1]/cnt)+1:(i+1)*(out.shape[1]/cnt)+1:1]
	if cntr == 0:
		result = disp
		cntr += 1
	else:
		result = np.hstack((result, disp))

def measure_l2r(i,j): 
  return np.amin([np.power((result[1::1,i:i+1:1]-result[:result.shape[0]-1:1,j:j+1:1]),2).sum(),
  				  np.power((result[::1,i:i+1:1]-result[::1,j:j+1:1]),2).sum(),
  				  np.power((result[:result.shape[0]-1:1,i:i+1:1]-result[1::1,j:j+1:1]),2).sum()])

for i in xrange(0,result.shape[1]):
	if(i == 0):
		a = np.array([measure_l2r(i,i+1)])
	elif(i < result.shape[1]):
		a = np.append(a, measure_l2r(i, i+1))
	else:
		a = np.append(a, 0)

xx = np.diff(np.asarray(a, dtype='int32'))
xx[xx<0]=0
scale = np.max(xx)/10
mx = 0
ratio = 0
for i in xrange(1,9):
	temp = np.copy(xx)
	temp[temp<(scale*i)]=0
	temp = np.diff(np.nonzero(temp)[0])
	val = mostCommon(temp) 
	if(val[1] > mx):
		mx = val[1]
		interval = val[0]
	else:
		break

print 'identified interval: ',interval
print 'no. of partitions: ',result.shape[1]/interval

x = np.arange(0, xx.size, 1)
y = xx
plt.figure(2)
plt.subplot(211)
plt.title('sample')
plt.imshow(result,'gray')
plt.subplot(212)
plt.title('mod shred boundaries')
plt.plot(x, y)
plt.show()

cnt = result.shape[1]/interval

#unshredder

d = {}
mx = 0
for i in xrange(0,cnt):
	mn = float('inf')
	for j in xrange(0,cnt):
		if j == i:
			continue
		else:
			a = measure_l2r((i+1)*result.shape[1]/cnt-1, j*result.shape[1]/cnt)
			if a < mn:
				mn = a
				slot = j
	if mn > mx:
		mx = mn
		last = i
	d[i] = slot

index = 0
cntr = 0

for i in xrange(0, cnt):
	temp = index
	disp = result[::1,index*(result.shape[1]/cnt):(index+1)*(result.shape[1]/cnt):1]
	if cntr == 0:
		result1 = disp
		cntr += 1
	else:
		result1 = np.hstack((result1, disp))
	index = d[index]
	d[temp] = -1
	if index == -1:
		break

plt.imshow(result1,'gray')
plt.show()