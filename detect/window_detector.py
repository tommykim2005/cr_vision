from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID



def find_window(name_contains: str):
    windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)

    for window in windows:
        owner = window.get("kCGWindowOwnerName", "")
        name = window.get("kCGWindowName", "")

        if name_contains.lower() in owner.lower() or name_contains.lower() in name.lower():
            bounds = window["kCGWindowBounds"]
            return {
                "left": bounds["X"],
                "top": bounds["Y"],
                "width": bounds["Width"],
                "height": bounds["Height"]
            }
        

    return None
