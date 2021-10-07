#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>

int main(int argc, char **argv)
{
    size_t amount_bytes_to_memcpy;
    char buf [64];
    char c[65212];
    ushort j;
    int i;

    // 0xffffffff
    // 0x7ffffffe
    // 0b10000000000000000000000000000000 = int min = 0x10000000 = 268435456(unsigned) = -0 (signed)
    // 0b11111111111111111111111111111111 = -1
    // 0b10000000000000000000000000000001
//    char* input = "268435456";

//    char* input = "65538";
//    char* input = "131074";
    char* input = "2147483648";
    char* payload = "AAAA";
    amount_bytes_to_memcpy = atoi(input);
    printf("%d\n", (ushort)amount_bytes_to_memcpy);
    if (0x3f < (ushort)amount_bytes_to_memcpy) {
        /* WARNING: Subroutine does not return */
        exit(1);
    }
    memcpy(buf,payload,amount_bytes_to_memcpy);
    return 0;
}
