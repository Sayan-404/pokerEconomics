#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define PLAYER_SIZE 55687
#define MICRO 149887
#define SMALL 149887
#define MEDIUM 149887
#define LARGE 149887

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
struct DataItem* microArray[MICRO];
struct DataItem* smallArray[SMALL];
struct DataItem* mediumArray[MEDIUM];
struct DataItem* largeArray[MEDIUM];


struct DataItem* oppSearch(int hand[],int handlength) {
    int i;
    long key=1;
    for(i=0;i<handlength;i++) {
        key *= primeArray[hand[i]];
    }
    // printf("%ld ",key);
    if(key<=311898) {
        // printf("in here");
        // exit(1);
        int hashIndex = key % MICRO;
        while(microArray[hashIndex] != NULL) {
        
            if(microArray[hashIndex]->key == key)
                return microArray[hashIndex]; 
                
            //go to next cell
            ++hashIndex;
            
            //wrap around the table
            hashIndex %= MICRO;
        }        
        return NULL;
    }
    else if(key>311898 && key<=121330189) {
        int hashIndex = key%SMALL;
        // if (hashIndex == 43983){
        //     printf("index: %d ",hashIndex);
        //     printf("key: %ld\n",key);
        // }
        while(smallArray[hashIndex] != NULL) {
            // printf("in here as well");
            if(smallArray[hashIndex]->key == key)
            return smallArray[hashIndex]; 
			
            //go to next cell
            ++hashIndex;
                
            //wrap around the table
            hashIndex %= SMALL;
        }
        return NULL;
    }
    else if(key>121330189 && key<=480745871) {
        int hashIndex = key%MEDIUM;
        while(mediumArray[hashIndex] != NULL) {
	
            if(mediumArray[hashIndex]->key == key)
            return mediumArray[hashIndex]; 
			
            //go to next cell
            ++hashIndex;
                
            //wrap around the table
            hashIndex %= MEDIUM;
        }
        return NULL;
    }
    else if(key>480745871) {

        int hashIndex = key%LARGE;
        while(largeArray[hashIndex] != NULL) {
	
            if(largeArray[hashIndex]->key == key)
            return largeArray[hashIndex]; 
			
            //go to next cell
            ++hashIndex;
                
            //wrap around the table
            hashIndex %= LARGE;
        }
        return NULL;
    }

}

struct DataItem* pSearch(int hand[],int handlength) {
    int i,j,temp;
    int swapped;
    long key=1;
    for(i=0;i<handlength;i++) {
        key *= primeArray[hand[i]];
    }

   
   int hashIndex = key % PLAYER_SIZE;  
	
   //move in array until an empty 
   while(PlayerArray[hashIndex] != NULL) {
	
      if(PlayerArray[hashIndex]->key == key)
         return PlayerArray[hashIndex]; 
			
      //go to next cell
      ++hashIndex;
		
      //wrap around the table
      hashIndex %= PLAYER_SIZE;
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
    if(key<=311898) {
        
        int hashIndex=key % MICRO;
        while(microArray[hashIndex] != NULL && microArray[hashIndex]->key != -1) {
            //go to next cell
            ++hashIndex;
            // collisions++;
            //wrap around the table
            hashIndex %= MICRO;
        }
        microArray[hashIndex] = item;

    }
    else if(key>311898 && key<=121330189) {
        // if(key == 317346)
        //     printf("\nhere");
        int hashIndex=key % SMALL;
        // if(key == 317346)
        //     printf("\nhashindex another: %d ",hashIndex);
        while(smallArray[hashIndex] != NULL && smallArray[hashIndex]->key != -1) {
            //go to next cell
            // if(key == 317346)
            // printf("\nInside the Hash Function another: %d ",hashIndex);
            ++hashIndex;
            // collisions++;
            //wrap around the table
            hashIndex %= SMALL;
        }
        smallArray[hashIndex] = item;
    }
    else if(key>121330189 && key<=480745871) {
        
        int hashIndex=key % MEDIUM;
        while(mediumArray[hashIndex] != NULL && mediumArray[hashIndex]->key != -1) {
            //go to next cell
            ++hashIndex;
            // collisions++;
            //wrap around the table
            hashIndex %= MEDIUM;
        }
        mediumArray[hashIndex] = item;
    }
    else if(key>480745871) {
        int hashIndex=key % LARGE;
        while(largeArray[hashIndex] != NULL && largeArray[hashIndex]->key != -1) {
            //go to next cell
            ++hashIndex;
            // collisions++;
            //wrap around the table
            hashIndex %= LARGE;
        }
        largeArray[hashIndex] = item;
    }
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
        long hashIndex = key % PLAYER_SIZE;

        //move in array until an empty or deleted cell
        while(PlayerArray[hashIndex] != NULL && PlayerArray[hashIndex]->key != -1) {
            //go to next cell
            ++hashIndex;
            // collisions++;
            //wrap around the table
            hashIndex %= PLAYER_SIZE;
    }
        
    PlayerArray[hashIndex] = item;
}