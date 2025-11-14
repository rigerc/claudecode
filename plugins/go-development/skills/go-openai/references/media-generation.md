# Media Generation - Images & Audio

## Overview

This guide covers media generation capabilities using OpenAI's DALL-E for image generation and Whisper for audio processing.

## 1. Image Generation

### DALL-E 2 Image Generation

```go
req := openai.ImageRequest{
    Prompt:         "Parrot on a skateboard performs a trick, cartoon style, natural light, high detail",
    Size:           openai.CreateImageSize256x256,
    ResponseFormat: openai.CreateImageResponseFormatURL,
    N:              1,
}

resp, err := client.CreateImage(ctx, req)
if err != nil {
    fmt.Printf("Image creation error: %v\n", err)
    return
}

fmt.Println(resp.Data[0].URL)
```

### DALL-E 3 / GPT Image Generation

```go
req := openai.ImageRequest{
    Prompt:            "Parrot on a skateboard performing a trick. Large bold text \"SKATE MASTER\" banner at the bottom.",
    Background:        openai.CreateImageBackgroundOpaque,
    Model:             openai.CreateImageModelGptImage1,
    Size:              openai.CreateImageSize1024x1024,
    N:                 1,
    Quality:           openai.CreateImageQualityLow,
    OutputCompression: 100,
    OutputFormat:      openai.CreateImageOutputFormatJPEG,
}

resp, err := client.CreateImage(ctx, req)
if err != nil {
    fmt.Printf("Image creation error: %v\n", err)
    return
}

// Decode base64 image
imgBytes, err := base64.StdEncoding.DecodeString(resp.Data[0].B64JSON)
if err != nil {
    fmt.Printf("Base64 decode error: %v\n", err)
    return
}

// Save to file
err = os.WriteFile("generated_image.jpg", imgBytes, 0644)
if err != nil {
    fmt.Printf("Failed to write image file: %v\n", err)
    return
}
```

## 2. Audio Processing

### Speech-to-Text Transcription

```go
req := openai.AudioRequest{
    Model:    openai.Whisper1,
    FilePath: "recording.mp3",
}

resp, err := client.CreateTranscription(ctx, req)
if err != nil {
    fmt.Printf("Transcription error: %v\n", err)
    return
}

fmt.Println(resp.Text)
```

### Generate SRT Captions

```go
req := openai.AudioRequest{
    Model:    openai.Whisper1,
    FilePath: "audio.mp3",
    Format:   openai.AudioResponseFormatSRT,
}

resp, err := client.CreateTranscription(context.Background(), req)
if err != nil {
    fmt.Printf("Transcription error: %v\n", err)
    return
}

// Save SRT captions
f, err := os.Create("audio.srt")
if err != nil {
    fmt.Printf("Could not open file: %v\n", err)
    return
}
defer f.Close()

if _, err := f.WriteString(resp.Text); err != nil {
    fmt.Printf("Error writing to file: %v\n", err)
    return
}
```

## Related Guides

- [Getting Started](getting-started.md) - Initial setup and configuration
- [Integration Patterns](integration-patterns.md) - Error handling and deployment patterns
- [Best Practices](best-practices.md) - Cost optimization and usage monitoring