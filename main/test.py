from Quartz import *
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID

windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
for w in windows:
    print(w.get("kCGWindowOwnerName",""), "|", w.get("kCGWindowName",""))