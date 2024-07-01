#ifndef LOOKUPTABLE_H
#define LOOKUPTABLE_H

#define SIZE 2000000

struct DataItem {
    int data;
    long key;
};

extern struct DataItem* hashArray[SIZE];
extern struct DataItem* dummyItem;
extern struct DataItem* item;

int hashCode(long key);
struct DataItem* search(int hand[], int handlength);
void insert(int hand[], int handlength, int data);

#endif /* LOOKUPTABLE_H */
