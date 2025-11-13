package main

import (
    "context"
    "fmt"
    "math"

    openai "github.com/sashabaranov/go-openai"
)

// EmbeddingUtils provides utilities for working with OpenAI embeddings
type EmbeddingUtils struct {
    client *openai.Client
}

// NewEmbeddingUtils creates a new embedding utilities instance
func NewEmbeddingUtils(client *openai.Client) *EmbeddingUtils {
    return &EmbeddingUtils{
        client: client,
    }
}

// CreateEmbeddings creates embeddings for multiple texts
func (eu *EmbeddingUtils) CreateEmbeddings(ctx context.Context, texts []string) ([][]float32, error) {
    req := openai.EmbeddingRequest{
        Input: texts,
        Model: openai.AdaEmbeddingV2,
    }

    resp, err := eu.client.CreateEmbeddings(ctx, req)
    if err != nil {
        return nil, fmt.Errorf("failed to create embeddings: %w", err)
    }

    embeddings := make([][]float32, len(resp.Data))
    for i, data := range resp.Data {
        embeddings[i] = data.Embedding
    }

    return embeddings, nil
}

// CalculateCosineSimilarity calculates cosine similarity between two embedding vectors
func (eu *EmbeddingUtils) CalculateCosineSimilarity(a, b []float32) (float64, error) {
    if len(a) != len(b) {
        return 0, fmt.Errorf("vectors must have same length")
    }

    var dotProduct, normA, normB float64

    for i := 0; i < len(a); i++ {
        dotProduct += float64(a[i] * b[i])
        normA += float64(a[i] * a[i])
        normB += float64(b[i] * b[i])
    }

    if normA == 0 || normB == 0 {
        return 0, fmt.Errorf("cannot calculate similarity with zero vector")
    }

    return dotProduct / (math.Sqrt(normA) * math.Sqrt(normB)), nil
}

// FindMostSimilar finds the most similar text from a list of candidates
func (eu *EmbeddingUtils) FindMostSimilar(ctx context.Context, query string, candidates []string) (string, float64, error) {
    // Create embedding for query
    queryEmbedding, err := eu.CreateEmbeddings(ctx, []string{query})
    if err != nil {
        return "", 0, fmt.Errorf("failed to create query embedding: %w", err)
    }

    // Create embeddings for candidates
    candidateEmbeddings, err := eu.CreateEmbeddings(ctx, candidates)
    if err != nil {
        return "", 0, fmt.Errorf("failed to create candidate embeddings: %w", err)
    }

    // Find best match
    bestMatch := ""
    bestScore := -1.0

    for i, candidateEmbedding := range candidateEmbeddings {
        similarity, err := eu.CalculateCosineSimilarity(queryEmbedding[0], candidateEmbedding)
        if err != nil {
            return "", 0, fmt.Errorf("failed to calculate similarity: %w", err)
        }

        if similarity > bestScore {
            bestScore = similarity
            bestMatch = candidates[i]
        }
    }

    return bestMatch, bestScore, nil
}

// BatchFindSimilar finds similar texts above a threshold
func (eu *EmbeddingUtils) BatchFindSimilar(ctx context.Context, query string, candidates []string, threshold float64) ([]SimilarResult, error) {
    // Create embedding for query
    queryEmbedding, err := eu.CreateEmbeddings(ctx, []string{query})
    if err != nil {
        return nil, fmt.Errorf("failed to create query embedding: %w", err)
    }

    // Create embeddings for candidates
    candidateEmbeddings, err := eu.CreateEmbeddings(ctx, candidates)
    if err != nil {
        return nil, fmt.Errorf("failed to create candidate embeddings: %w", err)
    }

    var results []SimilarResult

    for i, candidateEmbedding := range candidateEmbeddings {
        similarity, err := eu.CalculateCosineSimilarity(queryEmbedding[0], candidateEmbedding)
        if err != nil {
            return nil, fmt.Errorf("failed to calculate similarity: %w", err)
        }

        if similarity >= threshold {
            results = append(results, SimilarResult{
                Text:       candidates[i],
                Similarity: similarity,
            })
        }
    }

    return results, nil
}

// SimilarResult represents a similar text with its similarity score
type SimilarResult struct {
    Text       string
    Similarity float64
}

// NormalizeEmbedding normalizes an embedding vector to unit length
func (eu *EmbeddingUtils) NormalizeEmbedding(embedding []float32) []float32 {
    var norm float64
    for _, v := range embedding {
        norm += float64(v * v)
    }
    norm = math.Sqrt(norm)

    if norm == 0 {
        return embedding
    }

    normalized := make([]float32, len(embedding))
    for i, v := range embedding {
        normalized[i] = v / float32(norm)
    }

    return normalized
}

// ReduceDimensions applies a simple dimensionality reduction technique (optional)
func (eu *EmbeddingUtils) ReduceDimensions(embedding []float32, targetDimensions int) []float32 {
    if targetDimensions >= len(embedding) {
        return embedding
    }

    // Simple truncation - in practice, you might use PCA or other techniques
    reduced := make([]float32, targetDimensions)
    copy(reduced, embedding[:targetDimensions])

    return reduced
}

// EstimateEmbeddingCost estimates the cost of creating embeddings
func (eu *EmbeddingUtils) EstimateEmbeddingCost(tokenCount int) float64 {
    // Ada Embedding V2 costs $0.0001 per 1K tokens
    return float64(tokenCount) / 1000.0 * 0.0001
}

// GetEmbeddingInfo returns information about the embedding model
func (eu *EmbeddingUtils) GetEmbeddingInfo() EmbeddingInfo {
    return EmbeddingInfo{
        Model:             openai.AdaEmbeddingV2,
        Dimensions:        1536,
        MaxTokens:         8192,
        CostPerMillion:    0.1, // $0.1 per 1M tokens
    }
}

// EmbeddingInfo contains information about the embedding model
type EmbeddingInfo struct {
    Model          string
    Dimensions     int
    MaxTokens      int
    CostPerMillion float64
}