#include <stdio.h>
#include <stdlib.h>

// ------------- FISH (hidden functions) -------------
void magikarp() {
    printf("You caught a Magikarp! It's flopping around uselessly.\n");
    system("python3 /workspaces/FishELF/tools/log_catch.py --zone pond --catch magikarp --weather any --location pond");
}

void guppy() {
    printf("You caught a Guppy! Small but slippery.\n");
    system("python3 /workspaces/FishELF/tools/log_catch.py --zone pond --catch guppy --weather any --location pond");
}

// ------------- ENTRY -------------
int main() {
    puts("Welcome to the Pond.\nUse your binary-fishing tools to discover hidden fish!");
    return 0;
}
