//
// Created by kali on 10/3/21.
//

#include "string.h"
#include <stdio.h>
#include <stdlib.h>



// finds char creating target index
char find_target_char(char target_index, int i){
    for (int j = 0; j < 255; ++j) {
        char index = (char)j ^ (char)i * '\x03';
        if (index == target_index){
            printf("found char: %0x\n",j);
            return j;
        }
        if(j == 254){
            printf("failed for index: %d\n",index);
            exit(1);
        }
    }
}


//void test_xor(char a, char b){
//    printf("a = %x\n",a);
//    printf("b = %x\n",b);
//    char r = a ^ b;
//    char r2 = r ^ a;
//    printf("r = %x\n",r);
//    printf("r2 (should be b ) %x\n",r2);
//}
//
//void test_xor2(char ch, char index){
//    printf("ch = %x\n", ch);
//    printf("index = %x\n", index);
//    char overflow_index = ch ^ index * '\x03';
//    char r2 = overflow_index ^ index * '\x03';
//    char r2 = overflow_index ^ ch * '\x03'; // not working
//    printf("overflow_index = %x\n", overflow_index);
//    printf("r2 (should be ch ) %x\n",r2);
//}

int main(int argc,char **argv)
{
    int ch;
    char index_buf_program [24];
    char overflow_buf [24];
    int c;
    int i;
    char overflow_index;

    char index_char_buf [24];
    char alpha_buf [24];

//    const char* indexes = "\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !\"#$%&\'()*+,-";
//    const char* indexes = "\x17\x1b\x19\x1a\x1b\x1c\x1d\x1e\x1f !\"#$%&\'()*+,-";


    int count = 0;
    for (char targetIndex = 23; targetIndex < 23 + 23; ++targetIndex) {
        char index_char = find_target_char(targetIndex, count);
        index_char_buf[count]=index_char;
        count+=1;
    }
    printf("index chars: %.*x\n",23,index_char_buf);
//    int len = strlen(index_char_buf);
//    memcpy(index_char_buf, index_char_buf, len);

    const char* alpha = "AAAABAAACAAADAAAEAAAFAA";
    memcpy(alpha_buf,alpha, strlen(alpha));


    i = 0;
    while( 1 ) {
//        ch = getchar();
        ch = index_char_buf[i];
        if ((ch == -1) || (0x17 < i)) break;
        index_buf_program[i] = (char)ch;
        index_buf_program[i] = index_buf_program[i] ^ (char)i * '\x03';

        overflow_index = index_buf_program[i];
        // overflow_index is index
//        ch = getchar();
        ch = alpha[i];
        overflow_buf[overflow_index] = (char)ch;
        i = i + 1;
    }
    return 0;
}