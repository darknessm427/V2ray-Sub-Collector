import pybase64
import base64 
import requests
import binascii
import os

TIMEOUT = 20  # seconds

fixed_text = """#profile-title: base64:w5DOm8mM4oKt4ZGOzp7wkJKh8JCSoXzwk4SC8JOGgw==
#profile-update-interval: 1
#subscription-userinfo: upload=20; download=20; total=10737418240000000; expire=2546249531
#profile-web-page-url: https://github.com/mansor427
"""


# Base64 decoding function
def decode_base64(encoded):
    decoded = ""
    for encoding in ["utf-8", "iso-8859-1"]:
        try:
            decoded = pybase64.b64decode(encoded + b"=" * (-len(encoded) % 4)).decode(encoding)
            break
        except (UnicodeDecodeError, binascii.Error):
            pass
    return decoded

# Function to decode base64-encoded links with a timeout
def decode_links(links):
    decoded_data = []
    for link in links:
        try:
            response = requests.get(link, timeout=TIMEOUT)
            encoded_bytes = response.content
            decoded_text = decode_base64(encoded_bytes)
            decoded_data.append(decoded_text)
        except requests.RequestException:
            pass  # If the request fails or times out, skip it
    return decoded_data

# Function to decode directory links with a timeout
def decode_dir_links(dir_links):
    decoded_dir_links = []
    for link in dir_links:
        try:
            response = requests.get(link, timeout=TIMEOUT)
            decoded_text = response.text
            decoded_dir_links.append(decoded_text)
        except requests.RequestException:
            pass  # If the request fails or times out, skip it
    return decoded_dir_links

# Filter function to select lines based on specified protocols
def filter_for_protocols(data, protocols):
    filtered_data = []
    for line in data:
        if any(protocol in line for protocol in protocols):
            filtered_data.append(line)
    return filtered_data

# Create necessary directories if they don't exist
def ensure_directories_exist():
    output_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))
    base64_folder = os.path.join(output_folder, "Base64")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(base64_folder):
        os.makedirs(base64_folder)

    return output_folder, base64_folder

# Main function to process links and write output files
def main():
    output_folder, base64_folder = ensure_directories_exist()  # Ensure directories are created

    protocols = ["vmess", "vless", "trojan", "ss", "ssr", "hy2", "tuic", "warp://"]
    links = [
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/hysteria",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/tuic",
        "https://raw.githubusercontent.com/AzadNetCH/Clash/main/V2Ray.txt",
        "https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/ssr",
        "https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/tr",
    ]
    dir_links = [
        "https://api.yebekhe.link/shervin/",
        "https://raw.githubusercontent.com/NiREvil/vless/main/sub/G-Core",
        "https://raw.githubusercontent.com/NiREvil/vless/main/sub/SSTime",
        "https://raw.githubusercontent.com/coldwater-10/V2rayCollector/main/vmess_iran.txt",
        "https://raw.githubusercontent.com/amirmohammad-mohammad-88/Sub-Reality-Azadi-config/Config/Azadi-Reality-Different",
        "https://raw.githubusercontent.com/amirmohammad-mohammad-88/Sub-Reality-Azadi-config/Config/Config",
        "https://raw.githubusercontent.com/amirmohammad-mohammad-88/Sub-Config-operator/Config/MCI.txt",
        "https://raw.githubusercontent.com/amirmohammad-mohammad-88/Sub-Config-operator/Config/Mobinet.txt",
        "https://raw.githubusercontent.com/amirmohammad-mohammad-88/Sub-Config-operator/Config/Mokhabrat.txt",
        "https://raw.githubusercontent.com/amirmohammad-mohammad-88/Sub-Config-operator/Config/Rightel.txt",
        "https://raw.githubusercontent.com/amirmohammad-mohammad-88/Sub-Config-operator/Config/irancell.txt",
        "https://raw.githubusercontent.com/amirmohammad-mohammad-88/Sub-Config-operator/Config/shatel.txt",
        "https://raw.githubusercontent.com/amirmohammad-mohammad-88/Sub-Config-operator/Config/various",
    ]

    decoded_links = decode_links(links)
    decoded_dir_links = decode_dir_links(dir_links)

    combined_data = decoded_links + decoded_dir_links
    merged_configs = filter_for_protocols(combined_data, protocols)


    # Delete existing output files
    output_filename = os.path.join(output_folder, "All_Darkness_Sub.txt")
    filename1 = os.path.join(output_folder, "All_Darkness_base64_Sub.txt")
    
    if os.path.exists(output_filename):
        os.remove(output_filename)
    if os.path.exists(filename1):
        os.remove(filename1)

    for i in range(20):
        filename = os.path.join(output_folder, f"Darkness Sub{i}.txt")
        if os.path.exists(filename):
            os.remove(filename)
        filename1 = os.path.join(base64_folder, f"Darkness Sub{i}_base64.txt")
        if os.path.exists(filename1):
            os.remove(filename1)
    
    # Write merged configs to output file
    with open(output_filename, "w") as f:
        f.write(fixed_text)
        for config in merged_configs:
            f.write(config + "\n")

    # Split merged configs into smaller files (no more than 600 configs per file)
    with open(output_filename, "r") as f:
        lines = f.readlines()

    num_lines = len(lines)
    max_lines_per_file = 700
    num_files = (num_lines + max_lines_per_file - 1) // max_lines_per_file

    for i in range(num_files):
        profile_title = f"ÐΛɌ₭ᑎΞ𐒡𐒡|𓄂𓆃"
        encoded_title = base64.b64encode(profile_title.encode()).decode()
        custom_fixed_text = f"""#profile-title: base64:{encoded_title}
#profile-update-interval: 1
#subscription-userinfo: upload=20; download=20; total=10737418240000000; expire=2546249531
#profile-web-page-url: https://github.com/darkness427
"""

        input_filename = os.path.join(output_folder, f"Darkness Sub{i + 1}.txt")
        with open(input_filename, "w") as f:
            f.write(custom_fixed_text)
            start_index = i * max_lines_per_file
            end_index = min((i + 1) * max_lines_per_file, num_lines)
            for line in lines[start_index:end_index]:
                f.write(line)

        with open(input_filename, "r") as input_file:
            config_data = input_file.read()
        
        output_filename = os.path.join(base64_folder, f"Darkness Sub{i + 1}_base64.txt")
        with open(output_filename, "w") as output_file:
            encoded_config = base64.b64encode(config_data.encode()).decode()
            output_file.write(encoded_config)

if __name__ == "__main__":
    main()
