#!/usr/bin/python3 -W ignore::DeprecationWarning

import json
import requests
import time
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
move this to apifunction lib in future
"""
def login_api(key, mds, domain):
    payload = {"api-key" : key, "domain" : domain}
    response = apifunctions.api_call(mds, "login", payload, "")

    return response["sid"]
#end of api

def get_cluster_names(mds, sid):
    #show simple-clusters limit 5 --format json | jq '.objects[] | .name'
    debug = 1
    cluster_names = list()

    show_simple_cluster_json = {
        "limit" : 5
    }

    show_simple_cluster_result = apifunctions.api_call(mds, "show-simple-clusters", show_simple_cluster_json, sid)

    print(json.dumps(show_simple_cluster_result))

    for x in range(show_simple_cluster_result['total']):
        cluster_names.append(show_simple_cluster_result['objects'][x]['name'])

    return(cluster_names)
#end of get_cluster_names

def get_spoof_from_name(mds, sid, cluster_name):
    #show simple-cluster name ALBA122 --format json | jq '."interfaces" | .objects[] | ."topology-settings"'
    debug = 0
    
    show_simple_cluster_json = {
        "name" : cluster_name
    }

    show_simple_cluster_result = apifunctions.api_call(mds, "show-simple-cluster", show_simple_cluster_json, sid)

    if(debug == 1):
        print(json.dumps(show_simple_cluster_result))

    for x in range(show_simple_cluster_result['interfaces']['total']):
        print(show_simple_cluster_result['interfaces']['objects'][x])
        
        print("\n")
        print(show_simple_cluster_result['interfaces']['objects'][x]['name'])
        print(show_simple_cluster_result['interfaces']['objects'][x]['interface-type'])

        if(show_simple_cluster_result['interfaces']['objects'][x]['interface-type'] == "cluster" or show_simple_cluster_result['interfaces']['objects'][x]['interface-type'] == "cluster + sync"):
            print("HIT")
            print("\U0001F603")

            try:
                print(show_simple_cluster_result['interfaces']['objects'][x]['interface-type'])
                print(show_simple_cluster_result['interfaces']['objects'][x]['topology-settings']['specific-network'])
            except:
                print("settings")

def main():
    print("Start")
    debug = 1
    mds = "146.18.96.16"
    cma = "146.18.96.28"

    clusters = list()

    key = {}
    with open('apirw-key.json', 'r') as f:
        key = json.load(f)

        if(debug == 1):
            print(key['api-key'])
    
    #sid = login_api(key['api-key'], mds, cma)
    sid = apifunctions.login("gdunlap", "1qazxsw2", mds, cma)

    if(debug == 1):
        print("login sid : " + sid)
    
    clusters = get_cluster_names(mds, sid)

    if(debug == 1):
        print("*" *20)
        print(clusters)
    
    for cluster in clusters:
        get_spoof_from_name(mds, sid, cluster)

    time.sleep(20)
    logout_result = apifunctions.api_call(mds, "logout", {}, sid)
    print("logout results : " + json.dumps(logout_result))
#end of main

if __name__ == "__main__":
    main()
#end of program