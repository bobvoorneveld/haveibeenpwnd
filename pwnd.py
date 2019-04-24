import csv
import hashlib
import sys
import urllib.parse

import requests

headers = {
    'User-Agent': 'Bobs test'
}


def pwned(password):

    sha_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    response = requests.get(f'https://api.pwnedpasswords.com/range/{sha_password[:5]}',
                            headers=headers)

    count = 0
    for row in response.text.splitlines():
        if sha_password[5:] in row:
            count = row.split(':')[1]
            break
    return count


def breached_account(account):
    account = urllib.parse.quote(account)
    response = requests.get(f'https://haveibeenpwned.com/api/v2/breachedaccount/{account}',
                            headers=headers)

    if not response.ok:
        return False
    return response.json()


def paste_account(account):
    account = urllib.parse.quote(account)
    response = requests.get(f'https://haveibeenpwned.com/api/v2/pasteaccount/{account}',
                            headers=headers)

    if not response.ok:
        return False

    return [(r['Id'], r['Title']) for r in response.json()]


def csv_check(file_name):
    with open(file_name, 'r') as csvfile:
        spamreader = csv.reader(csvfile, quotechar='"')
        for row in spamreader:
            if row[-1]:
                count = pwned(row[-1])
                if count:
                    print(count, row)


if __name__ == '__main__':
    method = sys.argv[1]
    if method == 'password':
        print(pwned(sys.argv[2]))
    elif method == 'breach':
        print(breached_account(sys.argv[2]))
    elif method == 'paste':
        print(paste_account(sys.argv[2]))
    elif method == 'csv':
        print(csv_check(sys.argv[2]))
    else:
        raise Exception('Wrong argument')
