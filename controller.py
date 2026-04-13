import sys
import subprocess

KEY = "/Users/rajlaxmiawatade/Downloads/s2dr3-keypair.pem"
HOST = "ubuntu@3.17.203.36"   # replace with current IP


def run_remote(lat, lon):
    remote_cmd = (
        f'cd ~ && '
        f'source ~/s2env/bin/activate && '
        f'python3 -c "from fetch import get_images; get_images({lat}, {lon})"'
    )

    cmd = ["ssh", "-i", KEY, HOST, remote_cmd]
    subprocess.run(cmd, check=True)


def download_files():
    for name in ["current.tif", "previous.tif"]:
        cmd = [
            "scp",
            "-i", KEY,
            f"{HOST}:/home/ubuntu/results/{name}",
            "/Users/rajlaxmiawatade/Desktop/sdk-s2dr3"
        ]
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 controller.py <lat> <lon>")
        sys.exit(1)

    lat = float(sys.argv[1])
    lon = float(sys.argv[2])

    run_remote(lat, lon)
    download_files()

    print("Done.")