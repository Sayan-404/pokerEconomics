#ifndef SIMPLIFIED_HAND_POTENTIAL_H
#define SIMPLIFIED_HAND_POTENTIAL_H

#ifdef __cplusplus
extern "C"
{
#endif

    typedef struct
    {
        float ppot;
        float npot;
    } potentials;

    void create_deck(int *deck);
    void remove_card(int *deck, int card, int *deck_size);
    int rank7(int hole[2], int comm_cards[3]);
    int rank5(int hole[2], int comm_cards[3]);
    potentials potential2(int hole[2], int comm_cards[3]);

#ifdef __cplusplus
}
#endif

#endif // SIMPLIFIED_HAND_POTENTIAL_H
