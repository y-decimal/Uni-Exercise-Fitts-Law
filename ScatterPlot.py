import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dataMouse = pd.read_csv('resultsMouse.csv')
dataVR = pd.read_csv('resultsVR.csv')

def best_fit(x, y):
    """Returns the slope and intercept of the best fit line for the given x and y data."""
    xbar = sum(x) / len(x)
    ybar = sum(y) / len(y)
    n = len(x)
    
    numerator = sum((x[i] - xbar) * (y[i] - ybar) for i in range(n))
    denominator = sum((x[i] - xbar) ** 2 for i in range(n))
    
    b = numerator / denominator
    a = ybar - b * xbar
    
    print(f"Best fit line: y = {a} + {b}x")
    return a, b

aM, bM = best_fit(dataMouse['Index of Difficulty'], dataMouse['Time Taken'])
mT_Mouse = [aM + bM* xi for xi in dataMouse['Index of Difficulty']]

aV, bV = best_fit(dataVR['Index of Difficulty'], dataVR['Time Taken'])
mT_VR = [aV + bV* xi for xi in dataVR['Index of Difficulty']]


plt.scatter(dataMouse['Index of Difficulty'], dataMouse['Time Taken'], label='Mouse', color='blue', alpha=0.5)
plt.scatter(dataVR['Index of Difficulty'], dataVR['Time Taken'], label='VR', color='red', alpha=0.5)

plt.plot(dataMouse['Index of Difficulty'], mT_Mouse, color='blue', label='Mouse Fit', linestyle='--')
plt.text(4.5,0.3, f"y = {aM:.2f} + {bM:.2f}x", color='blue', fontsize=10, ha='left', va='bottom')

plt.plot(dataVR['Index of Difficulty'], mT_VR, color='red', label='VR Fit', linestyle='--')
plt.text(4.5,0.7, f"y = {aV:.2f} + {bV:.2f}x", color='red', fontsize=10, ha='left', va='bottom')

plt.title('Fitts Law - Mouse vs VR (emultating Touchscreen)')
plt.ylabel('Time Taken (s)')
plt.xlabel('Index of Difficulty')
plt.legend()
plt.savefig('Fitts_Law_Mouse_vs_VR.png')
plt.show()