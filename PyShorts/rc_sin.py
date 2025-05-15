import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Define the frequency and amplitude of the sinusoidal input
f = 100  # 100 Hz
A = 1  # 1 V
# Circuit parameters
R = 1e3  # 1 kOhm
C = 1e-6  # 1 uF

# Define the transfer function of the RC circuit
tf = signal.TransferFunction([1], [R*C, 1])
# Generate the input waveform
t = np.linspace(0, 1/f, 1000)
u = A * np.sin(2 * np.pi * f * t)

# Simulate the circuit's response to the input waveform
t, y, _ = signal.lsim(tf, u, t)

# Plot the input and output waveforms
plt.plot(t, u, label='Input')
plt.plot(t, y, label='Output')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Response of RC Circuit to Sinusoidal Input')
plt.legend()
plt.show()
