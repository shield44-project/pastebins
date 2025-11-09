import matplotlib.pyplot as plt
import numpy as np

# Create data points from 0 to 2π (about 6.28)
x = np.linspace(0, 2 * np.pi, 100)  # 100 points
y = np.sin(x)  # Sine of each x

# Plot
plt.plot(x, y, label="sin(x)", color="blue", linewidth=2)

# Labels and title
plt.xlabel("x (radians)")
plt.ylabel("sin(x)")
plt.title("Sine Wave")

# Add grid and legend
plt.grid(True)
plt.legend()

# Show
plt.show()
