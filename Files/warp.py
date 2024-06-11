import pybase64
import base64
import requests
import binascii
import os

warp_fixed_text = """#profile-title: base64:w5DOm8mM4oKt4ZGOzp7wkJKh8JCSoXzwk4SC8JOGg3x3YXJw
#profile-update-interval: 1
#subscription-userinfo: upload=29; download=12; total=10737418240000000; expire=2546249531
#profile-web: https://github.com/darkness427


"""

def decode_base64(encoded):
    decoded = ''
    for encoding in ['utf-8', 'iso-8859-1']:
        try:
            decoded = pybase64.b64decode(encoded + b'=' * (-len(encoded) % 4)).decode(encoding)
            break
        except (UnicodeDecodeError, binascii.Error):
            pass
    return decoded

def fetch_and_process_links(links):
    warp_lines = []
    for link in links:
        response = requests.get(link)
        content = response.text
        for line in content.splitlines():
            if "warp://" in line:
                warp_lines.append(line)
    return warp_lines

def main():
    warp_links = [
        'https://raw.githubusercontent.com/mansor427/Warp-Autosub/main/subwarp/warp',
        'https://raw.githubusercontent.com/mansor427/Warpauto/main/warp.json',
        'https://raw.githubusercontent.com/NiREvil/vless/main/hiddify/auto-gen-warp'
    ]
    # Process the links and filter out warp lines
    decoded_warp_lines = fetch_and_process_links(warp_links)
    merged_configs = '\n'.join(decoded_warp_lines)

    # Define the directory to save your files
    output_folder = os.path.abspath(os.path.join(os.getcwd(), '..'))
    os.makedirs(output_folder, exist_ok=True)

    # Writing the fixed text and merged warp lines to an output file
    warp_output_file = os.path.join(output_folder, 'Warp_sub.txt')
    with open(warp_output_file, 'w') as f:
        f.write(warp_fixed_text + merged_configs)

if __name__ == "__main__":
    main()
