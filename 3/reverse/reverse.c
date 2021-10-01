#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
//    input_buf[i] ^ (char)i * '\x03';
    int index = (int)strtol(argv[2],NULL,0);
    char c = (char)(*argv[1]);
    char result =  c ^ (char)index * '\x03';
    printf("%c",result);
    return 0;
}
