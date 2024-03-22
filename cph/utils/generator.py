import typing as t

T = t.TypeVar('T')
U = t.TypeVar('U')


def apply(f: t.Callable[[T], None], gen: t.Generator[T, None, U]) -> U:
    try:
        while True:
            f(next(gen))
    except StopIteration as e:
        return e.value


def is_not_none(x: t.Any) -> bool:
    return x is not None


def count(iterable: t.Iterable[t.Any]) -> int:
    return sum(1 for _ in iterable)
