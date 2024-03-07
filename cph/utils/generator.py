import typing as t

T = t.TypeVar('T')
U = t.TypeVar('U')


def apply(f: t.Callable[[T], None], gen: t.Generator[T, None, U]) -> U:
    try:
        while True:
            f(next(gen))
    except StopIteration as e:
        return e.value
