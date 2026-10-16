#ifndef STACK_H
#define STACK_H

#define MAX_STACK 10

struct Stack {
    int data[MAX_STACK];
    int top;
};

void createStack(Stack &S);
bool isEmpty(Stack S);
bool isFull(Stack S);
void push(Stack &S, int nilai);
int pop(Stack &S);
void printStack(Stack S);

#endif
