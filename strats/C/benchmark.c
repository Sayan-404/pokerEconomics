#include<stdio.h>

#include <simplified_hand_potential.h>
#include <hand_potential.h>
#include <stdlib.h>

#include <time.h>
void main() {
    int a,b;
    int i,j,k;
    int runs;
    printf("Enter the number of runs");
    scanf("%d",&runs);
    int count=0;
    int decksize = 52;
    clock_t t;
    double time_taken=0;
    float ppot_difference_list[runs];
    float npot_difference_list[runs];

    for(i=0;i<runs;i++)
    {
        srand(time(NULL));
        int hole[2]={rand()%52,rand()%52};
        int comm_cards[3]={rand()%52,rand()%52,rand()%52};
        t = clock();
        potentials pot = potential2(hole,comm_cards);
        simplepotentials simplepot = simple_potential2(hole,comm_cards);
        t = clock() - t;
        printf("hand_potential ppot: %f\n",pot.ppot);
        printf("simple hand potential ppot: %f\n",simplepot.ppot);
        ppot_difference_list[count]=pot.ppot - simplepot.ppot;
        npot_difference_list[count]=pot.npot - simplepot.npot;
        time_taken += ((double)t)/CLOCKS_PER_SEC;

    }
    // for(a=0;a<decksize-4;a++)
    //     for(b=a+1;b<decksize-3;b++)
    //         for(i=b+1;i<decksize-2;i++)
    //             for(j=i+1;j<decksize-1;j++)
    //                 for(k=j+1;k<decksize;k++) {
    //                     if(count == runs)
    //                         break;
    //                     int hole[2] = {a,b};
    //                     int comm_cards[3] = {i,j,k};
    //                     t = clock();
    //                     potentials pot = potential2(hole,comm_cards);
    //                     simplepotentials simplepot = simple_potential2(hole,comm_cards);
    //                     t = clock() - t;
    //                     printf("hand_potential ppot: %f\n",pot.ppot);
    //                     printf("simple hand potential ppot: %f\n",simplepot.ppot);
    //                     ppot_difference_list[count]=pot.ppot - simplepot.ppot;
    //                     npot_difference_list[count]=pot.npot - simplepot.npot;
    //                     time_taken += ((double)t)/CLOCKS_PER_SEC;
    //                     count++;
    //                 }

    printf("Runs: %d\n",runs);
    printf("timetaken: %f\n",time_taken);
    printf("average time taken: %f\n",time_taken/runs);   
    float avg_ppot_devation=0;
    float avg_npot_deviation=0;
    for(i=0;i<runs;i++) {
        avg_ppot_devation += ppot_difference_list[i];
        avg_npot_deviation += npot_difference_list[i];
    }
    printf("average ppot deviation: %f\n",avg_ppot_devation/runs);
    printf("average npot deviation: %f",avg_npot_deviation/runs);
}