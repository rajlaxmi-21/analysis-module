import os
import math
import glob
import shutil
import subprocess
from datetime import datetime, timedelta


BASE_OUTPUT = "/home/ubuntu/results"
S2_OUTPUT = "/home/ubuntu/s2dr3/output"


def build_bbox(lat, lon, side_km=2):
    """
    2 km x 2 km square = 4 km²
    Returns W S E N
    """
    half_lat = (side_km / 2) / 111.0
    half_lon = (side_km / 2) / (111.0 * math.cos(math.radians(lat)))

    west = lon - half_lon
    east = lon + half_lon
    south = lat - half_lat
    north = lat + half_lat

    return west, south, east, north


def clear_old_outputs():
    os.makedirs(BASE_OUTPUT, exist_ok=True)
    os.system(f"rm -rf {S2_OUTPUT}/*")
    os.system(f"rm -rf {BASE_OUTPUT}/*")


def find_latest_ms_file():
    files = glob.glob(f"{S2_OUTPUT}/**/*_MS.tif", recursive=True)
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def run_s2dr3(lat, lon, target_date, save_name):
    w, s, e, n = build_bbox(lat, lon, side_km=2)

    cmd = [
        "python3",
        "infer.py",
        "-f",
        "--max_clouds", "0",
        "--date", target_date,
        "--aoi",
        str(w), str(s), str(e), str(n)
    ]

    print("Running:", " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)

    if result.returncode != 0:
        raise Exception("S2DR3 failed")

    ms_file = find_latest_ms_file()

    if ms_file is None:
        raise Exception("No MS file generated")

    final_path = os.path.join(BASE_OUTPUT, save_name)
    shutil.copy2(ms_file, final_path)

    return final_path


def get_images(lat, lon):
    clear_old_outputs()

    today = datetime.today().date()
    prev_day = today - timedelta(days=7)

    current_date = today.strftime("%Y-%m-%d")
    previous_date = prev_day.strftime("%Y-%m-%d")

    current_file = run_s2dr3(lat, lon, current_date, "current.tif")
    previous_file = run_s2dr3(lat, lon, previous_date, "previous.tif")

    return {
        "current": current_file,
        "previous": previous_file,
        "requested_current_date": current_date,
        "requested_previous_date": previous_date
    }


if __name__ == "__main__":
    # Example test
    result = get_images(18.5204, 73.8567)
    print(result)