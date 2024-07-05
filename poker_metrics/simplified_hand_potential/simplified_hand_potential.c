#include <phevaluator/phevaluator.h>
#include <phevaluator/rank.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <Python.h>

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
potentials potential2(int hole[2], int comm_cards[3]) {
    float ahead=0;
    float behind=0;
    int deck[52];
    int decksize=52;
    int current_hand[5]={hole[0],hole[1],comm_cards[0],comm_cards[1],comm_cards[2]};
    int current_rank = evaluate_5cards(hole[0], hole[1], comm_cards[0], comm_cards[1], comm_cards[2]);
    create_deck(&deck[0]);
    int i,j;
    int rank;
    for(i=0;i<5;i++) {
        if(i<2)
            remove_card(&deck[0],hole[i],&decksize);
        else
            remove_card(&deck[0],comm_cards[i-2],&decksize);
    }
    for(i=0;i<decksize-1;i++) {
        for(j=i+1;j<decksize;j++)
            {
                int full_hand[7] ={hole[0],hole[1],comm_cards[0],comm_cards[1],comm_cards[2],deck[i],deck[j]};
                rank=evaluate_7cards(hole[0],hole[1],comm_cards[0],comm_cards[1],comm_cards[2],deck[i],deck[j]);  
            if(rank <= current_rank)
                ahead++;
            else
                behind++;
            }
    }
    float total = ahead+behind;
    total = total/2;
    potentials pot = {ahead/total,behind/total};
    // printf("ppot: %f",(float)ahead/total);
    // printf("npot: %f",(float)behind/total);
    // printf("ahead: %d",ahead);
    // printf("behind: %d",behind);
    
    return pot;
}

static PyObject* potential2_wrapper(PyObject* self, PyObject* args) {
    int hole[2];
    int comm_cards[3];

    if (!PyArg_ParseTuple(args, "(ii)(iii)", &hole[0], &hole[1], &comm_cards[0], &comm_cards[1], &comm_cards[2])) {
        return NULL;
    }

    potentials result = potential2(hole, comm_cards);

    return Py_BuildValue("(ff)", result.ppot, result.npot);
}

static PyMethodDef PotentialMethods[] = {
    {"potential2", potential2_wrapper, METH_VARARGS, "Calculate poker potential."},
    {NULL, NULL, 0, NULL}  // Sentinel
};

static struct PyModuleDef potentialmodule = {
    PyModuleDef_HEAD_INIT,
    "potential",
    NULL,
    -1,
    PotentialMethods
};

PyMODINIT_FUNC PyInit_potential(void) {
    return PyModule_Create(&potentialmodule);
}

int main() {
    int hole[2]={35,32};
    int comm_cards[3] = {31,27,21};
    clock_t t;
    t = clock();
    int i=0;
    
        // printf("\rIn progress %d", i/100);
    potential2(hole,comm_cards);
    t = clock() - t;
    double time_taken = ((double)t)/CLOCKS_PER_SEC;
    printf("\n first function execution time: %f\n",time_taken);
    // printf("ppot2: %f",pot.ppot);
    // printf("npot2: %f",pot.npot);
}
