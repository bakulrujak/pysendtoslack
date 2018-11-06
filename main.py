from utils.config import slack
import json
import requests

def main_handler(event, context):

	deployment_state  = event['detail']['state']       
	deployment_id     = event['detail']['deploymentId']
	deployment_group  = event['detail']['deploymentGroup']

	print(event)
	codedeploy_result_handler(deployment_state, deployment_id, deployment_group)
	
def codedeploy_result_handler(deployment_state, deployment_id, deployment_group):    
	
	color = "#00FF00"
	env_stage = "dev"
	slack_webhook = slack.slack_webhook

	## Informations -- Codedeploy ##
	if not deployment_state == 'SUCCESS':
		color     = "#E53935"
		deployment_state = 'FAILED'

	codedeploy_uri  = "https://ap-southeast-1.console.aws.amazon.com/codedeploy/home?region=ap-southeast-1#/deployments/" + deployment_id

	payload           = {
						  "attachments": [
							  {
								  "color": color,
								  "pretext": "Your deployment summary:",
								  "title": "Your deployment for `" + env_stage + "` was " + deployment_state + "!",
								  "text": "Build ID: <" + codedeploy_uri + "|" + deployment_id + ">",
								  "mrkdwn_in": ["text", "title"]
							  }
						  ]
					  }

	## Send to Slack now! ##
	do_send_slack(slack_webhook, payload)                  

def do_send_slack(webhook, payload):

	headers = {'Content-Type': 'application/json'}
	r = requests.post(
			webhook,
			data=json.dumps(payload),
			headers=headers
	)

	try:
		return r.text
	except:
		return 'Unable to reach Slack.'	