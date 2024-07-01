#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define SIZE 2000000

int collisions=0;

struct DataItem {
   int data;   
   long key;
};

struct primemap{
   int card;
   int prime;
};
struct DataItem* hashArray[SIZE]; 
struct DataItem* dummyItem;
struct DataItem* item;

int hashCode(long key) {
   return key % SIZE;
}

struct primemap* primearray[52];
int prime(int index) {
   int i=0,j;
   int num=2;
   while(i!=index) {
      int k=0;
      for(int j=1;j<=num;j++)
         if(num%j == 0) 
            k++;
      
      if(k==2) {
         i++;
      }
      if(index == i)
         return num;
      num++;
   }
}
void assignPrimes() {

}

struct DataItem *search(int hand[],int handlength) {
   //get the hash
   int i,j,temp;
   int swapped;
   long key=0;
   for(i=0;i<handlength-1;i++) {
        swapped = 0;
        for(j=0;j<handlength - i - 1;j++) {
             if (hand[j] > hand[j + 1]) {
                temp = hand[i];
                hand[i] = hand[j];
                hand[j] = temp;
                swapped = true;
            }
            if(temp == false)
                break;
        }
   }
   for(i=0;i<handlength;i++) {
        key = key*100 + hand[i];
   }

   
   long hashIndex = hashCode(key);  
	
   //move in array until an empty 
   while(hashArray[hashIndex] != NULL) {
	
      if(hashArray[hashIndex]->key == key)
         return hashArray[hashIndex]; 
			
      //go to next cell
      ++hashIndex;
		
      //wrap around the table
      hashIndex %= SIZE;
   }        
	
   return NULL;        
}

void insert(int hand[],int handlength,int data) {
    int i,j,temp;
    int swapped;
    long key=0;
    for(i=0;i<handlength-1;i++) {
        swapped = 0;
        for(j=0;j<handlength - i - 1;j++) {
             if (hand[j] > hand[j + 1]) {
                temp = hand[i];
                hand[i] = hand[j];
                hand[j] = temp;
                swapped = true;
            }
            if(temp == false)
                break;
        }
   }
   for(i=0;i<handlength;i++) {
        key = key*100 + hand[i];
   }

    struct DataItem *item = (struct DataItem*) malloc(sizeof(struct DataItem));
    item->data = data;  
    item->key = key;

    //get the hash 
    long hashIndex = hashCode(key);

    //move in array until an empty or deleted cell
    while(hashArray[hashIndex] != NULL && hashArray[hashIndex]->key != -1) {
        //go to next cell
        ++hashIndex;
        collisions++;
        //wrap around the table
        hashIndex %= SIZE;
   }
	
   hashArray[hashIndex] = item;
}

// int main() {
//    for(int i=1;i<=52;i++) 
//       printf("%d\n",prime(i));
//    //  int rank=1;
//    //  int arr[] = {40,49,3,8,38};
//    //  insert(arr,5,2);
//    //  item = search(arr,5);
//    //  int i;
//    //  for(i=0;i<=1;i++) {
//    //      if(item != NULL) {
//    //          printf("Element found: %d\n", item->data);
//    //      } else {
//    //          printf("Element Not Found");
//    //          insert(arr,5,rank);
//    //      }
//    //  }
// }