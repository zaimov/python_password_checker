import requests
import hashlib
import sys

def request_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

def check_password_against_the_api(hashes, hash_to_check):  
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf8')).hexdigest().upper()
    first_five_characters, tail = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first_five_characters)

    return check_password_against_the_api(response, tail)

def main(args):
    for password in args:
        count = api_check(password)
        if count:
            print(f'{password} was found {count} times. You should change your password')
        else:
            print('You are safe.')
    return 'Done.'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))