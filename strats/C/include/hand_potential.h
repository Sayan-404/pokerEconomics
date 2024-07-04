// hand_potential.h
#ifndef HAND_POTENTIAL_H
#define HAND_POTENTIAL_H

typedef struct {
    float ppot;
    float npot;
} potentials;

potentials potential2(int hole[2],int comm_cards[3]);
#endif // HAND_POTENTIAL_H
