library(readr)
library(dplyr)
library(magrittr)
library(ggplot2)
library(tidyr)

data_path <- commandArgs(trailingOnly = TRUE)[1]
game_dirs <- list.dirs(data_path, full.names = TRUE)

custom_colors <- c("#04ff00", "#000099")

for (dir_index in seq(2, length(game_dirs))) {
  current_game_dir <- game_dirs[dir_index]
  current_game_file <- paste(current_game_dir, "/games.csv", sep = "")
  if (file.exists(current_game_file)) {
    game <- read.csv(current_game_file,
                     fileEncoding = "UTF-8", check.names = FALSE)
    game <- game[-1, ]
    columns <- colnames(game)
    total_players <- (length(columns) - 3) / 2 # 2 columns for each player signifying the bankroll and the tendency index

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
    for (i in seq(2, 2 + total_players - 1)) {
      player <- columns[i]
      ti <- game %>%
        pull(.data[[columns[i + total_players]]]) %>%
        last()
      player_name <- sub("\\(.*", "", player)
      win_ratio <- entity_counts %>%
        filter(grepl(player_name, .data[["winner"]])) %>%
        distinct(winner, .keep_all = TRUE) %>%
        pull(.data[["win_ratio"]])

      metrics <- rbind(metrics, data.frame(player = player,
                                           ti = ti, win_ratio = win_ratio))
    }
    print(metrics)

    ending_round <- game %>%
      count(.data[["ending_round"]])
    print(ending_round)

    game_long <- game %>%
      pivot_longer(cols = columns[2:(2 + total_players - 1)],
             names_to = "Player",
             values_to = "Score") %>%
      mutate(Score = log10(Score)) # logarithmic scaling of the bankrolls

    player_colors <- setNames(custom_colors[seq_len(length(unique(game_long$Player)))],
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
    print(plot)
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
    print(plot)
    dev.off()  # Close the svg device
    message(paste("Plot saved to:", output_file))

    size <- 1000
    convergence_metrics <- data.frame(
      index = numeric(),
      player = character(),
      win_ratio_cumm = numeric(),
      win_ratio = numeric(),
      profitability_per_hand_cumm = numeric(),
      profitability_per_hand = numeric(),
      stringsAsFactors = FALSE
    )
    for (j in seq(size, nrow(game), size)) {
      sliced_game_cumm <- game %>%
        slice(1: min(j + size, nrow(game)))
      sliced_game <- game %>%
        slice(j: min(j + size - 1, nrow(game)))
      entity_counts_cumm <- sliced_game_cumm %>%
        count(.data[["winner"]])
      entity_counts_cumm <- entity_counts_cumm %>%
        mutate(win_ratio = n / sum(.data[["n"]]),
               winner = winner)
      entity_counts <- sliced_game %>%
        count(.data[["winner"]])
      entity_counts <- entity_counts %>%
        mutate(win_ratio = n / sum(.data[["n"]]),
               winner = winner)
      for (i in seq(2, 2 + total_players - 1)) {
        player <- columns[i]
        player_name <- sub("\\(.*", "", player)
        profitability_per_hand_cumm <- (sliced_game_cumm %>%
          pull(.data[[player]]) %>%
          last() - sliced_game_cumm %>%
          pull(.data[[player]]) %>%
          first()) / nrow(sliced_game_cumm)
        profitability_per_hand <- (sliced_game %>%
          pull(.data[[player]]) %>%
          last() - sliced_game %>%
          pull(.data[[player]]) %>%
          first()) / nrow(sliced_game)
        if (nrow(sliced_game) < size) {
          next
        }
        convergence_metrics <- rbind(convergence_metrics, data.frame(
          index = j,
          player = player,
          win_ratio_cumm = entity_counts_cumm %>%
            filter(grepl(player_name, .data[["winner"]])) %>%
            pull(.data[["win_ratio"]]),
          profitability_per_hand_cumm = profitability_per_hand_cumm,
          win_ratio = entity_counts %>%
            filter(grepl(player_name, .data[["winner"]])) %>%
            pull(.data[["win_ratio"]]),
          profitability_per_hand = profitability_per_hand
        ))
      }
    }
    plot1 <- ggplot(data = convergence_metrics,
                   aes(x = index, y = profitability_per_hand_cumm, colour = player)) +
      geom_line() +
      scale_color_manual(values = player_colors) +
      labs(
        x = "Index", y = "Profitability per Hand",
        title = paste("Profitability per Hand Convergence"),
        subtitle = paste(metrics$player,
                          collapse = " vs ")
      ) +
      theme(legend.position = "bottom")
    plot2 <- ggplot(data = convergence_metrics,
                   aes(x = index, y = win_ratio_cumm, colour = player)) +
      geom_line() +
      scale_color_manual(values = player_colors) +
      labs(
        x = "Index", y = "Win Ratio",
        title = paste("Win Ratio Convergence"),
        subtitle = paste(metrics$player,
                         collapse = " vs ")
      ) +
      theme(legend.position = "bottom")
    output_file <- file.path(current_game_dir, "profitability_per_hand.svg")
    svg(output_file, width = 10, height = 6)
    print(plot1)
    dev.off()  # Close the svg device
    message(paste("Plot saved to:", output_file))
    output_file <- file.path(current_game_dir, "win_ratio.svg")
    svg(output_file, width = 10, height = 6)
    print(plot2)
    dev.off()  # Close the svg device
    message(paste("Plot saved to:", output_file))
    confidence_intervals <- data.frame(
      player = character(),
      p_value = numeric(),
      win_rate_lower = numeric(),
      win_rate_upper = numeric(),
      profitability_lower = numeric(),
      profitability_upper = numeric(),
      stringsAsFactors = FALSE
    )
  } else {
    print(paste(current_game_file, "not found"))
  }
}