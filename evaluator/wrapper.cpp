#include "wrapper.hpp"

int evaluate5_cards(const char* card1, const char* card2, const char* card3, const char* card4, const char* card5) {
    return phevaluator::EvaluateCards(card1, card2, card3, card4, card5).value();
}

int evaluate6_cards(const char* card1, const char* card2, const char* card3, const char* card4, const char* card5, const char* card6) {
    return phevaluator::EvaluateCards(card1, card2, card3, card4, card5, card6).value();
}

int evaluate7_cards(const char* card1, const char* card2, const char* card3, const char* card4, const char* card5, const char* card6, const char* card7) {
    return phevaluator::EvaluateCards(card1, card2, card3, card4, card5, card6, card7).value();
}
