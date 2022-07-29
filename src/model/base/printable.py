class Printable:
    self_in_str = ""

    def to_str(self) -> str:
        return self.self_in_str

    def print(self, prefix: str = "-"):
        print(f"{prefix} {self.self_in_str}")
