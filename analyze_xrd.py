import csv
import math

INPUT = "data/raw/A-Z-1.csv"
WAVELENGTH = 1.5406  # Cu Kα, Å

peaks = []

with open(INPUT, newline="") as f:
    reader = csv.DictReader(f)
    reader.fieldnames = [name.strip() for name in reader.fieldnames]
    print("CSV columns:", reader.fieldnames)
    rows = list(reader)

for i in range(1, len(rows) - 1):
    x0 = float(rows[i - 1]["#twotheta"])
    y0 = float(rows[i - 1]["yobs"])

    x1 = float(rows[i]["#twotheta"])
    y1 = float(rows[i]["yobs"])

    x2 = float(rows[i + 1]["#twotheta"])
    y2 = float(rows[i + 1]["yobs"])

    if y1 > y0 and y1 >= y2:
        theta = math.radians(x1 / 2.0)
        d = WAVELENGTH / (2.0 * math.sin(theta))

        peaks.append((x1, y1, d))

peaks.sort(key=lambda p: p[1], reverse=True)

print("Top XRD peaks")
print("==============================")

for two_theta, intensity, d in peaks[:20]:
    print(f"2theta={two_theta:7.3f}  I={intensity:8.1f}  d={d:7.4f}")

# ZnO/wurtzite candidate indexing
# Use the strongest representative peaks:
d100 = min(peaks, key=lambda p: abs(p[0] - 31.76))[2]
d002 = min(peaks, key=lambda p: abs(p[0] - 34.40))[2]
d101 = min(peaks, key=lambda p: abs(p[0] - 36.28))[2]

a = 2.0 * d100 / math.sqrt(3.0)
c = 2.0 * d002

print()
print("Candidate hexagonal unit cell")
print("==============================")
print(f"d100 = {d100:.4f} Å")
print(f"d002 = {d002:.4f} Å")
print(f"d101 = {d101:.4f} Å")
print(f"a    = {a:.4f} Å")
print(f"c    = {c:.4f} Å")

# Check predicted d101 from calculated a,c
inv_d101_sq = (4.0 / 3.0) / (a * a) + 1.0 / (c * c)
predicted_d101 = 1.0 / math.sqrt(inv_d101_sq)

print(f"predicted d101 = {predicted_d101:.4f} Å")
print(f"observed  d101 = {d101:.4f} Å")
