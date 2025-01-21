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
    output_csv_file <- file.path(current_game_dir, "metrics.csv")
    write.csv(metrics, file = output_csv_file, row.names = FALSE)
    message(paste("Metrics saved to:", output_csv_file))

    ending_round <- game %>%
      count(.data[["ending_round"]])
    output_csv_file <- file.path(current_game_dir, "ending_round.csv")
    write.csv(ending_round, file = output_csv_file, row.names = FALSE)
    message(paste("Ending round data saved to:", output_csv_file))

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
    message(paste("Bankroll plot saved to:", output_file))

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
    message(paste("Ending round histogram saved to:", output_file))

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
    sliced_game <- game %>%
      slice(seq_len(min(size, nrow(game))))
    sliced_game <- game %>%
      slice(seq_len(min(size, nrow(game))))
    for (j in seq(size, nrow(game) - size, size)) {
      sliced_game_cumm <- game %>%
        slice(seq_len(min(j + size, nrow(game))))
      sliced_game <- game %>%
        slice((j + 1): min(j + size, nrow(game)))
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
    message(paste("Win Ratio convergence plot saved to:", output_file))
    output_file <- file.path(current_game_dir, "win_ratio.svg")
    svg(output_file, width = 10, height = 6)
    print(plot2)
    dev.off()  # Close the svg device
    message(paste("Profitability convergence plot saved to:", output_file))

    # confidence_intervals <- data.frame(
    #   player = character(),
    #   alpha = numeric(),
    #   win_ratio_lower = numeric(),
    #   win_ratio_upper = numeric(),
    #   profitability_lower = numeric(),
    #   profitability_upper = numeric(),
    #   win_ratio_CI_diff = numeric(),
    #   profitability_CI_diff = numeric(),
    #   stringsAsFactors = FALSE
    # )
    x_1 <- 0.1 # proportion of first part
    x_2 <- 0.5 # proportion of last part
    analysis_metrics <- data.frame(
      player = character(),
      variable = character(),
      p = numeric(),
      t_statistic = numeric(),
      stringsAsFactors = FALSE
    )
    for (i in seq(2, 2 + total_players - 1)) {
      player <- columns[i]
      player_data <- convergence_metrics %>%
        filter(player == !!player)
      data_first_part <- player_data[seq_len(as.integer(x_1 * nrow(player_data))), ]
      data_last_part <- player_data[as.integer((1 - x_2) * nrow(player_data) + 1):nrow(player_data), ]

      n_1 <- nrow(data_first_part)
      n_2 <- nrow(data_last_part)

      win_ratio_mu_1 <- mean(data_first_part$win_ratio)
      win_ratio_mu_2 <- mean(data_last_part$win_ratio)
      win_ratio_sd_1 <- sd(data_first_part$win_ratio)
      win_ratio_sd_2 <- sd(data_last_part$win_ratio)
      win_ratio_s_dash_square <- (((n_1 - 1)*(win_ratio_sd_1^2)) + ((n_2 - 1)*(win_ratio_sd_2^2))) / (n_1 + n_2 - 2)
      win_ratio_s_dash <- sqrt(win_ratio_s_dash_square)
      win_ratio_t <- (win_ratio_mu_1 - win_ratio_mu_2) / (win_ratio_s_dash * sqrt((1 / n_1) + (1 / n_2)))
      win_ratio_df <- n_1 + n_2 - 2
      win_ratio_p <- 2 * (1 - pt(abs(win_ratio_t), win_ratio_df))

      profitability_mu_1 <- mean(data_first_part$profitability_per_hand)
      profitability_mu_2 <- mean(data_last_part$profitability_per_hand)
      profitability_sd_1 <- sd(data_first_part$profitability_per_hand)
      profitability_sd_2 <- sd(data_last_part$profitability_per_hand)
      profitability_s_dash_square <- (((n_1 - 1)*(profitability_sd_1^2)) + ((n_2 - 1)*(profitability_sd_2^2))) / (n_1 + n_2 - 2)
      profitability_s_dash <- sqrt(profitability_s_dash_square)
      profitability_t <- (profitability_mu_1 - profitability_mu_2) / (profitability_s_dash * sqrt((1 / n_1) + (1 / n_2)))
      profitability_df <- n_1 + n_2 - 2
      profitability_p <- 2 * (1 - pt(abs(profitability_t), profitability_df))

      analysis_metrics <- rbind(analysis_metrics, data.frame(
        player = c(player, player),
        variable = c("win_ratio", "profitability_per_hand"),
        p = c(win_ratio_p, profitability_p),
        t_statistic = c(win_ratio_t, profitability_t)
      ))
      # alpha_z_score_matrix <- matrix(
      #   c(0.10, 1.65, 0.05, 1.96, 0.01, 2.58),
      #   nrow = 3,
      #   byrow = TRUE
      # )
      # mu_win_ratio <- convergence_metrics %>%
      #   filter(player == !!player) %>%
      #   pull(.data[["win_ratio"]]) %>%
      #   mean()
      # sigma_win_ratio <- convergence_metrics %>%
      #   filter(player == !!player) %>%
      #   pull(.data[["win_ratio"]]) %>%
      #   sd()
      # mu_profitability <- convergence_metrics %>%
      #   filter(player == !!player) %>%
      #   pull(.data[["profitability_per_hand"]]) %>%
      #   mean()
      # sigma_profitability <- convergence_metrics %>%
      #   filter(player == !!player) %>%
      #   pull(.data[["profitability_per_hand"]]) %>%
      #   sd()
      # n <- convergence_metrics %>%
      #   filter(player == !!player) %>%
      #   nrow()
      # sem_win_ratio <- sigma_win_ratio / sqrt(n)
      # sem_profitability <- sigma_profitability / sqrt(n)
      # for (i in seq_len(nrow(alpha_z_score_matrix))) {
      #   alpha <- alpha_z_score_matrix[i, 1]
      #   z_score <- alpha_z_score_matrix[i, 2]
      #   win_ratio_lower <- mu_win_ratio - z_score * sem_win_ratio
      #   win_ratio_upper <- mu_win_ratio + z_score * sem_win_ratio
      #   profitability_lower <- mu_profitability - z_score * sem_profitability
      #   profitability_upper <- mu_profitability + z_score * sem_profitability
      #   confidence_intervals <- rbind(confidence_intervals, data.frame(
      #     player = player,
      #     alpha = alpha,
      #     win_ratio_lower = win_ratio_lower,
      #     win_ratio_upper = win_ratio_upper,
      #     profitability_lower = profitability_lower,
      #     profitability_upper = profitability_upper,
      #     win_ratio_CI_diff = win_ratio_upper - win_ratio_lower,
      #     profitability_CI_diff = profitability_upper - profitability_lower
      #   ))
      # }
    }
    output_csv_file <- file.path(current_game_dir, "analysis_metrics.csv")
    write.csv(analysis_metrics, file = output_csv_file, row.names = FALSE)
    message(paste("Analysis metrics saved to:", output_csv_file))
    # output_csv_file <- file.path(current_game_dir, "confidence_intervals.csv")
    # write.csv(confidence_intervals, file = output_csv_file, row.names = FALSE)
    # message(paste("Confidence intervals saved to:", output_csv_file))
    # output_csv_file <- file.path(current_game_dir, "convergence_metrics.csv")
    # write.csv(convergence_metrics, file = output_csv_file, row.names = FALSE)
    # message(paste("Convergence metrics saved to:", output_csv_file))
  } else {
    print(paste(current_game_file, "not found"))
  }
}