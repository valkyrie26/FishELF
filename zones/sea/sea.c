#include <stdio.h>
#include <stdlib.h>

__attribute__((used))
void sea_bass() {
    printf("You caught a Sea Bass!\n");
    system("python3 /workspaces/FishELF/tools/log_catch.py --zone sea --catch sea_bass --weather any --location sea");
}

__attribute__((used))
void coelacanth() {
    printf("You caught a Coelacanth!\n");
    system("python3 /workspaces/FishELF/tools/log_catch.py --zone sea --catch coelacanth --weather raining --location sea");
}


int main() {
    printf("Welcome to the Sea.\nUse your binary-fishing tools to explore the depths!\n");
    return 0;
}
