
def clean(filename='train.txt'):
    with open('train_clean.txt', 'w') as out:
        with open(filename) as inp:
            idx = 0
            for line in inp.readlines():
                if idx > 1:
                    line = line.split(' ')
                    out.write(line[0] + ' ' + line[-1])
                idx += 1


if __name__ == '__main__':
    clean()

