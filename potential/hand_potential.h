// example.h

#ifndef HAND_POTENTIAL_H
#define HAND_POTENTIAL_H

#ifdef __cplusplus
extern "C"
{
#endif

    typedef struct
    {
        float ppot;
        float npot;
    } potentials;

    potentials potential2(char hole[2][3], char comm_cards[5][3])
    {
        potentials tpot = {250.3, 350.3};
        return tpot;
    }
#ifdef __cplusplus
}
#endif

#endif // EXAMPLE_H
