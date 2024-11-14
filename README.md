# Query Reformulation System

A machine learning system that reformulates input queries into semantically similar search queries while maintaining the original intent. The system is optimized for low latency (≤100ms) on consumer-grade CPUs.

## Quick start

- Install docker and docker compose
- Run script

```bash
docker-compose build && docker-compose up
```

- Access to `localhost:7860`

## Overview

The system takes a natural language query as input and generates multiple alternative search queries that help retrieve more comprehensive and relevant results.

### Key Requirements

- Maximum latency of 100ms on consumer-grade CPU
- No dependency on large language models (LLMs)
- Lightweight deployment with minimal infrastructure requirements
- Preservation of original search intent

## Example Transformations

Input: "In what year was the winner of the 44th edition of the Miss World competition born?"  
Output: "44th Miss World competition winner birth year"

Input: "Who lived longer, Nikola Tesla or Milutin Milankovic?"  
Outputs:

- "Nikola Tesla lifespan"
- "Milutin Milankovic lifespan"

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

## Related Research

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

## References

1. Gao, J., Xie, S., He, X., & Ali, A. (2012). Learning lexicon models from search logs for query expansion. _EMNLP Proceedings_.
2. Grbovic, M., et al. (2015). Context- and content-aware embeddings for query rewriting in sponsored search.
3. Banerjee, S., & Lavie, A. (2005). METEOR: An automatic metric for MT evaluation with improved correlation with human judgments.

## Future Improvements

1. Explore additional optimization techniques for further latency reduction
2. Implement adaptive query reformulation based on result quality
3. Expand training dataset with domain-specific query pairs
4. Investigate hybrid approaches combining rule-based and ML methods
