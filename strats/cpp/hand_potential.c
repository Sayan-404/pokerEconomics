#include <assert.h>
#include <phevaluator/phevaluator.h>
#include <phevaluator/rank.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define CARD_LENGTH 3
#define DECK_SIZE 52

#define AHEAD 1
#define TIED 0
#define BEHIND 2

typedef struct {
    float ppot;
    float npot;
} potentials;

void create_deck(char (*deck)[CARD_LENGTH]) {

    char ranks[] = {'2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'};
    char suits[] = {'c', 'd', 'h', 's'};
    int index = 0;

    for (int i = 0; i < 13; i++) {
        for (int j = 0; j < 4; j++) {
            deck[index][0] = ranks[i];
            deck[index][1] = suits[j];
            deck[index][2] = '\0';
            index++;
        }
    }
}
void remove_card(char (*deck)[CARD_LENGTH], char* card_to_remove, int* deck_size) {
    int i;
    for (i = 0; i < *deck_size; i++) {
        if (strcmp(deck[i], card_to_remove) == 0) {
            // Swap the card to remove with the last card in the deck
            strcpy(deck[i], deck[*deck_size - 1]);
            (*deck_size)--;
            return;
        }
    }
    printf("Card %s not found in the deck.\n", card_to_remove);
}


int rank_to_int(char rank_char) {
    switch (rank_char) {
        case '2': return 0;
        case '3': return 1;
        case '4': return 2;
        case '5': return 3;
        case '6': return 4;
        case '7': return 5;
        case '8': return 6;
        case '9': return 7;
        case 'T': return 8;
        case 'J': return 9;
        case 'Q': return 10;
        case 'K': return 11;
        case 'A': return 12;
        default: return -1;
    }
}

int suit_to_int(char suit_char) {
    switch (suit_char) {
        case 'c': return 0;
        case 'd': return 1;
        case 'h': return 2;
        case 's': return 3;
        default: return -1;
    }
}

int card_to_int(char *card_str) {
    int rank = rank_to_int(card_str[0]);
    int suit = suit_to_int(card_str[1]);
    return rank * 4 + suit;
}

int rank7(char hole[2][3], char comm_cards[5][3]) {
    int ids[7];
    for (int i = 0; i < 2; i++) {
        ids[i] = card_to_int(hole[i]);
        // printf("id: %d",ids[i]);
    }
    int k;
    for (int i = 2; i < 7; i++) {
        ids[i] = card_to_int(comm_cards[i%5]);
    }
    int final_rank = evaluate_7cards(ids[0], ids[1], ids[2], ids[3], ids[4], ids[5], ids[6]);
  return final_rank;
}
int rank5(char hole[2][3], char comm_cards[3][3]) {
    int ids[7];
    for (int i = 0; i < 2; i++) {
        ids[i] = card_to_int(hole[i]);
        // printf("id: %d",ids[i]);
    }
    for (int i = 2; i < 5; i++) {
        ids[i] = card_to_int(comm_cards[i%3]);
    }
    int final_rank = evaluate_5cards(ids[0], ids[1], ids[2], ids[3], ids[4]);
  return final_rank;
}

// char* makedeck()
potentials potential2(char hole[2][3], char comm_cards[5][3]) {

    float hp[3][3];
    float hp_total[3];

    float ppot2, npot2;
    float ourrank5,ourrank7,opprank;

    //Creating the deck
    char deck[DECK_SIZE][CARD_LENGTH];
    int deck_size = DECK_SIZE;
    create_deck(&deck[0]);

    ourrank5 = rank5(hole,comm_cards);
    int i,j;
    int k;

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
        
    for(i=0;i<deck_size-1;i++)
        for(j=i+1;j<deck_size;j++)
            {
                char oppcards[2][3];
                strcpy(oppcards[0],deck[i]);
                strcpy(oppcards[1],deck[j]);

                opprank = rank5(oppcards,comm_cards);
                // printf("%f",opprank);
                if(ourrank5 < opprank)
                    index=AHEAD;
                else if(ourrank5 == opprank)
                    index = TIED;
                else
                    index = BEHIND;
                
                char t_deck[DECK_SIZE][CARD_LENGTH];
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
                        char remaining_cards[2][CARD_LENGTH];
                        strcpy(remaining_cards[0],t_deck[l]);
                        strcpy(remaining_cards[1],t_deck[m]);

                        hp_total[index] += 1;

                        char five_card_board[5][CARD_LENGTH];
                        int h;
                        // printf("%s ",remaining_cards[0]);
                        // printf("%s ",remaining_cards[1]);
                        // printf("\n");
                        for(h=0;h<5;h++) {
                            if(h<3)
                                strcpy(five_card_board[h],comm_cards[h]);
                            else
                                strcpy(five_card_board[h],remaining_cards[h-3]);
                        }
                        ourrank7=rank7(hole,five_card_board);
                        opprank=rank7(oppcards,five_card_board);
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
    int i;
    // for(i=0;i<100;i++)
    // {
        
    //     // char deck[DECK_SIZE][CARD_LENGTH];
    //     // create_deck(&deck[0]);
    //     // char used[5][CARD_LENGTH];
    //     // char hole[2][CARD_LENGTH];
    //     // char comm[3][CARD_LENGTH];
    //     // int j,k;
        
    //     // for(j=0;i<2;j++){
    //     //     char card[] = deck[(int) rand() % 51];
    //     //     for(k=0;k<5;k++)
    //     //         if(strcmp(card,used[k]) == 0)
        
    //     char hole[2][3] = {"Ad","Qc"};
    //     char comm_cards[5][3] = {"3h","4c","Jh"};
    //     potentials pot = potential2(hole,comm_cards);
    // }
    char hole[2][3] = {"Ad","Qc"};
    char comm_cards[5][3] = {"3h","4c","Jh"};
    // int ourrank=rank5(hole,comm_cards);
    potentials pot = potential2(hole,comm_cards);
    // printf("ppot2: %f",pot.ppot);
    // printf("npot2: %f",pot.npot);
    // // printf("Our Rank: %d", ourrank);
}

 