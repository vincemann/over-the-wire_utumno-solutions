#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

int main(int argc, char** argv)
{
	char* const args[] = {NULL};
	// does not do anything, we dont qcare about env vars
    // last arg is program to be called
//    printf("env var: %s\n", argv[1]);
    char* const envp[10] = {"BBB0", "BBBB", "CCCC", "DDDD","AAA1", "BBB1", "CCC1", "DDD1",argv[1],NULL};
    execve("/utumno/utumno3", args, envp);

    // this should never be called
    printf("Oh dear, something went wrong with execve! %s\n", strerror(errno));
    return 0x42;
}