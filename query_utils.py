import requests
import json
import time
import urllib3

##CONNEXTION A L'API

#Intégration --> mathis-integration.rte-france.com
#Privé / Public --> mathis.rte-france.com
SERVER_HOST_ADDR = "mathis.rte-france.com"
USE_SSL_VERIFICATION = False

#disable security warning (dw it's safe)
urllib3.disable_warnings()


def get_headers(nni, mdp):
    AUTH_DATA = {"userName": f"{nni}", "password": f"{mdp}"}
    r = requests.post("https://" + SERVER_HOST_ADDR + "/apiv2/login", data=json.dumps(AUTH_DATA),verify=USE_SSL_VERIFICATION, headers={"content-type": "application/json"})
    status_code = r.status_code
    status_code_response = (0,"")
    if status_code != 200:
        print("##### Erreur de connection à l'API #####")
        headers = None
        if status_code in [401, 403, 404]:
            status_code_response = (status_code, f'{status_code} --> {r.reason}')
        else:
            status_code_response = (000, 'Erreur inconnue')
    else :
        print("##### Connexion Success #####")
        TOKEN = r.json()["token"]
        headers = {'content-type': 'application/json', 'Authorization': '_dremio{authToken}'.format(authToken=TOKEN)}
    print(headers)
    return [headers, status_code_response]


def make_query(query, headers):
    print(query, headers)
    payload = {"sql": f"{query}"}
    r = requests.post("https://" + SERVER_HOST_ADDR + "/api/v3/sql", data=json.dumps(payload), verify=USE_SSL_VERIFICATION, headers=headers)
    jobId = r.json()["id"]
    r = requests.get("https://" + SERVER_HOST_ADDR + "/api/v3/job/" + jobId, verify=USE_SSL_VERIFICATION, headers=headers)

    while r.json()["jobState"] == "RUNNING":
        time.sleep(0.4)  # reduce here later to make it look faster but not too much it might break it
        print("Querying server for job status")
        r = requests.get("https://" + SERVER_HOST_ADDR + "/api/v3/job/" + jobId, verify=USE_SSL_VERIFICATION, headers=headers)
    print("Job has been processed, trying to get the result")
    while r.json()["jobState"] != "COMPLETED" and r.json()["jobState"] != "FAILED" and r.json()["jobState"] != "CANCELED":
        r = requests.get("https://" + SERVER_HOST_ADDR + "/api/v3/job/" + jobId, verify=USE_SSL_VERIFICATION, headers=headers)
        print(r.json()["jobState"])
        time.sleep(0.4)  # reduce here later to make it look faster but not too much it might break it

    # loop si jamais il y a plus de 500 résultat dans la requetes
    if r.json()["jobState"] == "COMPLETED":
        print("Accessing job result")
        offset = 0
        limit = 500
        results = []
        while True:
            r = requests.get(f"https://{SERVER_HOST_ADDR}/api/v3/job/{jobId}/results?limit={limit}&offset={offset}", verify=USE_SSL_VERIFICATION, headers=headers)
            data = r.json()
            results.extend(data["rows"])
            if len(data["rows"]) < limit:
                break
            offset += limit
        print(results)
    else:
        print("Failed to get job result due to an invalid state: ")
        results = None

    return results
