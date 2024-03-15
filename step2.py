#######################################################################
#
#  step1.py
#
#  Part of the task to reset and resubmit McM requests.
#
#  author: Samadhan Kamble (samadhan.kamble@cern.ch)
#
#  The step 1 performs: 
#   1) identify the chained request
#   2) un-check the flag in the chained request
#   3) rewind the chained request to root
#   4) reset and delete all daughter requests (except root)
#   5) reserve the same chain again
#
#  The step 2 (step2.py) performs:
#   6) check back the flag in chained request
#
#   Finally one can soft reset and resubmit corresponding root requests
#
########################################################################


import sys
import argparse
sys.path.append("/afs/cern.ch/cms/PPD/PdmV/tools/McM/")
from rest import McM


parser = argparse.ArgumentParser(
    description="revalidation: flag=True")
parser.add_argument("--chained_requests", type=str, nargs="+", default=None)
parser.add_argument("--root_requests", type=str, nargs="+", default=None)
parser.add_argument("--dry", default=False, action="store_true")

args = parser.parse_args()
dry = args.dry
chained_requests = args.chained_requests
root_requests = args.root_requests

# making sure user input is meaningful
assert not (chained_requests is None and root_requests is None)
if chained_requests is None:
    assert root_requests is not None
if root_requests is None:
    assert chained_requests is not None

mcm = McM(dev=dry)

# in case that root_requests are provided, identify their chained requests
chained_requests = []
for request in root_requests:
    mcm_request = mcm.get("requests", object_id=request)
    chains = mcm_request["member_of_chain"]
#    if len(chains) != 1:
#        print(f"The following root request is member of {len(chains)}"
#              f" chains instead of 1: {request}")
#        input("Press enter to skip it or abort with Ctrl+C")
#        continue
    chained_requests.append(chains[0])

print("\nChained requests that will be reseted:")
for chained_request in chained_requests:
    print(f"\t{chained_request}")

# operate each chained request
for chained_request in chained_requests:
    print("\nOperating chained request:", chained_request)
    mcm_chained_request = mcm.get(
        "chained_requests", object_id=chained_request)
    if mcm_chained_request is None:
        print(f"Warning: Chained request doesn't exist!!")
        input("Press enter to skip it or abort with Ctrl+C")
        continue
    steps = mcm.steps_from_chained_request(chained_request)

    print("\tre-validating chained request...")
 #   mcm_chained_request["action_parameters"]["flag"] = False
 #   update_answer = mcm.update("chained_requests", mcm_chained_request)

    mcm_chained_request["action_parameters"]["flag"] = True
    update_answer = mcm.update("chained_requests", mcm_chained_request)

