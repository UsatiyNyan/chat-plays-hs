import typing as t
from pathlib import Path
from cph.utils import generator


def get_dir(hs_root: Path) -> Path | None:
    if not hs_root.exists():
        return None
    logs_dir = hs_root / 'Logs'
    if not logs_dir.exists():
        return None
    return logs_dir


def get_latest_log_dir(logs_dir: Path) -> Path | None:
    log_dirs = (log_dir for log_dir in logs_dir.iterdir() if log_dir.is_dir())
    return max(log_dirs,
               key=lambda log_dir: log_dir.stat().st_birthtime,
               default=None)


def get_path(hs_root: Path | None = None) -> Path | None:
    hs_root = hs_root or Path('C:/Program Files (x86)/Hearthstone')
    logs_dir = get_dir(hs_root)
    if logs_dir is None:
        return None
    latest_log_dir = get_latest_log_dir(logs_dir)
    if latest_log_dir is None:
        return None
    power_log_path = latest_log_dir / 'Power.log'
    if not power_log_path.exists():
        return None
    return power_log_path


def read_lines_from_offset(power_log_path: Path,
                           offset: int) -> t.Generator[str, None, int]:
    with power_log_path.open('r', encoding='utf-8') as file:
        file.seek(offset)
        yield from file
        offset = file.tell()
    return offset


def handle_lines_once(line_handler: t.Callable[[str], None],
                      prev_power_log_path: Path | None,
                      offset: int) -> t.Tuple[Path | None, int]:
    power_log_path = get_path()
    if power_log_path is None:
        return None, 0

    offset = offset if power_log_path == prev_power_log_path else 0
    lines = read_lines_from_offset(power_log_path, offset)
    offset = generator.apply(line_handler, lines)
    return power_log_path, offset
