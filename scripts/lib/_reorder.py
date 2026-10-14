"""Dev helper: reorder the `<!-- ░░ Name ░░ -->` blocks inside a generator's body literal."""
import re, sys

MARK = '      <!-- ░░ '

def reorder(path, order, closing_token='      {closing(', renumber=True):
    src = open(path, encoding='utf-8').read()
    start = src.index("    body = f'''") + len("    body = f'''")
    end = src.index("'''", start)
    body = src[start:end]
    tail = ''
    if closing_token in body:
        k = body.index(closing_token)
        tail = body[k:]
        body = body[:k]
    parts = body.split(MARK)
    head = parts[0]
    blocks = {}
    seq = []
    for p in parts[1:]:
        name = p[:p.index(' ░░ -->')]
        blocks[name] = MARK + p
        seq.append(name)
    missing = [n for n in order if n not in blocks]
    extra = [n for n in seq if n not in order]
    assert not missing, ('missing blocks', missing, seq)
    assert not extra, ('blocks not in order list', extra, seq)
    new_body = head + ''.join(blocks[n] for n in order) + tail
    if renumber:
        i = [0]
        def rep(m):
            i[0] += 1
            return f'<span class="kicker__num">{i[0]:02d}</span>'
        new_body = re.sub(r'<span class="kicker__num">\d{2}</span>', rep, new_body)
    src = src[:start] + new_body + src[end:]
    open(path, 'w', encoding='utf-8').write(src)
    return seq, order

if __name__ == '__main__':
    print(reorder(sys.argv[1], sys.argv[2].split(',')))
