# File: trunc_norm_plot.R

library(truncnorm)
library(ggplot2)

# Read command-line arguments
args <- commandArgs(trailingOnly = TRUE)
mean <- as.numeric(args[1])
lower <- as.numeric(args[2])
upper <- as.numeric(args[3])
po <- as.numeric(args[4])

# Calculate standard deviation based on truncation bounds
sd <- (upper - lower) / 3

# Generate data for the truncated normal distribution
x_vals <- seq(lower - 0.2, upper + 0.2, length.out = 1000)
y_vals <- dtruncnorm(x_vals, a = lower, b = upper, mean = mean, sd = sd)

# Create a data frame for plotting
data <- data.frame(x = x_vals, y = y_vals)

# Ensure all vline positions are within range
vline_data <- data.frame(
  position = c(mean, lower, upper, po),
  label = c(
    paste("Mean (", mean, ")"),
    paste("Lower Bound (", lower, ")"),
    paste("Upper Bound (", upper, ")"),
    paste("Pot Odds (", po, ")")
  ),
  color = c("red", "green", "purple", "orange")
)

# Filter vline_data to keep only lines within x range
vline_data <- vline_data[vline_data$position >= min(x_vals) & vline_data$position <= max(x_vals), ]

# Create the plot
plot <- ggplot(data, aes(x = x, y = y)) +
  geom_line(color = "blue", linewidth = 1) +
  # Add dashed vertical lines with a proper legend
  geom_vline(
    data = vline_data,
    aes(xintercept = position, color = label),
    linetype = "dashed",
    linewidth = 0.8
  ) +
  # Customize the color scale for the legend
  scale_color_manual(
    name = "Parameters",
    values = setNames(vline_data$color, vline_data$label)
  ) +
  labs(
    title = "Truncated Normal Distribution",
    x = "Value",
    y = "Density"
  ) +
  theme(
    legend.position = "bottom",
    legend.title = element_text(face = "bold"),
    legend.text = element_text(size = 10)
  )

# Save the plot to a file
output_file <- "truncated_normal_distribution_with_lines.svg"
svg(output_file, width = 10, height = 6)
print(plot)
dev.off()  # Close the svg device
message(paste("Bankroll plot saved to:", output_file))