from os.path import exists
from random import randint


def main():
    source = 'src.txt'
    compiled = 'cpld.txt'
    force_compile = False
    sep = '\1'  # pas ' ' à cause de 'nicolas fruit#3900' (y a un espace) 🐓
    # posera peut-être des problès plus tard, il faut un caractère que personne
    # utilise (\n marchera toujours mais fichier chiant à lire après)

    if not exists(compiled) or force_compile:
        d = make(source, compiled, sep)
    else:
        d = read(compiled, sep)
    #print(d)
    
    for _ in range(10):
        print(gen(d), end='')
        # spécifier qqn ("User#xxxx") pour des mots de cette personne seulement


def make(source, out, sep):
    sf = open(source, 'r')
    authors = []
    d: dict[str, tuple[int, dict[str, tuple[int, dict[str, int]]]]] = {}
    # data
    prfx = sf.readline()[:-1]  # renseigné en 1ere ligne
    # apparait devant l'auteur de chaque message

    auth: str = None
    k = 0
    while (line := sf.readline()): #and k < 300000:
        if line.startswith(prfx):
            auth = line[len(prfx):-1]
            if auth not in authors:
                authors.append(auth)
        else:
            words = []
            w = ''          # mot courant
            #alnm = True     # alpha-num avant
            whsp = False    # espace avant

            for c in line:
                if c == '\n':
                    break
                if c == ' ':
                    if not whsp:
                        words.append(w)
                        w = ''
                        whsp = True
                else:
                    w += c
                    whsp = False

            if w != '':
                words.append(w)
            words.append('\n')
            #print(words)

            last = '\0'
            for w in words:
                if last not in d:
                    d[last] = (0, {})
                n, last_d = d[last]

                if auth not in last_d:
                    last_d[auth] = (0, {})
                m, auth_d = last_d[auth]

                if w not in auth_d:
                    auth_d[w] = 0
    
                auth_d[w] += 1
                last_d[auth] = (m+1, auth_d)
                d[last] = (n+1, last_d)
                last = w
        k += 1
    #print(d, '\n')

    of = open(out, 'w')
    ids: dict[str, str] = {}
    # id unique par mot

    i = 0
    for auth in authors:
        ids[auth] = hex(i)[2:]
        i += 1
    for w in d:
        ids[w] = hex(i)[2:]
        i += 1
    ids['\n'] = hex(i)[2:]
    #print(ids)

    # table des ids
    for w in ids:
        of.write(w + sep + ids[w] + sep)
    of.write('\n')

    # écriture du dict
    for w, (n, w_d) in d.items():
        of.write(hex(n)[2:] + sep + ids[w] + sep)
        for auth, (m, a_d) in w_d.items():
            of.write(hex(m)[2:] + sep + ids[auth] + sep)
            for next, k in a_d.items():
                of.write(hex(k)[2:] + sep + ids[next] + sep)
    
    of.close()
    return d


def read(source, sep):
    f = open(source, 'r')
    ids: dict[int, str] = {}
    d: dict[str, tuple[int, dict[str, tuple[int, dict[str, int]]]]] = {}

    acc = ''
    b = True
    id = None

    # table des ids (jusque \n car ajouté en dernier)
    while (c := f.read(1)) != '\n':
        if c == sep:
            b = not b
            if b:   # tous les 2 sep
                w, _id = acc.split(sep)
                id = int(_id, 16)
                ids[id] = w
                acc = ''
            else:
                acc += c
        else:
            acc += c
    # ajout manuel
    ids[id+1] = '\n'
    # skip l'id de \n (on vient de le rentrer)
    while (c := f.read(1)) != '\n':
        pass

    #print(ids)

    last, auth, next = None, None, None
    n, m = None, None
    nk, mk = 0, 0

    # création du dict
    while c := f.read(1):
        if c == sep:
            b = not b
            if b:   # tous les 2 sep

                if n is None:
                    _n, _last = acc.split(sep)
                    n = int(_n, 16)
                    last = ids[int(_last, 16)]
                    d[last] = (n, {})
                    
                elif m is None:
                    _m, _auth = acc.split(sep)
                    m = int(_m, 16)
                    auth = ids[int(_auth, 16)]
                    d[last][1][auth] = (m, {}) 
                    
                else:
                    _k, _next = acc.split(sep)
                    k = int(_k, 16)
                    next = ids[int(_next, 16)]
                    d[last][1][auth][1][next] = k
                    mk += k

                    if mk == m:
                        nk += m
                        m = None
                        mk = 0
                    if nk == n:
                        n = None
                        nk = 0
                acc = ''
            else:
                acc += c
        else:
            acc += c
    #print(d)

    return d


def _gen(d: dict[str, tuple[int, dict[str, tuple[int, dict[str, int]]]]]):
    result = ''
    last = '\0'
    
    while last != '\n':
        n, last_d = d[last]
        i = randint(0, n)
        for _, (m, auth_d) in last_d.items():
            i += -m
            if i < 0:
                j = randint(0, m)
                for w, k in auth_d.items():
                    j += -k
                    if j < 0:
                        result += w + ' '
                        last = w
                        break
                break
    
    return result[:-1]


def gen(d: dict[str, tuple[int, dict[str, tuple[int, dict[str, int]]]]], auth: str = None):
    if auth is None:
        return _gen(d)

    result = ''
    last = '\0'

    while last != '\n':
        m, auth_d = d[last][1][auth]
        j = randint(0, m)
        for w, k in auth_d.items():
            j += -k
            if j < 0:
                result += w + ' '
                last = w
                break

    return result[:-1]

if __name__ == '__main__':
    main()