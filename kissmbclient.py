import os
from subprocess import PIPE, Popen
import subprocess as sp

class smb:

    username = 'bert.klandermans@wur.nl'
    password = 'koe12343'

    def exec(command):
        cmd = "smbclient //WURNET.NL/dfs-root -U "+smb.username+"%"+smb.password+" -c'"+command+"'"
        print(cmd)
        return sp.getoutput(cmd)

    def list(dir):
        return smb.exec("ls "+dir)

    def size(file):
        ls = smb.list(file)
        for line in ls.split('\n'):
            if 'Unable to initialize messaging context' not in line:
                line = line.split('  ')
                print(line)
                return  np.uint64(line[len(line)-2].replace('A',''))

    def put(source, destination, overwrite=False):
        smb.exec('put '+source+' '+destination)
        if np.uint64(os.path.getsize(source)) == smb.size(destination):
            return True
        return False

   def get(source, destination, overwrite=False):
        smb.exec('get '+source+' '+destination)    
    
    
    def move(source, destination):
        if smb.put(source, destination) == True:
            os.system('rm '+source)


print(smb.move('test.txt', 'asg/WLR_Dataopslag/DairyCampus/3406_Nlas/test.txt'))
