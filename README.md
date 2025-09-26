# Agent-Swarm
Absolutely! Here is the complete and professional README.md translated into English, ready for your GitHub repository.

Markdown

# Coding Challenge: Agent Swarm

## Introduction

This project is the solution for the AI agent swarm coding challenge. The application consists of a multi-agent system designed to collaboratively process user requests and generate comprehensive responses. The architecture is centered around a router agent that efficiently directs queries to specialized agents, ensuring accuracy and resource optimization.

## Core Features

* **Multi-Agent System:** A collaboration between three distinct agents: Router, Knowledge, and Customer Support.
* **RAG Pipeline (Retrieval-Augmented Generation):** The Knowledge Agent uses a RAG pipeline to source information from the InfinitePay website (`infinitepay.io`) and generate accurate, up-to-date answers.
* **Tool Usage:** The Customer Support Agent utilizes simulated tools to access specific user data based on the provided `user_id`.
* **Web API:** A single HTTP endpoint, built with **FastAPI**, serving as the entry point for all user interactions.
* **Containerization:** The application is fully containerized using **Docker** and **Docker Compose** for guaranteed portability and easy execution.

---

## Getting Started

### Prerequisites

Ensure you have **Docker** and **Docker Compose** installed on your machine.

### Setup

1.  Clone this repository to your local environment:
    ```bash
    git clone [https://github.com/rmorais06/Coding-Challenge-Agent-Swarm.git](https://github.com/rmorais06/Coding-Challenge-Agent-Swarm.git)
    cd Coding-Challenge-Agent-Swarm
    ```

2.  Create a `.env` file in the root directory based on the `.env.example` file. You will need a Google Gemini API key:
    ```bash
    cp .env.example .env
    ```

3.  Open the `.env` file and insert your API key:
    ```
    GOOGLE_API_KEY="insert_your_key_here"
    ```
    > **Note:** For security reasons, the `.env` file is in `.gitignore` and should not be publicly shared.

### Running the Application with Docker Compose

With the prerequisites and configuration complete, the application can be launched with a single command:

```bash
docker-compose up --build
This command will:

Build the Docker image (using the Dockerfile).

Start the container and map port 8000 to port 8000 on your host machine.

Load the necessary environment variables from your .env file.

The application is ready when the Docker logs show the Uvicorn server has started.

API Usage
The single API endpoint is available at http://localhost:8000/process_message. It accepts POST requests with a JSON body.

Endpoint
POST /process_message

Request Body (JSON)
Field	Type	Description
message	string	The user's query or statement.
user_id	string	A unique identifier for the user (e.g., "client789").

Exportar para as Planilhas
Example Request
You can test the endpoint using curl:

Bash

curl -X POST http://localhost:8000/process_message \
-H "Content-Type: application/json" \
-d '{
    "message": "What are the fees for the Smart Terminal?",
    "user_id": "client789"
}'
System Architecture and Message Flow
The system is built on a multi-agent swarm architecture utilizing LangChain. The workflow for a message is as follows:

The Router Agent receives the user's request, analyzing the message and user_id.

Based on the message's intent, the Router Agent directs the request to one of the specialized agents:

Knowledge Agent: Handles questions about products, services, fees, and public InfinitePay information. It uses a RAG pipeline to ensure factually grounded answers.

Customer Support Agent: Handles specific user issues, such as "I can't log in" or "transfer problems." It accesses simulated tools using the user_id to provide contextualized support.

The specialized agent processes the request and returns a final response, which is then sent back to the user via the API endpoint.

Implementation Details
RAG Pipeline
The RAG pipeline is implemented in knowledge_agent.py. It uses a WebBaseLoader to load data from the specified URLs, a RecursiveCharacterTextSplitter to chunk the content, and GoogleGenerativeAIEmbeddings to create vectors. These vectors are stored in a FAISS vectorstore for fast semantic search, which retrieves relevant context for the LLM (gemini-pro) to generate the final answer.

Support Agent Tools
The Customer Support Agent is equipped with two key tools that simulate interaction with an external user database:

check_account_status: Used to diagnose issues related to login, access, or general account status.

check_transaction_history: Used to investigate problems with recent transfers, payments, or other financial activity.

Technologies
Language: Python

Web Framework: FastAPI

Agent Orchestration: LangChain

LLM and Embeddings: Google Gemini (gemini-pro, embedding-001)

Containerization: Docker and Docker Compose

Testing Strategy
The testing approach focuses on validating the end-to-end flow and agent behaviors. The strategy relies on manual testing for key scenarios:

Routing Tests: Sending messages designed to deliberately route to each agent type to confirm proper decision-making.

"What are the machine fees?" -> Knowledge Agent.

"I cannot log into my account." -> Support Agent.

"What are the top news headlines today?" -> Default/Fallback response.

Tool Tests: Verifying the Support Agent correctly identifies the need for a tool and uses the provided user_id as an argument to retrieve simulated data.

RAG Accuracy: Validating that the Knowledge Agent's responses are contextually accurate and directly sourced from the specified InfinitePay web pages.





