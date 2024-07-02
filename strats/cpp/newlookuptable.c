#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define PLAYER_SIZE 55687
#define MICRO 2894777321

// #define SMALL 149887
// #define MEDIUM 149887
// #define LARGE 307573

int used=0;

int primeArray[] = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
        127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
        179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
        233, 239
    };



int *PlayerArray;
// struct DataItem* microArray = (struct Dataitem*)malloc(MICRO * sizeof(struct Dataitem*));
// struct DataItem* smallArray[SMALL];
// struct DataItem* mediumArray[MEDIUM];
// struct DataItem* largeArray[LARGE];
int *microArray;

void freeArray() {
    free(microArray);
    free(PlayerArray);
}
void assignArray() {
    microArray =(int *)calloc(MICRO,sizeof(int));
    PlayerArray=(int *)calloc(MICRO,sizeof(int));

}
int oppSearch(int hand[],int handlength) {
    // if(used == 0)
    // {
    //     microArray =(int *)calloc(MICRO,sizeof(int));
    //     used++;
    // }
    int i;
    long key=1;
    for(i=0;i<handlength;i++) {
        key *= primeArray[hand[i]];
    }
    // printf("%ld ",key);
    if(microArray[key] != 0)
    {
        return microArray[key];
    }
    else {
        return 0;
    }
}

int pSearch(int hand[],int handlength) {
    int i;
    long key=1;
    for(i=0;i<handlength;i++) {
        key *= primeArray[hand[i]];
    }
    if(PlayerArray[key] != 0)
        return PlayerArray[key];
    else
        return 0;
}

void oppInsert(int hand[],int handlength,int data) {
    int i;
    long key=1;

    for(i=0;i<handlength;i++) {
            key *= primeArray[hand[i]];
    }
    microArray[key] = data;
}
void pInsert(int hand[],int handlength,int data) {
   int i;
    long key=1;

    for(i=0;i<handlength;i++) {
            key *= primeArray[hand[i]];
    }
    PlayerArray[key] = data;
}