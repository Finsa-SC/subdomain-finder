from dataclasses import dataclass

@dataclass
class ScanConfig:
    timeout: float
    thread: int
    available: bool
    verbose: bool
    redirect: bool
    no_wildcard: bool
    save_file_plain: bool
    save_file_json: bool