# Embeddings & Fine-tuning

## Overview

This guide covers vector embeddings for semantic similarity and fine-tuning custom models using OpenAI's capabilities.

## 1. Embeddings

### Create Text Embeddings

```go
req := openai.EmbeddingRequest{
    Input: []string{"The quick brown fox jumps over the lazy dog"},
    Model: openai.AdaEmbeddingV2,
}

resp, err := client.CreateEmbeddings(context.Background(), req)
if err != nil {
    fmt.Printf("CreateEmbeddings error: %v\n", err)
    return
}

embeddings := resp.Data[0].Embedding // []float32 with 1536 dimensions
fmt.Printf("Embedding dimensions: %d\n", len(embeddings))
```

### Calculate Similarity

```go
// Create embeddings for two texts
queryReq := openai.EmbeddingRequest{
    Input: []string{"What is the capital of France?"},
    Model: openai.AdaEmbeddingV2,
}

targetReq := openai.EmbeddingRequest{
    Input: []string{"Paris is the capital city of France"},
    Model: openai.AdaEmbeddingV2,
}

queryResp, _ := client.CreateEmbeddings(context.Background(), queryReq)
targetResp, _ := client.CreateEmbeddings(context.Background(), targetReq)

// Calculate similarity (dot product)
queryEmbedding := queryResp.Data[0]
targetEmbedding := targetResp.Data[0]

similarity, err := queryEmbedding.DotProduct(&targetEmbedding)
if err != nil {
    log.Fatal("Error calculating dot product:", err)
}

fmt.Printf("Similarity score: %f\n", similarity)
```

## 2. Fine-tuning

### Upload Training Data

```go
file, err := client.CreateFile(ctx, openai.FileRequest{
    FilePath: "training_data.jsonl",
    Purpose:  "fine-tune",
})
if err != nil {
    fmt.Printf("Upload file error: %v\n", err)
    return
}

fmt.Printf("File uploaded with ID: %s\n", file.ID)
```

### Create Fine-tuning Job

```go
fineTuningJob, err := client.CreateFineTuningJob(ctx, openai.FineTuningJobRequest{
    TrainingFile: file.ID,
    Model:        "davinci-002", // or "gpt-3.5-turbo-0613", "babbage-002"
})
if err != nil {
    fmt.Printf("Creating fine-tuning job error: %v\n", err)
    return
}

fmt.Printf("Fine-tuning job created with ID: %s\n", fineTuningJob.ID)
```

### Check Fine-tuning Status

```go
job, err := client.RetrieveFineTuningJob(ctx, fineTuningJob.ID)
if err != nil {
    fmt.Printf("Retrieving fine-tuning job error: %v\n", err)
    return
}

fmt.Printf("Job status: %s\n", job.Status)
if job.FineTunedModel != "" {
    fmt.Printf("Fine-tuned model: %s\n", job.FineTunedModel)
}
```

## Related Guides

- [Getting Started](getting-started.md) - Initial setup and configuration
- [Integration Patterns](integration-patterns.md) - Error handling and deployment patterns
- [Best Practices](best-practices.md) - Model selection and cost optimization