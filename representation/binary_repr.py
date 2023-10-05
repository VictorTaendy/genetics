from math import log10
import numpy as np

def int2bin(n, num_bits=8):
    if n == 0:
        return [0] * num_bits
    elif n > 0:
        return list(reversed([n >> i & 1 for i in range(num_bits)]))
    else:
        n = abs(n) - 1
        return list(reversed([~(n >> i) & 1 for i in range(num_bits)]))

def bin2int(val):
    if val[0] == 1:
        inverted = ''.join(['1' if bit == 0 else '0' for bit in val])
        inverted_int = int(inverted, 2) + 1
        return -inverted_int
    else:
        return int(''.join(list(str(i) for i in val)), 2)

class bool_repr:
    
    @classmethod
    def bool2bin(self, n : bool):
        return [1] if True else [0]
    
    @classmethod
    def bin2bool(self, val : int):
        return True if val[0] == 1 else False
    
class int_repr:
    
    def __init__(self, num_bits : int = 8):
        self.num_bits = num_bits
    
    def int2bin(self, n):
        return int2bin(n, num_bits=self.num_bits)

    def bin2int(self, val):
        assert len(val) == self.num_bits
        
        return bin2int(val)
    
## representação flutuante com decimal
class float_dec:
    
    def __init__(self, mant_size : int = 24, exp_size : int = 8):
        self.mant_size = mant_size
        self.exp_size = exp_size
    
    @classmethod
    def _findPoint(self, n):
        return str(abs(n)).find('.')

    @classmethod
    def _findLen(self, n):
        return len(str(abs(n)).replace('.',''))

    @classmethod
    def _findExp(self, n):
        return self._findPoint(n) - self._findLen(n)

    @classmethod
    def _toMant(self, n):
        return int(str(n).replace('.', ''))

    def float2bin(self, n):
        mant_bin = int2bin(self._toMant(n), num_bits=self.mant_size)
        exp_bin = int2bin(self._findExp(n), num_bits=self.exp_size)
        return mant_bin + exp_bin

    def bin2float(self, val):
        split_dot = len(val) - self.exp_size
        assert split_dot == self.mant_size
        mant_bin, exp_bin = val[:split_dot], val[split_dot:]
        return float(bin2int(mant_bin) * 10 ** (bin2int(exp_bin)))