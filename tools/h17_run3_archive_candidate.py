"""Inactive archive-only performance candidate; the frozen recorder is untouched.

Root must review, activate and freeze a new closure before this candidate can be
used for any measurement. Import constructs no controller or random generator.
"""
import tempfile
import zipfile
import numpy as np
from h17_run3_recording import Archive as FrozenArchive


class Archive(FrozenArchive):
    def seal(self,metadata):
        """Same reachable-blob fixed point, enqueue each newly discovered ID once.

        Traversal costs O(V+E) expected set operations rather than O(V squared).
        Payloads remain streamed one array/member at a time. ZIP copying retains
        the frozen array insertion order and original uncompressed NPY bytes.
        """
        roots=set();pending=[]
        def scan(value):
            if isinstance(value,str) and value in self.blobs:
                if value not in roots:
                    roots.add(value);pending.append(value)
            elif isinstance(value,dict):
                for v in value.values():scan(v)
            elif isinstance(value,(tuple,list)):
                for v in value:scan(v)
        scan(metadata)
        self.zip.close();self.temp.seek(0)
        source=zipfile.ZipFile(self.temp,'r')
        for key in self.arrays:
            if key.startswith('blob/') or not key.endswith(('timeline','hashes','call_refs','checkpoints')):continue
            if key.endswith('hashes'):continue
            with source.open(key+'.npy') as stream:a=np.lib.format.read_array(stream,allow_pickle=False)
            for v in a.flat:scan(bytes(v).decode('ascii'))
        seen=set()
        while pending:
            key=pending.pop()
            if key in seen:continue
            seen.add(key);scan(self.tags[key])
            if self.blobs[key]['kind']=='ndarray' and self.blobs[key]['dtype']=='|S64' and key not in self.non_reference_blobarrays:
                with source.open('blob/'+key+'.npy') as stream:a=np.lib.format.read_array(stream,allow_pickle=False)
                for v in a.flat:scan(bytes(v).decode('ascii'))
        target=tempfile.TemporaryFile('w+b')
        with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as dest:
            for key in list(self.arrays):
                if key.startswith('blob/') and key[5:] not in seen:
                    del self.arrays[key];self.blobs.pop(key[5:],None);continue
                with source.open(key+'.npy') as src,dest.open(key+'.npy','w',force_zip64=True) as dst:
                    while chunk:=src.read(1<<18):dst.write(chunk)
        source.close();self.temp.close();self.temp=target
        self.zip=zipfile.ZipFile(target,'a');return self.finish()
