import olefile
f = r'C:\사전\【20】O 2179-2182排版页수4-金花顺-.backup'
ole = olefile.OleFileIO(f, write_mode=False)
streams = ole.listdir()
print('OLE streams:', len(streams))
for s in streams[:10]:
    name = '/'.join(s)
    print('  ' + name)
ole.close()
print('File integrity: OK')
