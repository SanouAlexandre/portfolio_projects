# LangFlow Customer Support Agent

An AI-powered customer support assistant built with LangFlow and Retrieval-Augmented Generation (RAG). This project seamlessly integrates company FAQs, order, and product data to provide intelligent, context-aware responses tailored for customer support use cases.

## Features

FAQ Agent: Uses RAG to search and answer questions from your company’s FAQ database, delivering accurate and relevant responses.

Order Lookup: Allows customers and support agents to query order statuses and details using sample CSV data or your own datasets.

Document Upload & RAG: Upload files such as PDFs to extend the agent’s knowledge base using vector-based retrieval for richer context.

Multi-Agent Architecture: Coordinates multiple specialized agents (FAQ, Manager, Order Lookup) to handle complex, real-world customer support scenarios.

## Project Structure

.env # Environment variables
app.py # Main application entrypoint
app_debug.py # Debug version with enhanced logging
Company_FAQ.pdf # Example FAQ document
Customer Support.json # LangFlow flow configuration
docker-compose.yml # Docker Compose setup
Dockerfile # Container image definition
requirements.txt # Python dependencies
sample_orders.csv # Sample order data
sample_products.csv # Sample product data
prompts/ # Directory containing prompt templates

## Setup & Usage

Prerequisites
Python 3.9+

Docker (optional, for containerized deployment)

Environment variables configured in .env (copy from .env.example)

## Install dependencies

pip install -r requirements.txt
Configure environment
Copy .env.example to .env and set your LangFlow API URL, API key, DataStax Astra credentials, and any other required variables.

## Run the app

### Locally

python app.py

### With Docker

Build and run the container:

docker build -t langflow_rag-app .
docker run -p 8501:8501 --env-file .env langflow_rag-app
Or deploy with Docker Swarm using the included docker-compose.yml.

## How It Works

The app connects to LangFlow workflows, leveraging DataStax Astra's scalable database for storing and retrieving structured customer data. Using Retrieval-Augmented Generation (RAG), it dynamically retrieves relevant documents and data points (from FAQs, orders, products) to generate precise, context-aware responses.

This approach enables real-time, data-driven assistance that enhances customer support efficiency by:

Quickly answering common questions

Tracking and clarifying order statuses

Providing detailed product information

Allowing easy knowledge base updates via document uploads

## Prompts & Flow Configuration

Customize agent behavior with prompt templates found in the prompts/ directory:

FAQAgent.txt

ManagerAgent.txt

OrderLookupAgent.txt

Modify the overall conversation and routing flow in Customer Support.json using the LangFlow visual editor.

## Demo

Try the live demo here:
https://demo-agent-rag-langflow.syascale.com/

License
This project is licensed under the MIT License.
