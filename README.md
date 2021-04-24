# Real-time dashboard using Flask

This example shows how to create a dashboard using Python [Flask](https://flask.palletsprojects.com/en/1.1.x/) framework that streams data from Quix and makes live updates to the dashboard, and deploy the application to the public domain using Quix.

## Setup

The dashboard connects to a live stream on Quix and displays stream data on the dashboard. Therefore, you need to make sure there is a live Quix data stream for the dashboard to connect to. You can refer to our [documentation](https://documentation.platform.quix.ai/sdk/python-how-to/#connecting-to-quix) on how to create and write live data to a Quix stream. If you do not already have a Quix account, [sign up](https://portal.platform.quix.ai/self-sign-up) for a free account.

This project uses [SignalR core client](https://github.com/mandrewcito/signalrcore) to connect to Quix over websockets. You can use any compatible Python implementation of SignalR.

## Obtain credentials for Quix

Quix APIs are secured using OAuth2.0 bearer tokens. Dashboard must use a Quix a personal access token (PAT) to read data from Quix.

 1. Login to [Quix](https://portal.platform.quix.ai/workspaces).
 2. 
