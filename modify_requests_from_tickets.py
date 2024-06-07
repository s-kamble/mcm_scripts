import sys
import argparse
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM

mcm = McM(dev=False)

parser = argparse.ArgumentParser(description='Change priority in McM')
parser.add_argument('--ticket', type=str)

args = parser.parse_args()
#debug = args.debug
#dry = args.dry
#if debug:
#    print('Args: %s' % (args))
    
requests = []
if args.ticket:
    ticket_prepids = args.ticket.split(',')
    for ticket_prepid in ticket_prepids:
        requests_in_ticket = mcm.root_requests_from_ticket(ticket_prepid)
        requests.extend(requests_in_ticket)

for request in requests:

    request['tags'] = ['PC_Jun5_2024']

    update_response = mcm.update('requests', request)

    print('Update response: %s' % (update_response))

