#include <iostream>
#include "Stack.h"
using namespace std;

void createStack(Stack &S) {
    S.top = -1;
}

bool isEmpty(Stack S) {
    return S.top == -1;
}

bool isFull(Stack S) {
    return S.top == MAX_STACK - 1;
}

void push(Stack &S, int nilai) {
    if (isFull(S)) {
        cout << "[Warning] Stack overflow! Tidak dapat menambahkan " << nilai << endl;
    } else {
        S.top++;
        S.data[S.top] = nilai;
        cout << "[Push] Sukses memasukkan nilai " << nilai << " ke Stack." << endl;
    }
}

int pop(Stack &S) {
    if (isEmpty(S)) {
        cout << "[Warning] Stack underflow! Stack masih kosong." << endl;
        return -1;
    } else {
        int val = S.data[S.top];
        S.top--;
        cout << "[Pop] Berhasil mengeluarkan nilai " << val << " dari Stack." << endl;
        return val;
    }
}

void printStack(Stack S) {
    if (isEmpty(S)) {
        cout << "[Display] Stack Kosong [ ]" << endl;
    } else {
        cout << "[Display] Isi Stack (Top -> Bottom): [ ";
        for (int i = S.top; i >= 0; i--) {
            cout << S.data[i] << (i > 0 ? ", " : " ");
        }
        cout << "]" << endl;
    }
}

int main() {
    Stack tumpukan;
    createStack(tumpukan);

    cout << "========================================" << endl;
    cout << "   SIMULASI OPERASI STACK (C++)         " << endl;
    cout << "   NgeLaprak — Modul 3 Struktur Data    " << endl;
    cout << "========================================" << endl;

    push(tumpukan, 10);
    push(tumpukan, 25);
    push(tumpukan, 40);
    printStack(tumpukan);

    pop(tumpukan);
    printStack(tumpukan);

    return 0;
}
