import jieba

__all__ = ['process_text']


def process_text(text):
    out = [item.lower() for item in jieba.cut(text) if item != ' ']
    out = ' '.join(out)
    out = out.replace('\n', '[SEP]')
    return out
