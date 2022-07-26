#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import json
from prance import ResolvingParser

parser = ResolvingParser('/Users/zeevshteiman/dev/event_schema/models/localize/event_api.yaml')
with open('/Users/zeevshteiman/dev/event_schema/schema.json', 'w') as outfile:
    json.dump(parser.specification, outfile, indent = 4)
