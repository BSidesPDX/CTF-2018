// gcc main.c -o pwnclub
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define ASCII_ART "" \
"                           _       _     \n" \
"                          | |     | |    \n" \
"  _ ____      ___ __   ___| |_   _| |__  \n" \
" | '_ \\ \\ /\\ / / '_ \\ / __| | | | | '_ \\ \n" \
" | |_) \\ V  V /| | | | (__| | |_| | |_) |\n" \
" | .__/ \\_/\\_/ |_| |_|\\___|_|\\__,_|_.__/ \n" \
" | |                                     \n" \
" |_|                                     \n\n\n" \
"1) Never let no one know how much code you hold\n" \
"2) Never let them know your next move\n" \
"3) Never trust nobody, IRC is bad luck when you chat too much\n" \
"4) SHUT THE F*CK UP\n" \
"5) Never do no hacks where you rest at\n" \
"6) Any logged cleartext, forget it. Encrypt all your data, take those bytes off the record\n" \
"7) Keep identites and profiles completely seperated\n" \
"8) Never keep no weight on you. Those cats that run your hacks can jack coins too\n" \
"9) Use your right to your attorney, keep away from police\n" \
"10) SHUT THE ACTUAL F*CK UP\n\n"

void print_ascii_art()
{
    printf(ASCII_ART);
}

void print_menu()
{
    printf("-----------------------------------------\n");
    printf("-------------- Pick a Vuln --------------\n");
    printf("1) strfmt\n");
    printf("2) stack overflow\n");
    printf("3) exit\n");
}

void strfmt()
{
    char input[256];
    memset(input, 0x00, 256);

    printf("Give me your strfmt payload: ");
    read(STDIN_FILENO, &input, 255);
    input[255] = 0x00;

    printf("\n");
    printf(input);
}

void stack_overflow(char* input)
{
    read(STDIN_FILENO, input, 1024);
    printf("See you on the otherside!\n");
}

int read_int()
{
    int choice;
    int ret;
    printf("> ");
    ret = scanf("%d", &choice);
    if (ret == EOF)
    {
        printf("Something bad happened...");
        exit(1);
    }

    if (ret == 0)
    {
        while(fgetc(stdin) != '\n');
        return 0;
    }
    return choice;
}

void main()
{
    int choice;
    char input[20];

    setbuf(stdout, NULL);

    print_ascii_art();

    while (1)
    {
        print_menu();
        choice = read_int();

        switch(choice){
            case 1:
                strfmt();
                break;
            case 2:
                stack_overflow(input);
                break;
            case 3:
                return;
            default:
                printf("What you say??\n");
        }
    }
}
