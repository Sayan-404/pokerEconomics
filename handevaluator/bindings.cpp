#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <phevaluator/phevaluator.h>

int evaluate_cards(const std::vector<std::string>& cards) {
    phevaluator::Rank rank =
      phevaluator::EvaluateCards(cards[0], cards[1], cards[2], cards[3], cards[4], cards[5], cards[6]);
    return rank.value();
}

PYBIND11_MODULE(phevaluator_bindings, m) {
    m.def("evaluate_cards", &evaluate_cards);
}
