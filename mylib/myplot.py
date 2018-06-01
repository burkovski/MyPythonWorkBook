import matplotlib.pyplot as plt
from lab9 import maximum, minimum


plt.scatter(maximum[1]['x'], maximum[1]['y'])
plt.scatter(minimum[1]['x'], minimum[1]['y'])
plt.scatter(maximum[2]['x'], maximum[2]['z'])
plt.scatter(minimum[2]['x'], minimum[2]['z'])
plt.show()
