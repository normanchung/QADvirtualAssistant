# TRANSform's Rasa Assistant

This is a Rasa-based chatbot built for UCSB's CS 189A/B capstone project. Our team is TRANSform and we are partnered with the QAD company, a provider of Cloud ERP software for manufactuers.

## Initalization
If no existing model exists or if new training data has been added, the assistant must be trained. Train a model using your NLU data and stories - saves trained model in ./models.
```bash
rasa train
```
Test a trained Rasa model on any files starting with test_.
```bash
rasa test
```

## Running
Start an action server using the Rasa SDK.
```bash
rasa run actions
```
Load trained model. This allows you to communicate with the assistant via command line.
```bash
rasa shell
```
Run chatbot on localhost.
```bash
rasa run -m models --enable-api --cors "*" --debug
```

## Usage
Input: User makes a command (in english)
```bash
Your input -> Create a new sales order
```
Output: Bot responds with english response or relative URL
```bash
https://qvarfrdlwb01.qad.com/clouderp/#/view/qraview/hybridbrowse?viewMetaUri=urn:view:meta:com.qad.erp.sales.salesOrders&viewAction=CREATE&hybridMode=maint
```

## Current version deployed at:
http://34.105.5.32/
