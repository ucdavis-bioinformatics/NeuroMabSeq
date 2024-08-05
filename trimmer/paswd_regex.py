import sys
import re


def check_strong(password):
    # check if at least one lowercase, one upper case, and one special character and a length of 10
    pattern = "^.*(?=.{10,})(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[$&+,:;=?@#'<>.^*()%!-]).+$"
    result = re.findall(pattern, password)
    if (result):
        return True
    else:
        return False


def check_medium(password):
    # check if at least one lowercase, one upper case, and one special character and a length of at least 8
    pattern = "^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[$&+,:;=?@#'<>.^*()%!-]).+$"
    result = re.findall(pattern, password)

    # also need to check if no special char but greater than or equal to 8
    pattern2 = "^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).+$"
    result2 = re.findall(pattern2, password)
    if (result):
        return True
    elif(result2):
        return True
    else:
        return False


#for line in sys.stdin:
def check_line(line):
    # TODO make this regex as well but not really sure all special characters are perfectly accounted for.
    if len(line) > 25 or len(line) < 6 or ' ' in line or '{' in line or '}' in line or '~' in line or '|' in line:
        print("invalid")
    elif check_strong(line):
        print("strong")
    elif check_medium(line):
        print("medium")
    else:
        print("weak")


check_line('iT*2spX*8')
check_line('iTt2spXt8')
check_line('Nufu&YM21S')
check_line('Nufu:YM21S')

check_line('gZAGel')
check_line('2N# 9k')