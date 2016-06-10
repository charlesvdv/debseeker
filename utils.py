def strip_str_list(strlist):
    """
    Trim each string in a list
    """
    newstr = []
    for s in strlist:
        newstr.append(s.strip())
    return newstr

def remove_duplicates(elements):
    """
    Remove duplicates existing in a list
    """
    baselist = []
    for i in elements:
        if not i in baselist:
            baselist.append(i)

