#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define PLAYER_SIZE 55687
#define MICRO 2654435769
// #define SMALL 149887
// #define MEDIUM 149887
// #define LARGE 307573

struct DataItem {
   int data;   
   long key;
};
int primeArray[] = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
        127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
        179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
        233, 239
    };


struct DataItem* PlayerArray[PLAYER_SIZE];
// struct DataItem* microArray = (struct Dataitem*)malloc(MICRO * sizeof(struct Dataitem*));
struct DataItem* microArray[MICRO];
// struct DataItem* smallArray[SMALL];
// struct DataItem* mediumArray[MEDIUM];
// struct DataItem* largeArray[LARGE];

struct DataItem* oppSearch(int hand[],int handlength) {
    int i;
    long key=1;
    for(i=0;i<handlength;i++) {
        key *= primeArray[hand[i]];
    }
    // printf("%ld ",key);
    if(key) {
        // printf("in here");
        // exit(1);
        while(microArray[key] != NULL) {
        
            if(microArray[key]->key == key)
                return microArray[key]; 
                
            //go to next cell
            ++key;
            
            //wrap around the table
            key %= MICRO;
        }        
        return NULL;
    }
    // else if(key>311898 && key<=121330189) {
    //     int key = key%SMALL;
    //     // if (key == 43983){
    //     //     printf("index: %d ",key);
    //     //     printf("key: %ld\n",key);
    //     // }
    //     while(smallArray[key] != NULL) {
    //         // printf("in here as well");
    //         if(smallArray[key]->key == key)
    //         return smallArray[key]; 
			
    //         //go to next cell
    //         ++key;
                
    //         //wrap around the table
    //         key %= SMALL;
    //     }
    //     return NULL;
    // }
    // else if(key>121330189 && key<=480745871) {
    //     int key = key%MEDIUM;
    //     while(mediumArray[key] != NULL) {
	
    //         if(mediumArray[key]->key == key)
    //         return mediumArray[key]; 
			
    //         //go to next cell
    //         ++key;
                
    //         //wrap around the table
    //         key %= MEDIUM;
    //     }
    //     return NULL;
    // }
    // else {
    //     largearray++;
    //     int key = key%LARGE;
    //     while(largeArray[key] != NULL) {
	
    //         if(largeArray[key]->key == key)
    //         return largeArray[key]; 
			
    //         //go to next cell
    //         ++key;
                
    //         //wrap around the table
    //         key %= LARGE;
    //     }
    //     return NULL;
    // }

}

struct DataItem* pSearch(int hand[],int handlength) {
    int i,j,temp;
    int swapped;
    long key=1;
    for(i=0;i<handlength;i++) {
        key *= primeArray[hand[i]];
    }

   //move in array until an empty 
   while(PlayerArray[key] != NULL) {
	
      if(PlayerArray[key]->key == key)
         return PlayerArray[key]; 
			
      //go to next cell
      ++key;
		
      //wrap around the table
      key %= PLAYER_SIZE;
   }        
	
   return NULL;
}

void oppInsert(int hand[],int handlength,int data) {
    int i;
    long key=1;

    for(i=0;i<handlength;i++) {
            key *= primeArray[hand[i]];
    }
    struct DataItem *item = (struct DataItem*) malloc(sizeof(struct DataItem));
        item->data = data;  
        item->key = key;
    if(key) {
        while(microArray[key] != NULL && microArray[key]->key != -1) {
            //go to next cell
            ++key;
            // collisions++;
            //wrap around the table
            key %= MICRO;
        }
        microArray[key] = item;

    }
    // else if(key>311898 && key<=121330189) {
    //     // if(key == 317346)
    //     //     printf("\nhere");
    //     int key=key % SMALL;
    //     // if(key == 317346)
    //     //     printf("\nkey another: %d ",key);
    //     while(smallArray[key] != NULL && smallArray[key]->key != -1) {
    //         //go to next cell
    //         // if(key == 317346)
    //         // printf("\nInside the Hash Function another: %d ",key);
    //         ++key;
    //         // collisions++;
    //         //wrap around the table
    //         key %= SMALL;
    //     }
    //     smallArray[key] = item;
    // }
    // else if(key>121330189 && key<=480745871) {
        
    //     int key=key % MEDIUM;
    //     while(mediumArray[key] != NULL && mediumArray[key]->key != -1) {
    //         //go to next cell
    //         ++key;
    //         // collisions++;
    //         //wrap around the table
    //         key %= MEDIUM;
    //     }
    //     mediumArray[key] = item;
    // }
    // else {
    //     int key=key % LARGE;
    //     while(largeArray[key] != NULL && largeArray[key]->key != -1) {
    //         //go to next cell
    //         ++key;
    //         // collisions++;
    //         //wrap around the table
    //         key %= LARGE;
    //     }
    //     largeArray[key] = item;
    // }
}
void pInsert(int hand[],int handlength,int data) {
    int i,j,temp;
    int swapped;
    long key=1;
    for(i=0;i<handlength;i++) {
            key *= primeArray[hand[i]];
    }

        struct DataItem *item = (struct DataItem*) malloc(sizeof(struct DataItem));
        item->data = data;  
        item->key = key;

        //get the hash
        //move in array until an empty or deleted cell
        while(PlayerArray[key] != NULL && PlayerArray[key]->key != -1) {
            //go to next cell
            ++key;
            // collisions++;
            //wrap around the table
    }
        
    PlayerArray[key] = item;
}