with open("04-1-spoc-memdiskdata.md", 'r') as file:
    for line in file:
        if not line.strip():
            break
    pdbr = file.readline()
    pdbr = pdbr[14:].split('[')[0]
    pdbr = int(pdbr, base=16)
    for line in file:
        if line.strip() == '~~~':
            break
    memory = []
    for line in file:
        line = line.strip()
        if line == '~~~':
            break
        line = list(map(lambda x:int(x, base=16), line[9:].split()))
        memory.append(line)
    for line in file:
        if line.strip() == '~~~':
            break
    disk = []
    for line in file:
        line = line.strip()
        if line == '~~~':
            break
        line = list(map(lambda x:int(x, base=16), line[9:].split()))
        disk.append(line)
while True:
    virtual = int(input(), base=16)
    pde_index = virtual >> 10
    pde_addr = pdbr + pde_index
    pde_contents = memory[pde_addr >> 5][pde_addr & 0x1f]
    valid = pde_contents >> 7
    pfn = pde_contents & 0x7f
    print('pde index:0x{0:x}({0:b}) pde contents:(0x{1:x}, {1:b}, valid {2}, pfn 0x{3:x}(page 0x{3:x}))'.format(pde_index, pde_contents, valid, pfn))
    if not valid:
        continue
    pte_index = virtual >> 5 & 0x1f
    pte_contents = memory[pfn][pte_index]
    valid = pte_contents >> 7
    pfn = pte_contents & 0x7f
    print('pte index:0x{0:x}({0:b}) pte contents:(0x{1:x}, {1:b}, valid {2}, pfn 0x{3:x})'.format(pte_index, pte_contents, valid, pfn))
    offset = virtual & 0x1f
    physical = (pfn << 5) + offset
    if valid == 1:
        value = memory[pfn][offset]
        print("To Physical Address {0:x}({0:b}) --> Value: {1:x}".format(physical, value))
    else:
        if pfn == 0x7f:
            print("Not exist")
        else:
            value = disk[pfn][offset]
            print("To Disk Sector Address {0:x}({0:b}) --> Value: {1:x}".format(physical, value))
