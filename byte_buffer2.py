#!/usr/bin/env python

from struct import *

class ByteBuffer2:
    def __init__(self, bs):
        self.m_data = bs
        self.m_offset = 0
        self.m_limit = len(bs)

    def has_remaining(self):
        return self.m_offset < self.m_limit 

    def size(self):
        return len(self.m_data)

    def limit(self):
        return len(self.m_data)

    @property
    def offset(self):
        return self.m_offset

    #offset 설정
    @offset.setter
    def offset(self, pos):
        self.m_offset = pos
        return self

    def unget(self, pos):
        self.m_offset -= pos
        return self

    def skip(self, count):
        self.m_offset += count
        return self

    def get_uint2_be(self):
        s = self.m_offset
        r = self.m_data[s:s+2]
        self.m_offset += 2
        return unpack('>H', r)[0]

    def get_uint1(self):
        r = self.m_data[self.m_offset]
        self.m_offset += 1
        return r

    def get_uint2_le(self):
        s = self.m_offset # 현재 offset 값을 s에 저장
        r = self.m_data[s:s+2] # 현재 offset으로 부터 2바이트를 읽어 r에 저장
        self.m_offset += 2 # offset을 2 증가시켜 다음에 읽을 위치를 2바이트 뒤로 이동시킴
        return unpack('<H', r)[0] # 읽어들인 2바이트 데이터 r을 리틀 엔디언 방식의 2바이트 부호 없는 정수로 변환

    # 현재 offset으로부터 4바이트를 읽어 리틀 엔디안 방식의 4바이트(unsigned int) 부호 없는 정수로 반환
    def get_uint4_le(self):
        s = self.m_offset
        r = self.m_data[s:s+4]
        self.m_offset += 4
        return unpack('<I', r)[0]

    def get_uint4_be(self):
        s = self.m_offset
        r = self.m_data[s:s+4]
        self.m_offset += 4
        return unpack('>I', r)[0]

    def get_ascii(self, *args):
        if len (args) == 0: return self.__get_ascii0()
        if len (args) == 1: return self.__get_ascii1(int(args[0]))
        return None

    def __get_ascii1(self, size):
        s = self.m_offset
        e = self.m_offset + size
        res = self.m_data[s:e].decode('utf-8')
        self.m_offset += size
        return res

    def __get_ascii0(self):
        index = self.m_data.find(b'\x00', self.m_offset)
        if index == -1:
            self.m_offset = self.m_limit
            return self.m_data[self.m_offset:].decode('utf-8')

        res = self.m_data[self.m_offset:index].decode('utf-8')
        self.m_offset = index + 1
        return res

    def get_utf16_le(self, size):
        o = self.m_offset
        res = self.m_data[o:o+size*2].decode('utf-16le')
        self.m_offset += size*2
        return res

    def compare_range(self, offset, count, val):
        if offset + count > self.m_limit:
            return False

        for i in range(offset, offset+count):
            if self.m_data[i] != val:
                return False

        return True

    def change_cur_to(self, ch):
        b = bytearray(self.m_data)
        b[self.m_offset] = ord(ch)
        self.m_data = bytes(b)
        return self

