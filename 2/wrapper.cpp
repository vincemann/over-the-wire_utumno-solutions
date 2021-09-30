#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

int main(int argc, char** argv)
{
	char* const args[] = {NULL};
	// does not do anything, we dont qcare about env vars
    // last arg is program to be called
    char* const envp[11] = {"AAA0", "BBB0", "CCC0", "DDD0","AAA1", "BBB1", "CCC1", "DDD1", "EEEE",argv[2] , NULL};
    execve(argv[1], args, envp);

    // this should never be called
    printf("Oh dear, something went wrong with execve! %s\n", strerror(errno));
    return 0x42;
}