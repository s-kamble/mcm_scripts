import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps

mcm = McM(dev=True)

# Script clones a request to other campaign.
# Fefine list of modifications
# If member_of_campaign is different, it will clone to other campaign
modifications = {'extension': 1,
                 'total_events': 101,
                 'member_of_campaign': 'Summer12'}

mod = {'Tags': 'test'}

request_prepid_to_clone = "B2G-Fall13-00001"

# Get a request object which we want to clone
request = mcm.get('requests', request_prepid_to_clone)

# Make predefined modifications
for key in mod:
    request[key] = mod[key]

#clone_answer = mcm.clone_request(request)
#if clone_answer.get('results'):
#    print('Clone PrepID: %s' % (clone_answer['prepid']))
#else:
#    print('Something went wrong while cloning a request. %s' % (dumps(clone_answer)))
