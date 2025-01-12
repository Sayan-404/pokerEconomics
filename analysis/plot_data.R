library(readr)
library(dplyr)
library(magrittr)
library(ggplot2)
library(tidyr)

data_path <- commandArgs(trailingOnly = TRUE)[1]
game_dirs <- list.dirs(data_path, full.names = TRUE)

custom_colors <- c("#04ff00", "#000099")

for (dir_index in 2:length(game_dirs)) {
  current_game_dir <- game_dirs[dir_index]
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
             winner = winner)

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
      player_name <- sub("\\(.*", "", player)
      win_ratio <- entity_counts %>%
        filter(grepl(player_name, .data[["winner"]])) %>%
        pull(.data[["win_ratio"]])

      metrics <- rbind(metrics, data.frame(player = player,
                                           ti = ti, win_ratio = win_ratio))
    }
    print(metrics)

    ending_round <- game %>%
      count(.data[["ending_round"]])
    print(ending_round)

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
  output_file <- file.path(current_game_dir, "bankroll_line.svg")
  svg(output_file, width = 10, height = 6)
  print(plot)  # Ensure the plot is rendered
  dev.off()  # Close the svg device
  message(paste("Plot saved to:", output_file))

    plot <- ggplot(data = ending_round,
                   aes(x = ending_round, y = n)) +
      geom_bar(stat = "identity") +
      labs(
        x = "Ending Round", y = "Count",
        title = "Ending Round Distribution"
      )
  output_file <- file.path(current_game_dir, "ending_round_hist.svg")
  svg(output_file, width = 10, height = 6)
  print(plot)  # Ensure the plot is rendered
  dev.off()  # Close the svg device
  message(paste("Plot saved to:", output_file))
  } else {
    print(paste(current_game_file, "not found"))
  }
}