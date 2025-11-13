# File Operations Guide

## File Upload

### From File System
```go
import "os"

file, err := os.Open("/path/to/file.json")
if err != nil {
    panic(err)
}
defer file.Close()

fileMetadata, err := client.Beta.Files.Upload(context.TODO(), anthropic.BetaFileUploadParams{
    File: anthropic.File(file, "custom-name.json", "application/json"),
    Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
})
```

### From String
```go
import "strings"

fileMetadata, err := client.Beta.Files.Upload(context.TODO(), anthropic.BetaFileUploadParams{
    File: anthropic.File(strings.NewReader("file contents"), "custom-name.json", "application/json"),
    Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
})
```

## File Management

### List Files with Auto-Paging
```go
iter := client.Beta.Files.ListAutoPaging(context.TODO(), anthropic.BetaFileListParams{
    Limit: anthropic.Int(20),
})

for iter.Next() {
    file := iter.Current()
    fmt.Printf("File: %+v\n", file)
}

if err := iter.Err(); err != nil {
    panic(err.Error())
}
```

### Download File Content
```go
import "io"

resp, err := client.Beta.Files.Download(context.TODO(), "file-id", anthropic.BetaFileDownloadParams{})
if err != nil {
    panic(err)
}
defer resp.Body.Close()

content, err := io.ReadAll(resp.Body)
fmt.Printf("File content: %s\n", string(content))
```

## Best Practices

### File Size Limits
- Check file size limits before upload
- Consider chunking large files
- Use appropriate MIME types

### Error Handling
- Handle upload failures gracefully
- Implement retry logic for transient failures
- Validate file metadata after upload

### Security
- Validate file types before upload
- Sanitize file names
- Use secure temporary storage for processing
