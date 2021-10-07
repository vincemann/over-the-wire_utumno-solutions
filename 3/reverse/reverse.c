#include <stdio.h>
#include <stdlib.h>



char find_target_char(char target_index, int i){
    for (int j = 0; j < 255; ++j) {
        char index = (char)j ^ (char)i * '\x03';
        if (index == target_index){
            printf("%c",j);
            return j;
        }
        if(j == 254){
            printf("failed for index: %d\n",index);
            exit(1);
        }
    }
}



int main(int argc, char** argv) {
    int start_index = (int)strtol(argv[1],NULL,0);
    int amount_chars = (int)strtol(argv[2],NULL,0);

    char index_char_buf [amount_chars];
    int count = 0;
    for (int targetIndex = start_index; targetIndex < start_index + amount_chars; ++targetIndex) {
        char index_char = find_target_char(targetIndex, count);
        index_char_buf[count]=index_char;
        count+=1;
    }
    return 0;
}





