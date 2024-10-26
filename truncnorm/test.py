import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import numpy as np

# Parameters
shift = 0.1
risk = 0.05
hs = 0.57
sp = 0.73
po = 0.33

# Calculate limits and distribution parameters
ll = po / (1 - po)
ul = sp + hs + risk  # increases range

mean = ll + hs * shift  # shifting the mean ll
sigma = (ul - mean) / 3  # since ul = 3sigma + mean where mean = ll before shifting

t_lower = (ll - mean) / sigma
t_upper = (ul - mean) / sigma

# Define the truncated normal distribution
dist = truncnorm(t_lower, t_upper, loc=mean, scale=sigma)

# Generate data samples
data = dist.rvs(size=1000000)

# Generate x values for plotting the PDF
x = np.linspace(ll, ul, 1000)
pdf = dist.pdf(x)

# Plotting
plt.figure(figsize=(10, 8))

# Plot the truncated normal distribution PDF
plt.subplot(2, 1, 1)
plt.plot(x, pdf, label='Truncated Normal Distribution')
plt.axvline(x=mean, color='red', linestyle='--', label='Mean')
plt.axvline(x=ll, color='blue', linestyle='--', label='Lower Limit')
plt.axvline(x=ul, color='purple', linestyle='--', label='Upper Limit')
plt.title('Truncated Normal Distribution')
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.legend()

# Plot the histogram of the sampled data
plt.subplot(2, 1, 2)
counts, bin_edges, _ = plt.hist(data, bins=100, density=True, alpha=0.6, color='g', label='Sampled Data')
plt.axvline(x=ll, color='blue', linestyle='--', label='Lower Limit')
plt.axvline(x=ul, color='purple', linestyle='--', label='Upper Limit')

# Calculate mode from histogram
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
mode_bin_index = np.argmax(counts)
mode_value = bin_centers[mode_bin_index]

plt.title('Histogram of Sampled Data')
plt.xlabel('x')
plt.ylabel('Density')
plt.axvline(x=mode_value, color='orange', linestyle='--', label='Mode')
plt.legend()

plt.tight_layout()
plt.show()

# Print statistics
print(f"Lower limit (min): {np.min(data):.4f} vs {ll:.4f}")
print(f"Upper limit (max): {np.max(data):.4f} vs {ul:.4f}")
print(f"Mean of sampled data: {np.mean(data)}")
print(f"Median of sampled data: {np.median(data):.4f}")
print(f"Mode of sampled data: {mode_value:.4f}")