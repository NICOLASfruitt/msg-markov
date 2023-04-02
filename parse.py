# ça c'est juste le script pour formatter le fichier
# des messages brut

from os import remove

source = 'messages.txt'
out = 'src.txt'
prefixes = ['\n', 'http', '{Embed}', '{Reactions}', '{Attachments}', 'Started a call that lasted', 'Added ', 'Pinned ']
id = '!μ!'

sf = open(source, 'r')
tf = open('tmp', 'w')

skip = False
while (line := sf.readline()):
    #print(line, end='')

    if line.startswith('[') and (i := line.find(']')) != -1:
            skip = False
            if (j := line.find(' (')) != -1:
                tf.write(id + line[i+2:j] + '\n')
            else:
                tf.write(id + line[i+2:])

    elif not skip:
        #print(line.split())

        b = False
        for i in range(len(prefixes)):
            if (line.startswith(prefixes[i])):
                skip = True
                b = True
                break
        if not b:
            if len(line.split()) > 2:   # messages de 3 mots min
                tf.write(line)

sf.close()
tf.close()
tf = open('tmp', 'r')
of = open(out, 'w')

# id
of.write(id + '\n')
# mesages vides
while (line := tf.readline()):
    if line.startswith(id):
        while (next := tf.readline()):
            if next.startswith(id):
                line = next
            else:
                of.write(line)
                line = next
                break
    of.write(line)

tf.close()
remove('tmp')
of.close()