import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splev, splrep

def find_nearest(array, value):
# Function finding nearest point in given array
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def spline_smoothing(x_base,y_base,x_smooth,k=4,s=0):
    #Find the B-spline representation of a 1-D curve.
    spl = splrep(x_base, y_base,k=k, s=s)
    y_spl = splev(x_smooth, spl)
    result = np.c_[x_smooth,y_spl]

    return result

# Profile Name - option to omit consol input

#profile_name="NACA0006" # left for tests
print('Input file should be in *.csv format.')
profile_name = input('Give name of input file (without extension): ')

#points_num = 100 # left for tests
points_num = int(input('Set number of points (number must be even): '))

#nose_condense = 2 # left for tests
nose_condense = int(input('Set factor of points condense on nose (number >1): '))

# Import csv file with original profile
profile = np.genfromtxt(f'{profile_name}.csv',dtype='float', delimiter=';')

# Divide profile to upper and lower

divide_point = find_nearest(profile[::,0],0)
upper_profile = profile[:divide_point+1,::]
lower_profile = profile[divide_point:,::]

#Nose profile
#Border points on nose

border = 0.05 # distnce defining nose
upper_div_point = find_nearest(upper_profile[::,0], border)
lower_div_point = find_nearest(lower_profile[::,0], border)

#Nose profile should be rotated between x and y axis to aquire function
nose_profile = profile[upper_div_point: (lower_div_point-len(lower_profile)+1):,::]
nose_profile = nose_profile[::-1,::]

dense_line = np.sort(np.concatenate((np.linspace(nose_profile[0,1],nose_profile[-1,1], num=(len(nose_profile)*nose_condense)), np.array([0.0]))))

smooth_nose = spline_smoothing(nose_profile[::,1],nose_profile[::,0],dense_line,k=2)
smooth_nose = smooth_nose[::,::-1]

#Profile spline divided to upper and lower surface
upper_profile = upper_profile[:upper_div_point+1]
upper_profile = upper_profile [::-1,::]
lower_profile = lower_profile[lower_div_point:]

num = int((points_num-(len(nose_profile)*nose_condense+1))/2)

xd_upper = np.linspace(upper_profile[0,0],upper_profile[-1,0],num=num) #dense line for upper profile
xd_lower = np.linspace(lower_profile[0,0],lower_profile[-1,0],num=num) #dense line for lower profile

spline_upper = spline_smoothing(upper_profile[::,0],upper_profile[::,1],xd_upper,k=4,s=0.0)
spline_lower = spline_smoothing(lower_profile[::,0],lower_profile[::,1],xd_upper,k=4,s=0.0)

#Concatenate nose with rest of the profile in two groups: upper surface and lower surface

nose_division = find_nearest(smooth_nose[::,0], 0)

spline_upper = np.concatenate((smooth_nose[nose_division::,::] , spline_upper[1:,::]),axis=0)
spline_lower = np.concatenate((smooth_nose[nose_division+1::-1,::] , spline_lower[1:,::]),axis=0)


# Plot result and save figure
fig, ax= plt.subplots(1, 2, figsize=(12, 3),  gridspec_kw={'width_ratios': [4,1]})
fig.tight_layout()

#Create subplot 1 with full profile
ax[0] = plt.subplot(1,2,1)

# Set title for subplot 1
ax[0].set_title(f'{profile_name}')

# Plot smoothed curves
l1 = ax[0].plot(spline_upper[::,0], spline_upper[::,1], 'k.-', linewidth = 1, label= 'Upper profile' )
l2 = ax[0].plot(spline_lower[::,0], spline_lower[::,1], 'g.-', linewidth = 1, label= 'Lower profile' )

# Add legend in subplot 2
handles, labels = ax[0].get_legend_handles_labels()
ax[0].legend(handles[::], labels[::])
ax[0].legend(loc=4, prop={'size': 6})


#Create subplot 2 with nose view

# Plot original curves
# Set upper and lower sparde curves for nose profile
sparse_upper = profile[profile[::,1]>=0]
sparse_upper = sparse_upper[sparse_upper[::,0]<=border]
sparse_upper = sparse_upper[::-1,::]
sparse_lower = profile[profile[::,1]<=0]
sparse_lower = sparse_lower[sparse_lower[::,0]<=border]

ax[1] = plt.subplot(1, 2, 2)
l01 = ax[1].plot(sparse_upper[::,0], sparse_upper[::,1], 'bv--', linewidth = 1, label= 'Original upper profile')
l02 = ax[1].plot(sparse_lower[::,0], sparse_lower[::,1], 'yv--', linewidth = 1, label= 'Original lower profile')

# Plot smoothed curves

# Prepare slice with nose smoothed nose profile 
nose_upper = spline_upper[spline_upper[::,0] <= border] 
nose_lower = spline_lower[spline_lower[::,0] <= border]

l11 = ax[1].plot(nose_upper[::,0], nose_upper[::,1], 'k.-', linewidth = 0.7, label= 'Smoothed upper profile')
l12 = ax[1].plot(nose_lower[::,0], nose_lower[::,1], 'g.-', linewidth = 0.7, label= 'Smoothed lower profile')

#Set title for subplot 2
ax[1].set_title(f'{profile_name} nose view')

# Add legend in subplot 2
handles, labels = ax[1].get_legend_handles_labels()
ax[1].legend(handles[::], labels[::])
ax[1].legend(loc=7, prop={'size': 6})

# Save figure
fig.savefig(f'{profile_name}_smoothed.jpg', dpi = 720)
plt.show()

#Write reusults to text file
result = np.concatenate((spline_upper[::-1,::] , spline_lower[1:,::]),axis=0)
np.savetxt(f'{profile_name}_smoothed.csv', result, delimiter=";",fmt='%1.6e')


