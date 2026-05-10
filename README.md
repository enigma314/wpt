# Overview

A simple FLASK app that can run standalone and serve as a POC for IEP + Lesson Plan analysis resulting in a Modified Action Plan proposal for a student.

## Setup

To setup make sure to create a .env file with the following environment variables exported:

```
export WPT_MODEL_PROVIDER="..."
export WPT_CLAUDE_API_KEY="sk-ant..."
export WPT_HF_API_KEY="hf_..."
```

WPT_MODEL_PROVIDER can be "CLAUDE", "HF", or "OLLAMA". Recommendation: "OLLAMA"

Most testing was done with ollama running qwen3:14b

```
ollama run qwen3:14b

git clone ...
cd wpt

export WPT_MODEL_PROVIDER="OLLAMA" # Or add this to your .env and source it

pip3 install -r requirements.txt
python3 app.py
```
_NOTE: Make sure your OLLAMA instance is running separately_

Then navigate to localhost:5000 and upload your IEP and Lesson PDFs to generate the Modified Action Plan.

## Architecture

Instead of just an MCP I produced a local harness with API calls out to your configurable model of choice. Running a local model allowed faster iteration and the experience on a local server provides more control in terms of design and UX, but this decision can be augmented to provide an MCP for a specific client with the existing generate logic.

Services have been abstracted, but further work would need to be done to make it a more robust long term and production ready solution where privacy and security are protected.

The focus was on a single POC to demonstrate providing the resources and prompting to identify actionable opportunities for accommodations and evaluations grounded in the lesson plan. That said, I did not get it where I wanted in terms of actionability but I think I made reasonable progress within a 5 hour window.

## A couple future considerations

There are a lot, but the main priority for next steps in my mind would be to do more research into successfully modified action plans. Feeding more examples of the interpretation of IEPs into the accommodations and evaluations for specific lesson plans would either be a fine tuning approach to a model, or a prompting guideline that could be supplied.

Secondly, consistency between recommendations leads me to believe exploring a sub-agent approach with multiple proposals in this format, which are then evaluated and summarized, might be a good path to explore. A committee of experts which are consulted, rather than relying on one shotting it.

## Acknowledgements

Coded with support from Claude Sonnet 4.6 Free Tier
