from math import log10
import numpy as np

# def custom_divmod(a, b):
#     quotient, remainder = divmod(a, b)
    
#     remainder = round(remainder, 10)
#     return quotient, remainder

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
    
def uint2bin(n, tam=8):
    return list(int(i) for i in bin(n)[2:].zfill(tam))

def bin2uint(val):
    return int(''.join(str(i) for i in val), 2)

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
class real_float_dec_repr:
    
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
    
class real_fixed_repr:
    
    def __init__(self, real_part=4, frac_part=4):
        self.real_part = real_part
        self.frac_part = frac_part
        
        for i in range(0, 30):
            if 2 ** i > 10 ** self.real_part:
                self.real_size = i
                break
        
        for i in range(0, 30):
            if 2 ** i > 10 ** self.frac_part:
                self.frac_size = i
                break
        
        self.bin_size = self.real_size + self.frac_size + 1
        
        
    def bin2fixed(self, val):
        
        sign, real, frac = val[:1], val[1:self.real_size + 1], val[self.real_size + 1:]
        dec_real = bin2int(real)
        dec_frac = bin2uint(frac)
        
        if sign[0] == 1:
            return dec_real + float('0.' + str(dec_frac).zfill(self.frac_part))
        else:
            return - (dec_real + float('0.' + str(dec_frac).zfill(self.frac_part)))
        

    def fixed2bin(self, n):
        
        sign = 1 if n >= 0 else 0
        real, frac = str(abs(n)).split('.')
        real, frac = int(real), int(frac.ljust(self.frac_part, '0'))
        
        if  (len(str(real)) > self.real_part and real >= 0) or \
            (len(str(real)) > self.real_part + 1 and real < 0) or \
            len(str(frac)) > self.frac_part:

            raise Exception('overflow')

        real_bin = int2bin(real, num_bits=self.real_size)
        frac_bin = uint2bin(frac, tam=self.frac_size)

        return [sign] + real_bin + frac_bin