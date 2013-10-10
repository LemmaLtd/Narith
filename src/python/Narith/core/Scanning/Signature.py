'''
[Narith]
Author: Saad Talaat
File:   Signature.py
brief:  Signature based scan & detection
'''
import os, sqlite3
'''
Yara based signature scanner:
    This scanner only scans files. Scanning packets
    will cause huge contention since yara scanner
    is uses on thread-pool.
'''
class YaraScanner(object):
    try:
        import yaraa
    except ImportError as e:
        print "yara package is not installed"
        print "using Thirdparty yara package"
        from ThirdParty import yara
    def __init__(self,data_dir="Data/"):
        self.rulefiles  = []
        self.files      = []
        database_dir    = "Database/"

        for root,subfolders, files in os.walk(database_dir):
            for f in files:
                if "yara" in f[-4:]:
                    self.rulefiles.append(root+"/"+f)
        for root,subfolder,files in os.walk(data_dir):
            for f in files:
                self.files.append(root+"/"+f)

    def scan(self):
        data_matches = []
        matches = []
        for f in self.files:
            fd = open(f,'r')
            data_matches = self._match(fd.read())
            if not data_matches:
                fd.close()
                continue
            matches += data_matches
            fd.close()
        return matches

    def _match(self,data):
        matches = []
        for db in self.rulefiles:
            rules = yara.compile(db)
            match = rules.match_data(data)
            if not match:
                continue
            matches.append(rules.match_data(data))
        return matches

    def close(self):
        del self.files
        del self.rulefiles


'''
Basic signature finder
'''
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
        if not filesflag:
            return

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
            i+=1
            pack_matches = self._match(packet)
            if packmatches:
                for match in pack_matches:
                    matches['packets'].append((i,packet,match))
        if not self.filesflag:
            return matches
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

    def close(self):
        del self.packets
        del self.filesflag
        del self.signdbs
        del self.files
