#ifndef NEWLOOKUPTABLE_H
#define NEWLOOKUPTABLE_H
#define MICRO 265443576

int oppSearch(int hand[], int handlength);
int pSearch(int hand[], int handlength);

extern int* microArray;

void oppInsert(int hand[], int handlength, int data);
void pInsert(int hand[], int handlength, int data);

#endif
