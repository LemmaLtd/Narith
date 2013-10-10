'''
[Narith]
Author: Saad Talaat
File:   Signature.py
brief:  Signature based scan & detection
'''
import os, sqlite3


class SignatureScanner(object):

    # Map of tables of dbs
    databases = {
            'shellcode.db': ['windows'],
            'encoders.db': ['windows'],
                }

    def __init__(self, rawPackets, filesflag=False):
        self.packets    = rawPackets
        self.filesflag  = filesflag
        self.signdbs    = []
        self.files      = []
        database_dir = 'Database/'
        data_dir = 'Data/'

        for root, subfolders, files in os.walk(database_dir):
            for f in files:
                if "db" in f[-2:]:
                    self.signdbs.append(root+"/"+f)
        for root, subfolder, files in os.walk(data_dir):
            for f in files:
                self.files.append(root+"/"+f)

    def scan(self):
        i = 0
        data_matches = []
        pack_matches = []
        matches = {
                'packets' : [],
                'files'   : []
                }
        for packet in self.packets:
            continue
            i+=1
            pack_matches = self._match(packet)
            if packmatches:
                for match in pack_matches:
                    matches['packets'].append((i,packet,match))

        for f in self.files:
            fd = open(f,'r')
            dat_matches = self._match(fd.read())
            fd.close()
            if dat_matches:
                for match in dat_matches:
                    matches['files'].append((f,match))
        return matches
    def _match(self, data):
        matches = []
        for db in self.signdbs:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            try:
                for table in self.databases[db.split("/")[-1]]:
                    cursor.execute("select * from "+table)
                    for entry in cursor:
                        sign =  "".join([str(x.decode('hex')) for x in entry[1].split("\\x")])
                        if sign in data:
                            matches.append(db+"/"+table+"/"+entry[0])
            except KeyError:
                pass
        return matches
