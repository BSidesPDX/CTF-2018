// gcc main.c -o secureshell
#include <stdio.h>	//printf
#include <string.h>	//strcmp
#include <stdlib.h> //exit

#define USERNAME "r00t"
#define PASSWORD_FILE "password.txt"

void main()
{
	char input[1024];
	char password[255];
	char password_in[255];
	FILE *fd;

	setbuf(stdout, NULL);
	printf("Welcome to my custom secure shell!\n");

	// Zero out input + password
	memset(password, 0x00, 255);
	memset(password_in, 0x00, 255);
	memset(input, 0x00, 1024);

	// Read password file
	fd = fopen(PASSWORD_FILE, "r");
	if (!fd)
	{
		printf("Could not open file: %s\n", PASSWORD_FILE);
		exit(1);
	}
	fread(password, 1, sizeof(password)-1, fd);

	// Prompt for username
	printf("Username: ");
	scanf("%1023s", &input);
	if (strcmp(USERNAME, input))
	{
		printf("Invalid Username: ");
		// strfmt vuln
		printf(input);
		exit(1);
	}

	// Prompt for password
	printf("Password: ");
	scanf("%254s", &password_in);
	if (strcmp(password, password_in))
	{
		printf("Invalid password\n");
		exit(1);
	}

	// Execute shell
	system("/bin/sh");
}
