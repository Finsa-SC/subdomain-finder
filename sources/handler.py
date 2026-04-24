from sources import hackertarget, crtsh, alienvault


def get_subdomain(domain: str, use_all: bool = False, selected_source: str = None):
    main_set = set()

    source_map = {
        "hackertarget": hackertarget.fetch_hackertarget,
        "crtsh": crtsh.fetch_crtsh,
        "alienvault": alienvault.fetch_alienvault
    }

    to_run = source_map.keys() if use_all else (selected_source or ["hackertarget"])

    for s_name in to_run:
        if s_name in source_map:
            print(f"[C] Fetching from {s_name}")
            result = source_map[s_name](domain)
            main_set.update(result)
    return list(main_set)