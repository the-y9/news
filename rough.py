from datetime import date
today = date.today()

# Default ISO format
print(today)  # 2026-02-05
print(today.strftime("%Y"))
print(today.strftime("%b_%Y"))  # 05-Feb-2026
print(today.strftime("%d_%b_%Y"))  # 05-Feb-2026