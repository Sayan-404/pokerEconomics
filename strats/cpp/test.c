#include<stdio.h>
#include "newlookuptable.h"
#include <phevaluator/phevaluator.h>
#include <phevaluator/rank.h>
#include <time.h>

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
void main() {
    int deck[52];
    create_deck(&deck[0]);
    int cons[5] = {25,35,8,12,40};
    int decksize=52;
    int i,j;
    clock_t t;
    for (i=0;i<5;i++)
        remove_card(&deck[0],cons[i],&decksize);
    t = clock();
    for(i=0;i<decksize-1;i++)
    {
        for(j=i+1;j<decksize;j++)
        {
            int remainingcards[2] = {deck[i],deck[j]};
            struct DataItem* pItem;
            pItem = pSearch(remainingcards,2);
            int ourrank7;
            if(pItem != NULL){
                // printf("found something");
                ourrank7 = pItem->data;
            }
            else {
                ourrank7=evaluate_7cards(cons[0],cons[1],cons[2],cons[3],cons[4],deck[i],deck[j]);
                pInsert(remainingcards,2,ourrank7);
            }
        }
    }
    t = clock() - t;
    double time_taken = ((double)t)/CLOCKS_PER_SEC;
    printf("\n first function execution time: %f",time_taken);
    t = clock();
    for(i=0;i<decksize-1;i++)
    {
        for(j=i+1;j<decksize;j++)
        {
            int remainingcards[2] = {deck[i],deck[j]};
            struct DataItem* pItem;
            pItem = pSearch(remainingcards,2);
            int ourrank7;
            if(pItem != NULL){
                // printf("found something");
                ourrank7 = pItem->data;
            }
            else {
                ourrank7=evaluate_7cards(cons[0],cons[1],cons[2],cons[3],cons[4],deck[i],deck[j]);
                pInsert(remainingcards,2,ourrank7);
            }
        }
    }
    t = clock() - t;
    time_taken = ((double)t)/CLOCKS_PER_SEC;
    printf("\n Second function execution time: %f",time_taken);
}