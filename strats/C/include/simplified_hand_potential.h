#ifndef SIMPLIFIED_HAND_POTENTIAL_H
#define SIMPLIFIED_HAND_POTENTIAL_H

typedef struct {
    float ppot;
    float npot;
} simplepotentials;

void create_deck(int *deck);
void remove_card(int *deck,int card,int *deck_size);
simplepotentials simple_potential2(int hole[2],int comm_cards[3]);

#endif 