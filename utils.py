import pandas as pd

def write_text(list1,list2,columns=None,separate=False):
    if separate:
        sep = [',']*len(list1)
        data = list(zip(list1,sep,list2))
    else:
        data = list(zip(list1,list2))
    df = pd.DataFrame(data, columns=columns)
    return df.to_string(index=False, header=False)

def read_text(text_in):
    list = [[],[]]
    lines = text_in.splitlines()
    for line in lines:
        print(line)
        elements = line.strip(' ').split(',',1)
        print(elements)
        for idy,element in enumerate(elements):
            list[idy].append(element.strip(' '))

    return (list[0],list[1])

def place_conversion(place):
    if place <= 1:
        return '1st'
    elif place == 2:
        return '2nd'
    elif place == 3:
        return '3rd'
    else:
        return str(place)+'th'

def param_read(p, input):
    pars = p
    warning = ''

    for i in range(len(pars)):
        try:
            pars[i] = int(input[i+1])
        except IndexError:
            warning += f'Missing input at position {i}, using default value.'+'\n'
        except ValueError:
            warning += f'Invalid input at position {i}. using default value.'+'\n'

    return pars, warning

def param_read_nita(input):
    course = None
    place = 1
    warning = None
    if input:
        course = input[0]
        if input[1:]:
            try:
                place = int(input[1])
                if place not in range(11):
                    place = 1
            except ValueError:
                warning = 'Wrong position given, will return the time of 1st place, please give a position between 1 and 10.'
        else:
            warning = 'No position given, will return the time of 1st place.'
    else:
        warning = 'Missing input for track abbreviation.'

    return course, place, warning            

if __name__ == '__main__':
    pass
