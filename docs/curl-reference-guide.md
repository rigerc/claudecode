# curl Reference Guide

## Overview

curl is a command-line tool and library for transferring data specified with URL syntax, supporting numerous protocols including HTTP, HTTPS, FTP, FTPS, SCP, SFTP, and more. It's one of the most widely used tools for testing APIs, downloading files, and automating web interactions.

## Table of Contents

- [Basic Usage](#basic-usage)
- [HTTP Methods](#http-methods)
- [Headers and Authentication](#headers-and-authentication)
- [Data Transfer](#data-transfer)
- [File Operations](#file-operations)
- [Advanced Options](#advanced-options)
- [Debugging and Troubleshooting](#debugging-and-troubleshooting)
- [Parallel Operations](#parallel-operations)
- [Security Options](#security-options)
- [Configuration Files](#configuration-files)
- [Variable Expansion](#variable-expansion)
- [libcurl Programming Examples](#libcurl-programming-examples)

## Basic Usage

### Simple GET Request

```bash
# Basic GET request
curl https://example.com

# Follow redirects
curl -L https://example.com

# Save output to file
curl -o output.html https://example.com

# Download with original filename
curl -O https://example.com/file.zip
```

### Show Response Information

```bash
# Include HTTP response headers
curl -i https://example.com

# Show only headers
curl -I https://example.com

# Verbose output (shows all communication)
curl -v https://example.com

# Silent mode (no progress meter)
curl -s https://example.com
```

## HTTP Methods

### GET Requests

```bash
# Basic GET with custom headers
curl -H "Accept: application/json" https://api.example.com/data

# GET with query parameters
curl "https://api.example.com/search?q=test&limit=10"
```

### POST Requests

```bash
# POST form data
curl -X POST https://api.example.com/submit \
  -d "name=john" \
  -d "email=john@example.com"

# POST JSON data
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'

# POST file upload
curl -X POST https://api.example.com/upload \
  -F "file=@document.pdf" \
  -F "description=Important document"
```

### PUT and DELETE

```bash
# PUT request
curl -X PUT https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Name"}'

# DELETE request
curl -X DELETE https://api.example.com/users/123
```

### Custom Methods

```bash
# PATCH request
curl -X PATCH https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{"email":"new@example.com"}'

# Custom HTTP method
curl -X CUSTOM https://api.example.com/special-endpoint
```

## Headers and Authentication

### Custom Headers

```bash
# Single header
curl -H "Authorization: Bearer token123" https://api.example.com

# Multiple headers
curl -H "Accept: application/json" \
     -H "User-Agent: MyApp/1.0" \
     -H "X-API-Version: 2.0" \
     https://api.example.com
```

### Authentication Methods

```bash
# Basic authentication
curl -u username:password https://api.example.com

# Bearer token authentication
curl -H "Authorization: Bearer your_token_here" https://api.example.com

# Digest authentication
curl --digest -u username:password https://api.example.com

# NTLM authentication
curl --ntlm -u username:password https://api.example.com

# OAuth 2.0 (with access token)
curl -H "Authorization: OAuth access_token_here" https://api.example.com
```

## Data Transfer

### Upload Data

```bash
# Upload file via PUT
curl -T upload.txt https://ftp.example.com/

# Upload via POST
curl -X POST -F "file=@data.txt" https://api.example.com/upload

# Upload multiple files
curl -F "file1=@doc1.pdf" -F "file2=@doc2.pdf" https://api.example.com/upload
```

### Download Data

```bash
# Download to specific file
curl -o downloaded.zip https://example.com/file.zip

# Download with original filename
curl -O https://example.com/filename.zip

# Resume interrupted download
curl -C - -o largefile.zip https://example.com/largefile.zip

# Download with speed limit (1KB/s)
curl --limit-rate 1k https://example.com/largefile.zip
```

## File Operations

### FTP Operations

```bash
# List FTP directory
curl ftp://ftp.example.com/

# Download via FTP
curl -O ftp://ftp.example.com/file.txt

# Upload via FTP
curl -T upload.txt ftp://ftp.example.com/

# FTP with authentication
curl -u user:pass -T upload.txt ftp://ftp.example.com/

# Delete file via FTP (using custom command)
curl -Q "DELE file.txt" ftp://ftp.example.com/
```

### SFTP Operations

```bash
# SFTP download
curl -O sftp://user:pass@example.com/path/file.txt

# SFTP upload
curl -T file.txt sftp://user:pass@example.com/path/
```

## Advanced Options

### Timeouts and Retries

```bash
# Set connection timeout (30 seconds)
curl --connect-timeout 30 https://example.com

# Set maximum time for entire operation (5 minutes)
curl --max-time 300 https://example.com

# Retry failed requests (3 times with 2-second delay)
curl --retry 3 --retry-delay 2 https://example.com

# Retry only on specific error codes
curl --retry 3 --retry-max-time 60 https://example.com
```

### Proxy Support

```bash
# Use HTTP proxy
curl -x http://proxy.example.com:8080 https://example.com

# Use SOCKS proxy
curl --socks5 proxy.example.com:1080 https://example.com

# Proxy with authentication
curl -x http://user:pass@proxy.example.com:8080 https://example.com
```

### Connection Management

```bash
# Keep connection alive
curl --keepalive-time 60 https://example.com

# Reuse connections
curl --keepalive https://example.com

# Limit connection speed
curl --limit-rate 1000B https://example.com

# Compress request data
curl --compressed https://example.com
```

## Debugging and Troubleshooting

### Debug Options

```bash
# Verbose output (shows all headers and data)
curl -v https://example.com

# Trace operation to file
curl --trace trace.log https://example.com

# Trace ASCII output to file
curl --trace-ascii trace_ascii.log https://example.com

# Show timing information
curl -w "@curl-format.txt" https://example.com

# Resolve names manually
curl --resolve example.com:443:127.0.0.1 https://example.com
```

### Response Formatting

```bash
# Pretty print JSON response (requires jq)
curl https://api.example.com/data | jq

# Show only response body
curl -s https://example.com

# Show response code
curl -w "%{http_code}" -s -o /dev/null https://example.com

# Show DNS resolve time
curl -w "DNS time: %{time_namelookup}s\n" -o /dev/null -s https://example.com
```

### Common curl-format.txt

```text
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
```

## Parallel Operations

### Multiple Downloads

```bash
# Download multiple files in parallel
curl -O https://example.com/file1.zip \
     -O https://example.com/file2.zip \
     -O https://example.com/file3.zip

# Parallel downloads with custom output names
curl -o file1.pdf https://example.com/doc1.pdf \
     -o file2.pdf https://example.com/doc2.pdf

# Use xargs for many URLs
echo -e "https://example.com/file1\nhttps://example.com/file2" | \
xargs -n1 -P4 curl -O
```

### Shell Script for Parallel Processing

```bash
#!/bin/bash
# parallel_curl.sh - Download multiple files in parallel

urls=(
    "https://example.com/file1.zip"
    "https://example.com/file2.zip"
    "https://example.com/file3.zip"
)

for url in "${urls[@]}"; do
    curl -O "$url" &
done

wait  # Wait for all background jobs to complete
echo "All downloads completed"
```

## Security Options

### SSL/TLS Configuration

```bash
# Ignore SSL certificate verification (not recommended for production)
curl -k https://example.com

# Use custom CA certificate
curl --cacert /path/to/ca-bundle.crt https://example.com

# Use client certificate
curl --cert /path/to/client.crt \
     --key /path/to/client.key \
     https://example.com

# Specify TLS version
curl --tlsv1.2 https://example.com

# Control SSL behavior
curl --ssl-reqd https://example.com  # Require SSL
curl --insecure https://example.com  # Allow insecure connections
```

### Certificate Pinning

```bash
# Pin public key hash
curl --pinnedpubkey pin-sha256-hash-value https://example.com

# Use certificate file for pinning
curl --cert-type DER --cert cert.der https://example.com
```

## Configuration Files

### Using .curlrc

Create a `~/.curlrc` file for default options:

```text
# ~/.curlrc - Default curl configuration

# Default headers
header = "User-Agent: MyApp/1.0"
header = "Accept: application/json"

# Always follow redirects
location

# Default timeout
connect-timeout = 30
max-time = 300

# Silent mode by default
silent

# Proxy settings
# proxy = http://proxy.example.com:8080
```

### Project-specific Configuration

Create a `.curlrc` in your project directory:

```text
# Project-specific curl configuration
url = "api.example.com"
header = "Authorization: Bearer ${API_TOKEN}"
output = "response.json"
verbose
```

### Loading Configuration Files

```bash
# Use specific config file
curl -K custom_config.txt https://example.com

# Load multiple config files
curl -K config1.txt -K config2.txt https://example.com
```

## Variable Expansion

curl 8.3.0+ supports variable expansion for dynamic content:

### Setting Variables

```bash
# Set literal value
--variable api_key=your_api_key_here

# Set from environment variable
--variable '%API_TOKEN'

# Set from file content
--variable data@input.json

# Set from standard input
--variable stdin_data@-
```

### Using Variables

```bash
# Expand variables in URLs
--variable user=john
--expand-url = "https://api.example.com/users/{{user}}/profile"

# Expand variables in data
--variable token=abc123
--expand-data = "{\"token\":\"{{token}}\",\"action\":\"test\"}"

# Variable transformation functions
--variable content@data.txt
--expand-data "{{content:trim:json}}"  # Trim whitespace and JSON encode

# URL encoding
--variable search="special chars & symbols"
--expand-data "query={{search:url}}"
```

### Complete Example with Variables

```bash
#!/bin/bash
# Advanced curl with variable expansion

curl \
  --variable api_key="${API_KEY}" \
  --variable user_id="${USER_ID}" \
  --variable request_data@payload.json \
  --expand-url = "https://api.example.com/v1/users/{{user_id}}" \
  --expand-header = "Authorization: Bearer {{api_key}}" \
  --expand-data = "{{request_data}}" \
  --header "Content-Type: application/json" \
  --verbose
```

## libcurl Programming Examples

### C Programming

#### Basic HTTP GET Request

```c
#include <stdio.h>
#include <curl/curl.h>

int main(void)
{
    CURL *curl;
    CURLcode res;

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://example.com");
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

        res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));
        }

        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();
    return 0;
}
```

#### Download to Memory Buffer

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

struct MemoryStruct {
    char *memory;
    size_t size;
};

static size_t write_callback(void *contents, size_t size,
                             size_t nmemb, void *userp)
{
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    char *ptr = realloc(mem->memory, mem->size + realsize + 1);
    if(!ptr) {
        printf("not enough memory (realloc returned NULL)\n");
        return 0;
    }

    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

int main(void)
{
    CURL *curl;
    CURLcode res;
    struct MemoryStruct chunk;

    chunk.memory = malloc(1);
    chunk.size = 0;

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.example.com/data");
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

        res = curl_easy_perform(curl);

        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));
        } else {
            printf("Downloaded %lu bytes\n", (unsigned long)chunk.size);
            printf("Data: %s\n", chunk.memory);
        }

        curl_easy_cleanup(curl);
    }

    free(chunk.memory);
    curl_global_cleanup();
    return 0;
}
```

#### POST Request with JSON Data

```c
#include <stdio.h>
#include <curl/curl.h>
#include <string.h>

int main(void)
{
    CURL *curl;
    CURLcode res;
    struct curl_slist *headers = NULL;

    const char *json_data = "{\"name\":\"John\",\"email\":\"john@example.com\"}";

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.example.com/users");

        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data);

        res = curl_easy_perform(curl);

        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));
        }

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();
    return 0;
}
```

#### Parallel Downloads with Multi Interface

```c
#include <stdio.h>
#include <curl/curl.h>

#define MAX_PARALLEL 5

static const char *urls[] = {
    "https://www.example1.com",
    "https://www.example2.com",
    "https://www.example3.com",
    "https://www.example4.com",
    "https://www.example5.com",
};

static size_t write_callback(char *data, size_t size, size_t nmemb, void *userp)
{
    (void)data;
    (void)userp;
    return size * nmemb;
}

static void add_transfer(CURLM *multi, int i)
{
    CURL *curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_URL, urls[i]);
        curl_easy_setopt(curl, CURLOPT_PRIVATE, urls[i]);
        curl_multi_add_handle(multi, curl);
        printf("Added: %s\n", urls[i]);
    }
}

int main(void)
{
    CURLM *multi;
    CURLMsg *msg;
    int still_running = 0;
    int msgs_left = 0;
    int i;

    curl_global_init(CURL_GLOBAL_ALL);
    multi = curl_multi_init();
    curl_multi_setopt(multi, CURLMOPT_MAXCONNECTS, (long)MAX_PARALLEL);

    for(i = 0; i < 5; i++) {
        add_transfer(multi, i);
    }

    curl_multi_perform(multi, &still_running);

    while(still_running) {
        CURLMcode mc;
        int numfds;

        mc = curl_multi_poll(multi, NULL, 0, 1000, &numfds);

        if(mc != CURLM_OK) {
            fprintf(stderr, "curl_multi_poll() failed: %s\n",
                    curl_multi_strerror(mc));
            break;
        }

        curl_multi_perform(multi, &still_running);
    }

    while((msg = curl_multi_info_read(multi, &msgs_left))) {
        if(msg->msg == CURLMSG_DONE) {
            CURL *curl = msg->easy_handle;
            CURLcode res = msg->data.result;
            char *url;

            curl_easy_getinfo(curl, CURLINFO_PRIVATE, &url);

            if(res == CURLE_OK) {
                long response_code;
                curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
                printf("Completed: %s (HTTP %ld)\n", url, response_code);
            } else {
                printf("Failed: %s (%s)\n", url, curl_easy_strerror(res));
            }

            curl_multi_remove_handle(multi, curl);
            curl_easy_cleanup(curl);
        }
    }

    curl_multi_cleanup(multi);
    curl_global_cleanup();
    return 0;
}
```

### Python with PycURL

```python
import pycurl
import json
from io import BytesIO

def get_request(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.FOLLOWLOCATION, True)
    c.perform()
    c.close()

    response_data = buffer.getvalue().decode('utf-8')
    return response_data

def post_json(url, data):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.POSTFIELDS, json.dumps(data))
    c.setopt(c.HTTPHEADER, ['Content-Type: application/json'])
    c.perform()
    c.close()

    response_data = buffer.getvalue().decode('utf-8')
    return response_data

# Usage examples
response = get_request('https://api.example.com/data')
print(response)

post_data = {'name': 'John', 'email': 'john@example.com'}
response = post_json('https://api.example.com/users', post_data)
print(response)
```

## Best Practices

1. **Always use HTTPS** when transferring sensitive data
2. **Validate SSL certificates** in production environments
3. **Set appropriate timeouts** to prevent hanging requests
4. **Use meaningful User-Agent strings** to identify your application
5. **Handle errors gracefully** and check response codes
6. **Limit request rates** to avoid overwhelming servers
7. **Secure authentication tokens** and avoid hardcoding them
8. **Use compression** for large data transfers
9. **Implement proper logging** for debugging and monitoring
10. **Test edge cases** like network failures and malformed responses

## Common Issues and Solutions

### SSL Certificate Problems
```bash
# Fix: Update CA certificates or use --cacert
curl --cacert /path/to/ca-bundle.crt https://example.com
```

### Timeouts
```bash
# Fix: Increase timeout values
curl --connect-timeout 60 --max-time 600 https://example.com
```

### Authentication Failures
```bash
# Fix: Check credentials and authentication method
curl -v -u username:password https://example.com
```

### DNS Resolution Issues
```bash
# Fix: Use IP address directly or custom DNS
curl --resolve example.com:443:93.184.216.34 https://example.com
```

### Large File Downloads
```bash
# Fix: Resume interrupted downloads
curl -C - -o largefile.zip https://example.com/largefile.zip
```

## Resources

- [Official curl Website](https://curl.se/)
- [curl Documentation](https://curl.se/docs/)
- [libcurl C API Documentation](https://curl.se/libcurl/)
- [curl Command Line Tool Manual](https://curl.se/docs/manpage.html)
- [Everything curl - Complete Guide](https://everything.curl.dev/)

---

*This reference guide covers the most commonly used curl features and options. For complete documentation, refer to the official curl website and manual pages.*