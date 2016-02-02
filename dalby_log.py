import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

def smooth_filter(raw,kernel):
	return signal.medfilt(raw, kernel_size=kernel)

# In files 
in_files = ['TRGS8068-Dalbyover5.LAS', 'TRGS8068-Dalbyover4.LAS']

in_data = np.empty([0, 8])

for file in in_files:
	read_data = np.genfromtxt(file, skiprows=39, delimiter=(10,)+(9,)+(14,)*6)
	print read_data.shape
	in_data = np.concatenate((in_data,read_data),axis=0)

# C convert feet to meters and us to s 0.3048
C = 10**6 

# Calculate velocity from spacing (20cm) and arrival time difference
v1 = C*0.20/(in_data[:,3]-in_data[:,2]) 	#R2-R1
v2 = C*0.20/(in_data[:,4]-in_data[:,3])		#R3-R2
#v3 = C*0.40/(in_data[:,4]-in_data[:,2])		#R3-R1

# Save file with velocity data
np.savetxt('data.txt',in_data,fmt='%5.2f') 

# Apply smoothing filter kernel is median window size, must be odd
kernel=51

v1s = smooth_filter(v1,kernel)
v2s = smooth_filter(v2,kernel)
#v3s = smooth_filter(v3,kernel)

# Plot sonic
fig = plt.figure(figsize=(10,12))
fig.subplots_adjust(wspace=0.05)


ax1 = plt.subplot(121)
ax1.set_ylim(ax1.get_ylim()[::-1]) 
plt.title('Sonic velocity', fontsize = 12)
plt.ylabel( 'Well depth (m)', fontsize = 12)

plt.plot(v1,in_data[:,0]+0.1, lw=1, color='black', alpha=0.2)
plt.plot(v2,in_data[:,0]-0.1, lw=1, color='green', alpha=0.2)
#plt.plot(v3,d, lw=1, color='blue', alpha=0.2)

plt.plot(v1s,in_data[:,0]+0.1, lw=2, color='black', label='R2-R1',alpha=0.7)
plt.plot(v2s,in_data[:,0]+0.1, lw=2, color='green', label='R3-R2', alpha=0.7)
#plt.plot(v3s,d+0.1, lw=2, color='blue', label='R3-R1', alpha=0.9)

plt.setp(ax1.get_xticklabels(), fontsize=6)
plt.xlim(0, 15000)
plt.grid()
plt.legend()

# Plot gamma
ax2 = plt.subplot(122, sharey=ax1)
plt.title('Gamma', fontsize = 12 )


plt.plot(in_data[:,7],in_data[:,0]+0.1, lw=2, color='black', label='API', alpha=0.7)
plt.xlim(0, 30)
plt.setp(ax2.get_yticklabels(), visible=False)
plt.grid()
plt.legend()
#plt.setp([a.get_yticklabels() for a in fig.axes[:-1]], visible=False)



#fig = plt.figure(figsize=(10,12))
# fig,AX = plt.subplots(2, 2, sharey=True)
# AX[0,0].invert_yaxis()
# 
# plt.gca().invert_yaxis()
# plt.ylabel( 'Well depth (m)', fontsize = 12)
# 
# fig.add_subplot(121)

# 

# 
# plt.title('Sonic velocity', fontsize = 12 )
# plt.legend()
# plt.xlim(0,15000)
# 
# 
# fig.add_subplot(122)
# plt.plot(in_data[:,7],in_data[:,0]+0.1, lw=2, color='black', label='Gamma', alpha=0.7)
# 
# plt.title('Gamma', fontsize = 12 )
# plt.xlim(0,60)
# 
# fig.subplots_adjust(hspace=0)
# plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

# 
# plt.title('Sonic velocity', fontsize = 12 )
# plt.ylabel( 'Well depth (m)', fontsize = 12)
# plt.xlabel('Velocity (m/s)', fontsize = 12)
# plt.xlim(0,15000)
# plt.gca().invert_yaxis()







plt.show()
