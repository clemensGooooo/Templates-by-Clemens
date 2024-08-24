from pathlib import Path
import re
import json
import sys
import os

# Usage: Add the path to the auth.log/secure log as an argument to the script
# Ex. parser.py auth.log

date_pattern = r'\b[A-Z][a-z]{2}\s{1,2}\d{1,2}\s\d{2}:\d{2}:\d{2}\b'

log_patterns = {
    "command_execution": r'PWD=(?P<PWD>\S+); USER=(?P<USER>\S+); COMMAND=(?P<COMMAND>\S+)',
    "pam_unix": r'pam_unix\(\S+:(?P<session_type>\S+)\): (?P<session_status>\S+) (?P<session_action>\S+) for user (?P<user>[\S\s]+)',
    "server_listening": r'Server listening on (?P<address>\S+) port (?P<port>\d+)',
    "received_signal": r'Received signal (?P<signal>\d+); terminating.',
    "accepted_publickey": r'Accepted publickey for (?P<user>\S+) from (?P<src_ip>\S+) port (?P<port>\d+) ssh2: (?P<auth_method>\S+) (?P<key_fingerprint>\S+)',
    "connection_closed": r'Connection closed by (authenticating user (?P<user>\S+) )?(?P<src_ip>\S+) port (?P<port>\d+)( \[preauth\])?',
    "group_added": r'(group added to (?P<group_file>\S+): name=(?P<group_name>\S+)|new group: name=(?P<group>\S+))(, GID=(?P<GID>\d+))?',
    "new_user": r'new user: name=(?P<user_name>\S+), UID=(?P<user_id>\S+), GID=(?P<group_id>\S+), home=(?P<home_dir>\S+), shell=(?P<shell>\S+) from=none',
    "disconnected": r'Disconnected from( invalid)?( user (?P<user>\S+))? (?P<src_ip>\S+) port (?P<port>\d+)( \[preauth\])?',
    "invalid_user": r'Invalid user( (?P<user>\S+))? from (?P<src_ip>\S+) port (?P<port>\d+)',
    "protocol_error": r'error: (?P<error_type>\S+): type (?P<type>\d+) seq (?P<seq>\d+) \[preauth\]',
    "disconnecting_user": r'Disconnecting authenticating user (?P<user>\S+) (?P<src_ip>\S+) port (?P<port>\d+): Too many authentication failures \[preauth\]',
    "banner_exchange": r'banner exchange: Connection from (?P<src_ip>\S+) port (?P<port>\d+): (?P<error_msg>\S+) (?P<error_detail>\S+)',
    "negotiate_error": r'Unable to negotiate with (?P<src_ip>\S+) port (?P<port>\d+): (?P<error_msg>.+)',
    "dispatch_protocol_error": r'dispatch_protocol_error: type (?P<type>\d+) seq (?P<seq>\d+) \[preauth\]',
    "userauth_pubkey": r'userauth_pubkey: key type (?P<key_type>\S+) not in PubkeyAcceptedAlgorithms \[preauth\]',
    "fatal_error": r'fatal: userauth_pubkey: parse packet: (?P<error_msg>\S+) (?P<error_detail>\S+) \[preauth\]',
    "drop_connection": r'drop connection #(?P<connection_id>\d+) from \[(?P<src_ip>\S+)\]:\d+ on \[(?P<dest_ip>\S+)\]:\d+ past MaxStartups',
    "exited_maxstartups": r'exited MaxStartups throttling after \S+, (?P<connections_dropped>\d+) connections dropped',
    "received_disconnect": r'Received disconnect from (?P<src_ip>\S+) port (?P<port>\d+):(?P<message>.+)( disconnected by user)?( \[preauth\])?',
    "disconnected_from_auth_user": r'Disconnected from authenticating user (?P<user>\S+) (?P<src_ip>\S+) port (?P<port>\d+) \[preauth\]',
    "connection_user": r'Connection (?P<type_of_connection>\S+) by (?P<reason>\S+) user( )?(?P<user>\S+)? (?P<src_ip>\S+) port (?P<port>\d+)( \[preauth\])?',
    "kex_exchange_identification": r'error: kex_exchange_identification: client sent invalid protocol identifier (?P<data_send>[\s\S]*)',
    "key_exchange_error": r'error: kex_exchange_identification: (?P<key_exchange_error>[\s\S]*)',
    "connection_reset": r'Connection reset by( invalid user (?P<user>\S+))? (?P<src_ip>\S+) port (?P<port>\d+)( \[preauth\])?',
    "max_password_attempts": r'(Disconnecting invalid|error: maximum authentication attempts exceeded for) user (?P<user>\S+) (?P<src_ip>\S+) port (?P<port>\d+)(: Too many authentication failures| ssh2)( \[preauth])?',
    "error": r'error: (?P<error>[\s\S]*)',
    "command_sudo": r'(?P<user_main>\S+) : (TTY=(?P<shell>\S+) ; )?PWD=(?P<PWD>\S+) ; USER=(?P<user>\S+) ; COMMAND=(?P<command>[\S\s]*)',
    "bad_packet": r'Bad packet (?P<error>[\s\S]*)( [preauth])?',
    "other": r'(?P<line>[\s\S]*)',
}

def parse_log_entry(log_entry,date,host,service,pid):
    log_object = {}
    
    log_str = ' '.join(log_entry)
    
    for key, pattern in log_patterns.items():
        match = re.search(pattern, log_str)
        if match:
            log_object["type"] = key
            log_object.update(match.groupdict())
            break
    log_object["date"] = date
    log_object["host"] = host
    log_object["service"] = service
    log_object["pid"] = pid

    return log_object

def process_lines(line):
    date = re.findall(date_pattern, line)[0]
    line_splitted = re.split(r'\s+', line)
    host = line_splitted[3]
    service_info = line_splitted[4].split("[")
    service = service_info[0]
    pid = service_info[1].split("]")[0]
    message = line_splitted[5:-1]
    parsed_log_entry = parse_log_entry(message,date,host,service,pid)
    if parsed_log_entry:
        return parsed_log_entry
    else:
        return

def main():
    try:
        log_path = Path(sys.argv[1])
        json_path = Path(sys.argv[2])
    except IndexError:
        print("Please add a log file!")
        exit(0)
    
    if not log_path.exists():
        exit(0)
    
    log_file = open(log_path)
    log_lines = log_file.readlines()
    output = []

    for line in log_lines:
        output.append(process_lines(line))

    print("Lines totally parsed: ",end="")
    print(len(output))
    print("Lines not parsed: ",end="")
    print(len(log_lines) - len(output))

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
