import numpy as np
import matplotlib.pyplot as plt

# Define the lists
a = [1, 2, 3]
b = [4, 5, 6]

# Create a scatter plot with connecting lines
# plt.plot([0, 1], [a[0], b[0]], 'o-', label='Value 1')
# plt.plot([0, 1], [a[1], b[1]], 'o-', label='Value 2')
# plt.plot([0, 1], [a[2], b[2]], 'o-', label='Value 3')

for i in range(len(a)):
    plt.plot([0,1], [a[i], b[i]], 'o-', label=('pp_idx_'+str(i)))
    
# Add the mean values to the plot as bars
plt.bar([0, 1], [np.mean(a), np.mean(b)], color='gray', alpha=0.5, edgecolor='black', linewidth=1.5, capsize=10)

# Add labels and title
plt.xlabel('Conditions')
plt.ylabel('Measure')
plt.title('Individual values and means in two conditions')

# Add legend and show the plot
plt.legend()
plt.show()
