
# OpenVPN Spray

A simple utility for password spray against OpenVPN access server.

## Requirements

- Python 3.x

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/nm10pt/OpenVPNSpray.git
   ```

2. **Navigate to the directory:**

   ```sh
   cd OpenVPNSpray
   ```

3. **Create and activate a virtual environment:**

   On macOS/Linux:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```

4. **Install the required Python libraries using `requirements.txt`:**

   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```sh
python openvpn_spray.py -t <host> [--target-port <port>] -u <users_file> -p <password> [-o <output_file>]
```

### Arguments

- `-t`, `--target` (required): The target host (IP or hostname).
- `--target-port` (optional): The target port.
- `-u`, `--users-file` (required): A file containing a list of usernames (one username per line).
- `-p`, `--password` (required): The password to attempt for each user.
- `-o`, `--outfile` (optional): Path to an output file where the results will be stored.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
