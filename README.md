# gemini_for_webdriver

Geminiを使ってWebDriverを操作する

## Setup

```bash
PROJECT_ID=`gcloud config list --format 'value(core.project)'` && echo $PROJECT_ID
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Set Environment Variables

```bash
export PROJECT_ID=<your-project-id>
export LOCATION=<your-location>
```

## Run the Project

```bash
python example/hello_world/main.py
```
