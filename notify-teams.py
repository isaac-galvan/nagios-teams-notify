#!/usr/bin/env python3 
#
#
# Author: Isaac J. Galvan
# Date: 2018-12-04
#
# https://github.com/isaac-galvan
#

import argparse
import json
import requests
import sys

def create_message(url, subject, output, long_message=None):
    ''' creates a dict with for the MessageCard '''
    message = {}

    message['summary'] = subject
    message['title'] = subject
    message['text'] = output

    # if not long_message is None:
    if long_message:
        message['text'] += '\n\n' + long_message

    message['@type'] = 'MessageCard'
    message['@context'] = 'https://schema.org/extensions'

    return message

def send_to_teams(url, message_json):
    """ posts the message to the ms teams webhook url """
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=message_json, headers=headers)
    if r.status_code == requests.codes.ok:
        print('success')
        return True
    else:
        print('failure')
        return False

def main(args):

    # verify url
    url = args.get('url')
    if url is None:
        # error no url
        print('error no url')
        exit(2)

    subject = args.get('subject')
    output = args.get('output')
    long_message = args.get('long_message')
    
    message_dict = create_message(url, subject, output, long_message)
    message_json = json.dumps(message_dict)
    
    send_to_teams(url, message_json)

if __name__=='__main__':
    args = {}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('subject', action='store', help='message subject')
    parser.add_argument('output', action='store', help='output of the check')
    parser.add_argument('url', action='store', help='teams connector webhook url')

    parsedArgs = parser.parse_args()

    args['subject'] = parsedArgs.subject
    args['url'] = parsedArgs.url
    args['output'] = parsedArgs.output

    if not sys.__stdin__.isatty():
        args['long_message'] = sys.__stdin__.read()
        pass
    
    main(args)