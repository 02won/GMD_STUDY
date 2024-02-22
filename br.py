from byte_buffer2 import *

class BootRecord:
    def __init__(self, buffer):
        bb = ByteBuffer2(buffer)
        bb.offset = 0x0b
        self.sector_size = bb.get_uint2_le() # bytes_per_sector
        self.sector_count = bb.get_uint1() # sectors_per_cluster
        self.cluster_size = self.sector_count * self.sector_size #FAT 크기

        bb.offset = 0x0e
        self.reserved_sector_count = bb.get_uint2_le()
        self.fat_area_address = self.reserved_sector_count * self.sector_size

        bb.offset = 0x10
        self.fat_count = bb.get_uint1()
        
        bb.offset = 0x24
        self.fat_sector_count = bb.get_uint4_le()
        self.data_area_address = self.fat_area_address + self.fat_count * self.fat_sector_count * self.sector_size

    def __str__(self) -> str:
        cs = hex(self.cluster_size)
        da = hex(self.data_area_address)

        return f"cluster_size: {cs}, data_area: {da}"

if __name__ == "__main__":
    file = open("fat32.mdf", 'rb')
    b0 = file.read(0x200)
    br = BootRecord(b0)
    print(br)