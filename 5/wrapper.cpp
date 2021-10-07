#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

int main(int argc, char** argv)
{
	char* const args[] = {NULL};
    char* const envp[11] = {"BBB0", argv[2], "CCCC", "DDDD","AAA1", "BBB1", "CCC1", "DDD1","DDD2",argv[1],NULL};
    execve("/utumno/utumno5", args, envp);

    // this should never be called
    printf("Oh dear, something went wrong with execve! %s\n", strerror(errno));
    return 0x42;
}