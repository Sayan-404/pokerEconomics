library(readr)
library(dplyr)
library(magrittr)
library(ggplot2)
library(tidyr)

data_path <- commandArgs()[6]
game_dirs <- list.dirs(data_path, full.names = TRUE)

for (i in 2:length(game_dirs)) {
  current_game_dir <- game_dirs[i]
  current_game_file <- paste(current_game_dir, "/games.csv", sep = "")
  if (file.exists(current_game_file)) {
    game <- read.csv(current_game_file)
    columns <- colnames(game)
    total_players <- length(columns) - 4 - 2 + 1
    ti <- c()
    for (i in 2:(length(columns) - 4)) {
      ti <- append(ti, game %>%
                      pull(.data[[columns[i + total_players]]]) %>%
                      last())
    }
    game_long <- game %>%
      pivot_longer(cols = columns[2:(length(columns) - 4)],
                   names_to = "Player",
                   values_to = "Score")
    plot <- ggplot(data = game_long,
                   aes(x = hand_no, y = Score, linetype = Player)) +
      geom_line() +
      labs(
        x = "Hand Number", y = "Score",
        title = paste("Comparison:", paste(columns[2:(length(columns) - 4)], collapse = " vs ")),
        subtitle = paste("Tendency Index:",
                         paste(ti, collapse = ", "))
      ) +
      theme(legend.position = "bottom")
    output_file <- file.path(current_game_dir, "plot.png")
    ggsave(output_file, plot = plot, width = 10, height = 6)
  } else {
    print(paste(current_game_file, "not found"))
  }
}