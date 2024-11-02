# Code Review AI

## Introduction

Code Review AI is a tool that helps developers to review their code. It is a web-based tool that uses machine learning
to analyze the code and provide feedback to the developer. The tool can be used to identify bugs, security
vulnerabilities, and code smells in the code. It can also provide suggestions for improving the code quality and
performance.

## Installation

This project uses Docker and Docker Compose for development and deployment. To run the project locally, follow these
steps:

1. Clone the repository:
   ```
   git clone https://github.com/EzGrade/CodeReviewAI
    ```
2. Change to the project directory:
    ```
    cd CodeReviewAI
    ```
3. Fill in the environment variables in the `.env` file:
    ```
    cp .env.example .env
    ```
4. Build and run the project using Docker Compose:
    ```
    docker-compose up --build
    ```
5. Access the project in your web browser at `http://localhost:8000/docs`.
6. To stop the project, press `Ctrl+C` in the terminal and run:
    ```
    docker-compose down
    ```

### Questions that might be asked:

- Where to get GITHUB_TOKEN?

  To get the GITHUB_TOKEN, you need to create a new GitHub token. Visit the following link to create a new token:
  [Create a new GitHub token](https://github.com/settings/tokens/new) and select repo/public_repo. Then put the token in
  the .env file.


- How to run the tests?
  If container is running, you can run the tests by running the following command:

   ```
   docker-compose exec web pytest
   ```

  If container is not running, you can run the tests by running the following command:

   ```
   docker compose up -d web && docker compose exec web pytest
   ```

## Questions answers:

In anticipation of handling more than 100 review requests every in few seconds
and dealing with a base source code with a greater number than 100, I recommend designing the system as follows.
For scaling infrastructure, Kubernetes would be used for the orchestration of numerous containerized services while
providing
auto-scaling features depending on traffic patterns. To ensure optimal connectivity between the application and the load
balancer,
the maximal number of application instances would be made available to serve incoming requests. Caching strategies would
also reduce
the requests load to the GitHub and OpenAI APIs by minimizing data retrieval redundancies. For this purpose, Redis would
be used
to store and access API responses that are mostly requested. For delicate API usage such as Open AI and GitHub,
other measures like rate limit and request queuing mechanisms would be applied which could involve the usage of message
brokers such as RabbitMQ or Kafka to queue the requests and then process them asynchronously.
Furthermore, I would examine the possibility of utilizing other third parties’ APIs or self-hosted models to lessen
the reliance on external services and manage the costs.