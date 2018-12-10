# nagios-teams-notify
Send Nagios alerts to a Microsoft Teams channel

## Overview

This script can send Nagios alerts to a Microsoft Teams channel.

By sending alerts to Teams, we can simplify addition and removal alert recipients, allow for self-service subscription and push preferences, and have conversations based around the alerts as they occur.

## Installation

Install dependancies from requirements.txt and place `notify-teams.py` where it can be executed by the Nagios user.

## Configuration

### Create the Webhook

From [Using Office 365 Connectors: Teams](https://docs.microsoft.com/en-us/microsoftteams/platform/concepts/connectors/connectors-using#setting-up-a-custom-incoming-webhook):

1. In Microsoft Teams, choose More options (⋯) next to the channel name and then choose Connectors.
2. Scroll through the list of Connectors to Incoming Webhook, and choose Add.
3. Enter a name for the webhook, upload an image to associate with data from the webhook, and choose Create.
4. Copy the webhook to the clipboard and save it. You'll need the webhook URL for sending information to Microsoft Teams.
5. Choose Done.

### Configure Nagios

Create a command object in the Nagios configuration.

```
define command {
    command_name notify_teams
    command_line /usr/bin/printf "$LONGSERVICEOUTPUT$" | /path/to/script/notify-teams.py  "$NOTIFICATIONTYPE$: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$" "$SERVICEOUTPUT$" $_CONTACTWEBHOOKURL$
}
```
Create a contact object with the custom variable macro _WEBHOOK set to the URL from the Teams channel connector. This variable is used when running the command above.

```
define contact {
    contact_name    example-team
    alias           Example Team
    host_notifications_enabled  1
    service_notifications_enabled   1
    host_notification_period	24x7
    service_notification_period	24x7 
    host_notification_options	d,u,r,f,s
    service_notification_options	w,u,c,r,f
    host_notification_commands	notify_teams
    service_notification_commands	notify_teams
    _WEBHOOKURL https://outlook.office.com/webhook/2bfd8a0a-1d45-4ea6-a736-db25a6be5c95@44467e6f-462c-4ea2-823f-7800de5434e3/IncomingWebhook/2863b6ee982c4c51af6e96852289c0c6/ba913a1a-4779-41ca-96af-93ed0869be1b
}