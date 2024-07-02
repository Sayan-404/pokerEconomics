#include <assert.h>
#include <phevaluator/phevaluator.h>
#include <phevaluator/rank.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "newlookuptable.h"
#include <time.h>

#define DECK_SIZE 52

#define AHEAD 1
#define TIED 0
#define BEHIND 2

typedef struct {
    float ppot;
    float npot;
} potentials;

void create_deck(int *deck) {

   int ranks[]={0,1,2,3,4,5,6,7,8,9,10,11,12};
   int suits[]={0,1,2,3};

    int index = 0;

    for (int i = 0; i < 13; i++) {
        for (int j = 0; j < 4; j++) {
            deck[index] = ranks[i] * 4 + suits[j];
            index++;
        }
    }
}
void remove_card(int *deck,int card, int* deck_size) {
    int i;
    for (i = 0; i < *deck_size; i++) {
        if(deck[i] == card) {
            deck[i] = deck[*deck_size - 1];
            (*deck_size)--;
            return;
        }
    }
    printf("Card %d not found in the deck.\n", card);
}

int rank7(int hole[2], int comm_cards[3]) {
    int rank = evaluate_7cards(hole[0], hole[1], comm_cards[0], comm_cards[1], comm_cards[2], comm_cards[3], comm_cards[4]);
    return rank;
}
int rank5(int hole[2], int comm_cards[3]) {
    int rank = evaluate_5cards(hole[0], hole[1], comm_cards[0], comm_cards[1], comm_cards[2]);
    return rank;
}

// char* makedeck()
potentials potential2(int hole[2], int comm_cards[5]) {

    float hp[3][3];
    float hp_total[3];

    float ppot2, npot2;
    float ourrank5,ourrank7,opprank;

    //Creating the deck
    int deck[DECK_SIZE];
    int deck_size = DECK_SIZE;
    create_deck(&deck[0]);
    ourrank5 = rank5(hole,comm_cards);
    int i,j;
    int k;
    clock_t t;
    double time_taken;
    // for(i=0;i<deck_size;i++)
    //     printf("%d",deck[i]);
    // printf("\n decksize: %d",deck_size);
    // exit(0);
    //initialising hp to all zeroes
    for(i=0;i<3;i++) {
        hp_total[i] = 0;
    for(j=0;j<3;j++)
        hp[i][j]=0;
    }

    int index=0; // 1 is ahead, 0 is tied, 2 is behind
    // removing hole cards and community cards
    for(k=0;k<2;k++)
        remove_card(&deck[0],hole[k],&deck_size);
    for(k=0;k<3;k++)
        remove_card(&deck[0],comm_cards[k],&deck_size);
        
    // printf("ourrank: %f",ourrank5);
    for(i=0;i<deck_size-1;i++)
        for(j=i+1;j<deck_size;j++)
            {
                int oppcards[2] = {deck[i], deck[j]};
                // printf("oppcards: %d %d",oppcards[0],oppcards[1]);
                // exit(1);
                opprank = rank5(oppcards,comm_cards);
                // printf("%f",opprank);
                // exit(1);
                if(ourrank5 < opprank)
                    index=AHEAD;
                else if(ourrank5 == opprank)
                    index = TIED;
                else
                    index = BEHIND;
                
                int t_deck[DECK_SIZE];
                int t_deck_size = DECK_SIZE;
                create_deck(&t_deck[0]);
                int l;
                for(l=0;l<2;l++) {
                    remove_card(&t_deck[0], hole[l], &t_deck_size);
                    remove_card(&t_deck[0], oppcards[l], &t_deck_size);
                }
                for(l=0;l<3;l++) {
                    remove_card(&t_deck[0], comm_cards[l], &t_deck_size);
                }
                //we draw two cards from the t_deck to make a 5 card board 
                int m;
                for(l=0;l<t_deck_size-1;l++) {
                    for(m=l+1;m<t_deck_size;m++) {
                        int remaining_cards[2] = {t_deck[l],t_deck[m]};
                        
                        hp_total[index] += 1;

                        // char five_card_board[5][CARD_LENGTH];
                        int five_card_board[5];
                        int h;
                        // printf("%s ",remaining_cards[0]);
                        // printf("%s ",remaining_cards[1]);
                        // printf("\n");
                        for(h=0;h<5;h++) {
                            if(h<3)
                                five_card_board[h] = comm_cards[h];
                            else
                                five_card_board[h] = remaining_cards[h-3];
                            }
                        struct DataItem* pItem = pSearch(remaining_cards,2);
                        if(pItem != NULL){
                            // printf("found something");
                            ourrank7 = pItem->data;
                        }
                        else {
                            ourrank7=rank7(hole,five_card_board);
                            pInsert(remaining_cards,2,ourrank7);
                        }
                        
                        int opp4[4]={remaining_cards[0],remaining_cards[1],oppcards[0],oppcards[1]};
                        struct DataItem* oppItem;
                        oppItem = oppSearch(opp4,4);
                        if(oppItem != NULL)
                        {
                            // printf("found something");
                            opprank=oppItem->data;
                        }
                        else {
                            opprank=rank7(oppcards,five_card_board);
                            oppInsert(opp4,4,opprank);
                        }
                        // opprank=rank7(oppcards,five_card_board);
                        // printf("ourrank: %f",ourrank7);
                        // printf("opprank: %f",opprank);
                        // exit(0);
                        if(ourrank7<opprank)
                            hp[index][AHEAD] += 1;
                        else if(ourrank7 == opprank)
                            hp[index][TIED] += 1;
                        else
                            hp[index][BEHIND] += 1;
                    }
                }
            }
    ppot2 = (hp[BEHIND][AHEAD] + hp[BEHIND][TIED]/2 + hp[TIED][AHEAD]/2) / (hp_total[BEHIND] + hp_total[TIED]/2);
    npot2 = (hp[AHEAD][BEHIND] + hp[AHEAD][TIED]/2 + hp[TIED][BEHIND]/2) / (hp_total[AHEAD] + hp_total[TIED]/2);

    potentials p = {ppot2, npot2};
    return p;        
}

void main() {
    int hole[2]={49,40};
    int comm_cards[5] = {6,8,38};
    // int ourrank=rank5(hole,comm_cards);
    clock_t t;
    t = clock();
    potentials pot = potential2(hole,comm_cards);
    t = clock() - t;
    double time_taken = ((double)t)/CLOCKS_PER_SEC;
    printf("\n first function execution time: %f\n",time_taken);
    printf("ppot2: %f",pot.ppot);
    printf("npot2: %f",pot.npot);
    printf("\nmicroarray: %d",microarray);
    printf("\nlargearray: %d",largearray);
    // printf("collisions: %d",collisions);
    // printf("runs: %ld",runs); 
    // // printf("Our Rank: %d", ourrank);
}

 