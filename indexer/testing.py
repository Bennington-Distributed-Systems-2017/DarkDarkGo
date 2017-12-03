#!/usr/bin/env python3
"""
    testing.py - Automated test tool for REST endpoints
    Author: Dung Le (dungle@bennington.edu)
    Date: 12/02/2017
"""

import requests
import json
from index_builder_final import Index_Builder

mgmt_ip_addr = '10.2.16.57'
crawler_ip_addr = '10.2.25.143'

# Test Endpoint 1: Update online status to Mgmt
online = requests.post('http://{0}:5000/set_component_state'.format(mgmt_ip_addr), json={"state": "online"})
print(online.json())

# Test Endpoint 2: Get content chunk metadata from Mgmt
metadata = requests.get('http://{0}:5000/get_content_chunk_metadata'.format(mgmt_ip_addr))
print(metadata.json())

chunk_ids = []
for item in metadata.json():
    chunk_id = item['chunk_id']
    chunk_ids.append(chunk_id)

print(chunk_ids)

# Test Endpoint 3: Get content chunk from Crawler
for id_ in chunk_ids:
    content_chunk = requests.get('http://{0}:5000/get_chunk/{1}'.format(crawler_ip_addr, id_))
    print(content_chunk.json())

    # Save the content chunk from Crawler into local json files
    with open('/sample_files/content_files/{0}.json'.format(id_), 'w') as content_file:
        json.dump(content_chunk.json(), content_file)
    content_file.close()

    # Call class Index_Builder to build index chunk
    indexer = Index_Builder(id_, '{0}.json'.format(id_))
    indexer.run()

    # Test Endpoint 4: Update status of index chunk to Mgmt
    data = {"chunk_id": id_, "state": "built"}
    index_chunk_metadata = requests.post('http://{0}:5000/set_index_chunk_metadata'.format(mgmt_ip_addr), json=data)
    print(index_chunk_metadata.json())
