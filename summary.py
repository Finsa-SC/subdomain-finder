class ReconStats:
    def __init__(self):
        super().__setattr__('allowed', ['ok', 'forbidden', 'ssl_error', 'server_error'])
        for name in self.allowed:
            super().__setattr__(f"_{name}", 0)

    def log(self, http_status, https_status):
        if 200 in (http_status, https_status):
            self.ok += 1
        elif 403 in (http_status, https_status):
            self.forbidden += 1
        elif None in (http_status, https_status):
            self.ssl_error += 1
        elif any(code in (500, 501, 502) for code in (http_status, https_status)):
            self.server_error += 1

    def summary(self):
        print("\n\nSummary:")
        print(f"Host Up      : {self.ok}")
        print(f"Forbidden    : {self.forbidden}")
        print(f"SSL Error    : {self.ssl_error}")
        print(f"Server Error : {self.server_error}")

    def __setattr__(self, name, value):
        if name in getattr(self, 'allowed', []):
            current = getattr(self, f"{name}")

            if value < 0 or value > current + 1:
                print("[!] Alert: attempt to manipulate points")
                return
            super().__setattr__(f"_{name}", value)
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.allowed:
            return getattr(self, f"_{name}")
        raise AttributeError