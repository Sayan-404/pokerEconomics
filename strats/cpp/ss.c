#include <pthread.h>
#include <assert.h>
#include <phevaluator/phevaluator.h>
#include <phevaluator/rank.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <lookuptable/lookuptable.h>
#include <time.h>

#define DECK_SIZE 52

#define AHEAD 1
#define TIED 0
#define BEHIND 2
#define NUM_THREADS 4

typedef struct {
    int start;
    int end;
    int hole[2];
    int comm_cards[5];
    float hp[3][3];
    float hp_total[3];
} thread_data_t;

typedef struct {
    float ppot;
    float npot;
} potentials;

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
void *potential2_thread(void *arg) {
    thread_data_t *data = (thread_data_t *)arg;
    int i, j, k, l, m, h;
    int deck[DECK_SIZE];
    int deck_size = DECK_SIZE;
    int ourrank5, ourrank7, opprank;
    float ppot2, npot2;

    create_deck(&deck[0]);
    ourrank5 = rank5(data->hole, data->comm_cards);

    for (i = 0; i < 3; i++) {
        data->hp_total[i] = 0;
        for (j = 0; j < 3; j++)
            data->hp[i][j] = 0;
    }

    for (k = 0; k < 2; k++)
        remove_card(&deck[0], data->hole[k], &deck_size);
    for (k = 0; k < 3; k++)
        remove_card(&deck[0], data->comm_cards[k], &deck_size);

    for (i = data->start; i < data->end; i++) {
        for (j = i + 1; j < deck_size; j++) {
            int oppcards[2] = {deck[i], deck[j]};
            opprank = rank5(oppcards, data->comm_cards);
            int index = (ourrank5 < opprank) ? AHEAD : (ourrank5 == opprank) ? TIED : BEHIND;

            int t_deck[DECK_SIZE];
            int t_deck_size = DECK_SIZE;
            create_deck(&t_deck[0]);
            int l;
            for (l = 0; l < 2; l++) {
                remove_card(&t_deck[0], data->hole[l], &t_deck_size);
                remove_card(&t_deck[0], oppcards[l], &t_deck_size);
            }
            for (l = 0; l < 3; l++) {
                remove_card(&t_deck[0], data->comm_cards[l], &t_deck_size);
            }

            for (l = 0; l < t_deck_size - 1; l++) {
                for (m = l + 1; m < t_deck_size; m++) {
                    int remaining_cards[2] = {t_deck[l], t_deck[m]};
                    data->hp_total[index] += 1;

                    int five_card_board[5];
                    int h;
                    for (h = 0; h < 5; h++) {
                        if (h < 3)
                            five_card_board[h] = data->comm_cards[h];
                        else
                            five_card_board[h] = remaining_cards[h - 3];
                    }
                    int pItem = pSearch(remaining_cards, 2);
                    if (pItem != 0) {
                        ourrank7 = pItem;
                    } else {
                        ourrank7 = rank7(data->hole, five_card_board);
                        pInsert(remaining_cards, 2, ourrank7);
                    }
                    opprank = rank7(oppcards, five_card_board);
                    if (ourrank7 < opprank)
                        data->hp[index][AHEAD] += 1;
                    else if (ourrank7 == opprank)
                        data->hp[index][TIED] += 1;
                    else
                        data->hp[index][BEHIND] += 1;
                }
            }
        }
    }

    pthread_exit(NULL);
}

potentials potential2(int hole[2], int comm_cards[5]) {
    pthread_t threads[NUM_THREADS];
    thread_data_t thread_data[NUM_THREADS];
    int chunk_size = DECK_SIZE / NUM_THREADS;
    int start = 0;

    for (int i = 0; i < NUM_THREADS; i++) {
        thread_data[i].start = start;
        start += chunk_size;
        thread_data[i].end = (i == NUM_THREADS - 1) ? DECK_SIZE : start;
        memcpy(thread_data[i].hole, hole, sizeof(int) * 2);
        memcpy(thread_data[i].comm_cards, comm_cards, sizeof(int) * 5);

        pthread_create(&threads[i], NULL, potential2_thread, (void *)&thread_data[i]);
    }

    float ppot2 = 0, npot2 = 0;
    float hp_total[3] = {0};
    float hp[3][3] = {0};

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);

        for (int j = 0; j < 3; j++) {
            hp_total[j] += thread_data[i].hp_total[j];
            for (int k = 0; k < 3; k++) {
                hp[j][k] += thread_data[i].hp[j][k];
            }
        }
    }

    ppot2 = (hp[BEHIND][AHEAD] + hp[BEHIND][TIED] / 2 + hp[TIED][AHEAD] / 2) / (hp_total[BEHIND] + hp_total[TIED] / 2);
    npot2 = (hp[AHEAD][BEHIND] + hp[AHEAD][TIED] / 2 + hp[TIED][BEHIND] / 2) / (hp_total[AHEAD] + hp_total[TIED] / 2);

    potentials p = {ppot2, npot2};
    return p;
}

int main() {
    int hole[2] = {49, 40};
    int comm_cards[5] = {6, 8, 38};

    assignArray(); // Assuming this function initializes any necessary data structures

    clock_t start_time = clock();
    potentials pot = potential2(hole, comm_cards);
    clock_t end_time = clock();

    double time_taken = ((double)(end_time - start_time)) / CLOCKS_PER_SEC;
    printf("\nFunction execution time: %f seconds\n", time_taken);
    printf("ppot2: %f\n", pot.ppot);
    printf("npot2: %f\n", pot.npot);

    freeArray(); // Assuming this function frees any dynamically allocated data structures

    return 0;
}
