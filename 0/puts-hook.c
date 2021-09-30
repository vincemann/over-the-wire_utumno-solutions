#include <stdio.h>

int puts ( const char * str ) {
        // find adrs on the stack
        printf("%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x\n");
        // investigate goodlooking
        printf("%s",0x08048402);
        printf("%s",0x080484a5);
        printf("%s",0x08048490);
        return 0;
}
