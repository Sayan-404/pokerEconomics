library(readr)
library(dplyr)
library(magrittr)
library(ggplot2)
library(tidyr)

data_path <- commandArgs()[6]
game_dirs <- list.dirs(data_path, full.names = TRUE)

custom_colors <- c("#04ff00", "#000099")

for (i in 2:length(game_dirs)) {
  current_game_dir <- game_dirs[i]
  current_game_file <- paste(current_game_dir, "/games.csv", sep = "")
  if (file.exists(current_game_file)) {
    game <- read.csv(current_game_file,
                     fileEncoding = "UTF-8", check.names = FALSE)
    game <- game[-1, ]
    columns <- colnames(game)
    total_players <- length(columns) - 4 - 2 + 1

    winner_column <- game$winner
    entity_counts <- game %>%
      count(.data[["winner"]])

    entity_counts <- entity_counts %>%
      mutate(win_ratio = n / sum(.data[["n"]]),
             winner = paste(winner, "(", winner, ")", sep = ""))

    metrics <- data.frame(
      player = character(),
      ti = numeric(),
      win_ratio = numeric(),
      stringsAsFactors = FALSE
    )
    for (i in 2:(length(columns) - 4)) {
      player <- columns[i]
      ti <- game %>%
        pull(.data[[columns[i + total_players]]]) %>%
        last()
      win_ratio <- entity_counts %>%
        filter(.data[["winner"]] == player) %>%
        pull(.data[["win_ratio"]])
      metrics <- rbind(metrics, data.frame(player = player,
                                           ti = ti, win_ratio = win_ratio))
    }
    print(metrics)
    game_long <- game %>%
      pivot_longer(cols = columns[2:(length(columns) - 4)],
                   names_to = "Player",
                   values_to = "Score")

    player_colors <- setNames(custom_colors[1:length(unique(game_long$Player))],
                              unique(game_long$Player))

    plot <- ggplot(data = game_long,
                   aes(x = hand_no, y = Score, colour = Player)) +
      geom_line() +
      scale_color_manual(values = player_colors) +
      labs(
        x = "Hand Number", y = "Score",
        title = paste("Comparison:",
                      paste(metrics$player,
                            collapse = " vs ")),
        subtitle = paste(paste("Tendency Index:",
                               paste(metrics$ti, collapse = ", ")),
                         paste("Win Ratio:",
                               paste(metrics$win_ratio, collapse = ", ")),
                         sep = "\n")
      ) +
      theme(legend.position = "bottom")
    output_file <- file.path(current_game_dir, "plot.png")
    ggsave(output_file, plot = plot, width = 10, height = 6)
  } else {
    print(paste(current_game_file, "not found"))
  }
}