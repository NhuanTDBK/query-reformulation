# Query Reformulation System

A machine learning system that reformulates input queries into semantically similar search queries while maintaining the original intent. The system is optimized for low latency (≤100ms) on consumer-grade CPUs.

## Quick start

- Install docker and docker compose
- Run script

```bash
docker-compose build && docker-compose up
```

- Access to `localhost:8040/docs` for API documentation
- Access to `https://huggingface.co/spaces/SteveTran/query-rewrite-demo` for Gradio app

## Overview

The system takes a natural language query as input and generates multiple alternative search queries that help retrieve more comprehensive and relevant results.

### Key Requirements

- Maximum latency of 100ms on consumer-grade CPU
- No dependency on large language models (LLMs)
- Lightweight deployment with minimal infrastructure requirements
- Preservation of original search intent

## How to approach the problem

### Related Research

The system builds upon several key research areas in query reformulation:

1. **Query-to-Query Transformations**

   - Term dropping and substitution [Banerjee & Lavie, 2005]
   - Term expansion techniques
   - Machine translation approaches
   - Reinforcement learning methods

2. **E-commerce Applications**
   - Amazon's research on product search optimization using RL-powered query reformulation
   - Keyword reformulation (KR) for handling less frequent search terms
   - Query-to-keyword reformulations using seq2seq models

### Solution Approach

- **Data Collection**: Use a large-scale search query dataset to train a query reformulation model, mostly less than 300M Transformers. Check in [Data Processing](notebook/query_generation_dataset.ipynb)
- **Model Selection**: Choose a lightweight transformer model suitable for CPU inference and train it on the dataset. Check in [Training](notebook/query_seq2seq.ipynb)
- **Optimization**: Apply alignment, quantization and fine-tuning techniques to reduce model size and improve performance. Check in [Optimization](notebook/query_ppo.ipynb)
- **Evaluation**: Assess model performance using BLEU score and other metrics
- **Deployment**: Deploy the model on a cloud-based infrastructure for real-time query reformulation

## Technical Architecture

### Dataset Generation and Processing

1. **Base Dataset**: MS MARCO v1.1

   - 82,326 unique queries
   - Query length distribution:
     - 8-22 tokens: 14.7%
     - 22-36 tokens: 46.0%
     - 36-50 tokens: 28.4%
     - 50-64 tokens: 8.3%
   - Query types:
     - Descriptive: 54.6%
     - Numeric: 27.6%
     - Entity: 10.4%

2. **Data Enhancement Pipeline**:
   - Generate query variations using LLaMA 3.2 3B Q8
   - Filter pairs using Nomic Text Embedding v1.5
   - Retain pairs with semantic similarity scores between 0.6 and 0.98
   - Final training dataset: 130k query pairs

### Model Architecture

#### Base Model Selection

We evaluated and selected lightweight transformer models suitable for CPU inference:

- T5-small (61M parameters)
- Flan-T5 (77M parameters)

#### Optimization Techniques

1. Model Quantization

   - Intel OpenVINO integration
   - INT4 quantization for reduced memory footprint and faster inference

2. Training Approach
   - Sequence-to-sequence training
   - PPO (Proximal Policy Optimization) fine-tuning
   - Loss function: KL Divergence + Causal Loss

### Evaluation

Fine-tuning metrics

| Model              | BLEU     | Precisions (1-gram, 2-gram, 3-gram, 4-gram) | Brevity Penalty | Length Ratio | Translation Length | Reference Length |
| ------------------ | -------- | ------------------------------------------- | --------------- | ------------ | ------------------ | ---------------- |
| LaMini-Flan-T5-77M | 0.162680 | [0.571584, 0.349920, 0.223066, 0.174198]    | 0.547903        | 0.624353     | 50577              | 81007            |
| LaMini-T5-61M      | 0.138377 | [0.569064, 0.326063, 0.190966, 0.142126]    | 0.519445        | 0.604232     | 48947              | 81007            |
| LaMini-T5-61M-PPO  | 0.137452 | [0.588333, 0.333662, 0.191974, 0.137355]    | 0.512445        | 0.599319     | 48549              | 81007            |
| SmolLM2-135M       | 0.215715 | [0.266698, 0.236559, 0.203836, 0.168377]    | 1.0             | 3.749565     | 303741             | 81007            |
| LaMini-GPT-124M    | 0.214838 | [0.265679, 0.235619, 0.202992, 0.167648]    | 1.0             | 3.763934     | 304905             | 81007            |

## Deployments

### Infrastructure

- **Compute**: AWS EC2 c7i.large 2vcpu, 4gb mem, region: us-west-1
- **Networking**: VPC peering for private communication

### Flow

```mermaid
flowchart LR
   User -->|Interacts with| GradioApp[Gradio app]
   GradioApp -->|Sends request to| FastAPI[Fast API]
   Nginx -->|Routes requests to|
   FastAPI -->|Utilizes| OpenVINORuntime[OpenVINO Runtime]
```

### Benchmark

```
Short queries
Running 1m test @ http://50.18.255.74:8040/rewrite
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    75.29ms    7.22ms 136.54ms   72.84%
    Req/Sec    26.58      8.23    40.00     77.46%
  Latency Distribution
     50%   74.90ms
     75%   79.64ms
     90%   83.71ms
     99%   97.08ms
  1594 requests in 1.00m, 275.39KB read
```

```
Long queries
Running 1m test @ http://50.18.255.74:8040/rewrite
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    70.88ms    5.59ms 111.41ms   80.00%
    Req/Sec    14.08      5.04    20.00     57.58%
  Latency Distribution
     50%   70.46ms
     75%   72.07ms
     90%   75.98ms
     99%   89.37ms
  140 requests in 10.01s, 26.49KB read
Requests/sec:     13.99
Transfer/sec:      2.65KB
```

## References

1. Gao, J., Xie, S., He, X., & Ali, A. (2012). Learning lexicon models from search logs for query expansion. _EMNLP Proceedings_.
2. Grbovic, M., et al. (2015). Context- and content-aware embeddings for query rewriting in sponsored search.
3. Banerjee, S., & Lavie, A. (2005). METEOR: An automatic metric for MT evaluation with improved correlation with human judgments.

## Future Improvements

1. Explore additional optimization techniques for further latency reduction: layer pruning, model compression
2. Implement adaptive query reformulation based on result quality
3. Expand training dataset with domain-specific query pairs
4. Investigate hybrid approaches combining rule-based and ML methods
5. Try high-performance model serving in C++ or Rust for further latency reduction
