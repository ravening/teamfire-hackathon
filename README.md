---
page_type: sample
description: "A minimal sample app that can be used to demonstrate deploying FastAPI apps to Azure App Service."
languages:
- python
products:
- azure
- azure-app-service
---


## Local Testing

set all the required env variables in your local machine.

ex:

```
export API_KEY=<get the key from: app service -> environment variables>
```

To try the application on your local machine:

### Install the requirements

`pip install -r requirements.txt`

### Start the application

`uvicorn main:app --reload`

### Example call

http://127.0.0.1:8000/


# Deploy on azure

Follow the steps mentioned in wiki: 

https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=fastapi%2Cmac-linux%2Cazure-cli%2Czip-deploy%2Cdeploy-instructions-azcli%2Cterminal-powershell%2Cdeploy-instructions-zip-curl#4---configure-startup-script