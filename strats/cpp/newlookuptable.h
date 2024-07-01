#ifndef NEWLOOKUPTABLE_H
#define NEWLOOKUPTABLE_H

struct DataItem {
    int data;
    long key;
};

struct DataItem* oppSearch(int hand[], int handlength);
struct DataItem* pSearch(int hand[], int handlength);
void oppInsert(int hand[], int handlength, int data);
void pInsert(int hand[], int handlength, int data);

#endif
