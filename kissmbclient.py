#Keep it stupid & simple Wrapper

from subprocess import PIPE, Popen
import subprocess as sp
import os

class smb:

    username = 'bert.klandermans@wur.nl'
    password = 'P@$$W0RD'
    
    # executes the smbcient command to the Wur dfs-root
    def exec(command):
        cmd = "smbclient //WURNET.NL/dfs-root -U "+smb.username+"%"+smb.password+" -c'"+command+"'"
        return sp.getoutput(cmd)
    
    # return the text output of the ls command
    def list(dir):
        return smb.exec("ls "+dir+'/*')
    
    # convert text output to dictionary
    def listDict(dir):
        c = smb.list(dir)
        c = c.splitlines()
        if len(c) > 0:
            newLines = []
            for line in c:
                # TODO: A bit of an obscure way of splitting. It is possible that the string occurance occurs in a filename. This works for me now.
                new = {}
                if ' A ' in line:
                    line = line.replace(' NaN ','  ')
                    new['filename'] = line.split(' A ')[0].strip(' ')
                    new['size'] = int(line.split(' A ')[1].strip(' ').split(' ')[0])
                    newLines.append(new)
                if ' D ' in line:
                    line = line.replace(' NaN ','  ')
                    new['dirname'] = line.split(' D ')[0].strip(' ')
                    new['size'] = int(line.split(' D ')[1].strip(' ').split(' ')[0])
                    if new['dirname'] not in ('.','..'):
                        newLines.append(new)
            return newLines
        return []

    dirCache = []   
    def checkDir(destinationPath):
        dd = destinationPath.replace('\\','/')
        dd = dd.replace('/*','')
        dd = dd.split('/')
        #TODO:: Move static root to static parameter in object
        dir = 'asg/WLR_Dataopslag/DairyCampus'
        for d in dd:
            dir = dir+'/'+d
            if dir not in smb.dirCache:
                smb.exec('mkdir '+dir)
                smb.dirCache.append(dir)

    def put(source, destinationPath,destinationFilename, overwrite=False):
        smb.checkDir(destinationPath)
        print(smb.exec('put '+source+' '+destinationPath+'/'+destinationFilename))
        # disabled filesize validation
        # if np.uint64(os.path.getsize(source)) == smb.size(destinationPath+'/'+destinationFilename):
        #     return True
        # smb.size(destinationPath+'/'+destinationFilename)
        return False

    def get(source, destination, overwrite=False):
        smb.exec('get '+source+' '+destination)

    def move(source, destinationPath,destinationFilename):
        if smb.put(source,  destinationPath,destinationFilename) == True:
            os.system('rm '+source)
    
    # static parameter to store cache
    lsCache = {}
    def exists(destionationPath, destionationFilename):
        if destionationPath not in smb.lsCache:
            smb.lsCache[destionationPath] = []
            listfiles = smb.listDict(destionationPath)
            if len(listfiles) > 0:
                smb.lsCache[destionationPath] = pd.DataFrame(listfiles)['filename'].values
                print(smb.lsCache[destionationPath])
        if destionationFilename in smb.lsCache[destionationPath]:
            return True
        return False
