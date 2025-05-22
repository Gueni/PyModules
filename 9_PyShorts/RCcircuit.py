
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Circuit parameters
R = 1e3  # 1 kOhm
C = 1e-6  # 1 uF

# Define the transfer function of the RC circuit
tf = signal.TransferFunction([1], [R*C, 1])

# Generate a step input and simulate the circuit's response
t, y = signal.step(tf)

# Plot the step response
plt.plot(t, y)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Step Response of RC Circuit')
plt.show()

