#include <phevaluator/phevaluator.h>

#include <cassert>
#include <iostream>

int evaluate_cards(const std::vector<std::string>& cards) {
    phevaluator::Rank rank1 =
      phevaluator::EvaluateCards(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5],cards[6]);
    return rank1.value();
}

int main() {
  std::vector<std::string> cards = {"9c", "4c", "4s", "9d", "4h", "Qc", "6c"};
  int rank = evaluate_cards(cards);
  std::cout << "Rank: " << rank << std::endl;
}

