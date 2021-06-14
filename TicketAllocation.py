import requests
import json
import random

# This job will check for new tickets in Zendesk support, and auto assign it randomly to agents and send the requester a 1st responce email.

# pwd is api key, generated in the API dashboard
user = 'user@domain.com/token'
pwd = ''

# List of active agents
agents = ['AgentOneReference', 'AgentTwoReference', 'AgentThreeReference', 'AgentFourReference']

url = 'https://{{Domain}}.zendesk.com/api/v2/search.json?query=type%3Aticket+status%3Anew'

# 1. Finding "new" tickets on the service desk.
response = requests.get(url, auth=(user, pwd))

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Problem with the request. Exiting.')
    exit()

data = response.json()

# 2. Update the found ticket, by changing the assignee ID (agent) from NULL to an agent.
tickets = data['results']
if (len(tickets) != 0):  # check if there is actual 'New' tickets in array
    for ticket in tickets:
        # print(ticket['subject'] + " ID: " + str(ticket['id']))
        id = ticket['id']
        agent = random.choice(agents)
        # print(str(id) + ' ' + agent)
        payload = {"ticket": {
            "comment": {
                "body": 'Hello {{ticket.requester.first_name}}, \n\nThank you for contacting {{Org}} Support. \n\nThis has been raised with reference {{ticket.id}}. \n\n Many thanks, \n{{ticket.assignee.first_name}}',
            },
            "author_id": agent,
            "assignee_id": agent}}
        assignrequest = requests.put('https://electio.zendesk.com/api/v2/tickets/' + str(id) + '.json',
                                     data=json.dumps(payload), auth=(user, pwd),
                                     headers={"Content-Type": "application/json"})


        if assignrequest.status_code != 200:
            print('Status:', response.status_code, 'Problem with the request. Exiting.')
            exit()
        data2 = assignrequest.json()
        print(data2)

else:
    print("No tickets")
