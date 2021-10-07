#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>

struct a{
    char * p;
    int table[10];
};


int main(int argc,char **argv)

{
    ulong input;
    struct a obj;
    int pos;
    int val;

//    if (argc < 3) {
//        puts("Missing args");
//        /* WARNING: Subroutine does not return */
//        exit(1);
//    }
    obj.p = (char *)malloc(0x20);
    if (obj.p == (char *)0x0) {
        puts("Sorry, ran out of memory :-(");
        /* WARNING: Subroutine does not return */
        exit(1);
    }
    input = strtoul(argv[2],(char **)0x0,0x10);
    pos = strtoul(argv[1],(char **)0x0,10);
    if (10 < pos) {
        puts("Illegal position in table, quitting..");
        /* WARNING: Subroutine does not return */
        exit(1);
    }
    obj.table[pos] = input;
    strcpy(obj.p,argv[3]);
    printf("Table position %d has value %d\nDescription: %s\n",pos,obj.table[pos],obj.p);
    return 0;
}
