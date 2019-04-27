
def extract_digit(num,start,numd=1,n=None):
    num_str = str(num)
    if n is not None:
        while len(num_str) < n: num_str = '0'+num_str
    digit_str = ''
    for digit in range(start,start+numd): digit_str += num_str[digit]
    return int(digit_str)