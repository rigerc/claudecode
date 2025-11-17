# Fyne Deployment Guide

## Overview

Fyne applications can be deployed to multiple platforms from a single codebase. This guide covers building for desktop, mobile, and web platforms.

## Prerequisites

### Go Development
- Go 1.16+ installed
- Basic Go development environment

### Platform-Specific Requirements
- **Windows**: Windows 10 SDK (for Windows apps)
- **macOS**: Xcode (for iOS apps)
- **Linux**: Build tools (gcc, make)
- **Mobile**: Android Studio/SDK or Xcode
- **Docker**: For cross-compilation

## Installation

### Install Fyne
```bash
# Install Fyne module
go get fyne.io/fyne/v2@latest

# Install Fyne CLI tools
go install fyne.io/tools/cmd/fyne@latest

# Verify installation
fyne version
```

### Install Cross-Compilation Tools
```bash
# Install fyne-cross for mobile and cross-platform builds
go install github.com/fyne-io/fyne-cross@latest
```

## Desktop Applications

### Standard Build
```bash
# Build for current platform
go build -o myapp

# Run the application
./myapp
```

### Cross-Compilation

#### Windows (from Linux/macOS)
```bash
# Set environment variables
export CGO_ENABLED=1
export CC=x86_64-w64-mingw32-gcc
export GOOS=windows
export GOARCH=amd64

# Build
go build -o myapp.exe

# Or use fyne-cross
fyne-cross windows -name myapp
```

#### macOS (from Linux/Windows)
```bash
# Set environment variables
export CGO_ENABLED=1
export CC=o64-clang
export GOOS=darwin
export GOARCH=amd64

# Build
go build -o myapp

# Or use fyne-cross
fyne-cross darwin -name myapp
```

#### Linux (from Windows/macOS)
```bash
# Use fyne-cross
fyne-cross linux -name myapp

# Or build with specific architecture
fyne-cross linux -arch amd64 -name myapp
fyne-cross linux -arch arm64 -name myapp
```

### Platform-Specific Installers

#### Windows Installer
```bash
# Using fyne command
fyne package -os windows

# This creates a .msi installer
```

#### macOS Application Bundle
```bash
# Create macOS app bundle
fyne package -os darwin

# Sign for distribution (requires Apple Developer account)
fyne package -os darwin -certificate "Developer ID Application: Your Name"
```

#### Linux Application
```bash
# Create AppImage
fyne package -os linux

# Or create Debian package
fyne package -os linux -deb

# Or create RPM package
fyne package -os linux -rpm
```

## Mobile Applications

### Android

#### Prerequisites
1. Android Studio installed
2. Android SDK configured
3. Set `ANDROID_HOME` environment variable
4. Enable USB debugging on device

#### Building APK
```bash
# Build APK using fyne-cross
fyne-cross android -name myapp

# Build with specific architecture
fyne-cross android -arch arm64-v8a -name myapp
fyne-cross android -arch x86 -name myapp

# Build debug APK
fyne-cross android -name myapp -debug

# Install to connected device
fyne-cross android -name myapp -install
```

#### Android Manifest Configuration
Create `AndroidManifest.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest package="com.example.myapp" xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application android:label="MyApp" android:icon="@mipmap/ic_launcher">
        <activity android:name="org.golang.app.GoNativeActivity"
                  android:label="MyApp"
                  android:exported="true"
                  android:configChanges="orientation|keyboardHidden|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

#### Using Custom Manifest
```bash
fyne-cross android -name myapp -manifest AndroidManifest.xml
```

### iOS

#### Prerequisites
1. Xcode installed
2. Apple Developer account (for device testing)
3. iOS device or simulator
4. iOS development certificate (for device deployment)

#### Building for iOS
```bash
# Build iOS app using fyne-cross
fyne-cross ios -name myapp

# Build for simulator
fyne-cross ios -name myapp -simulator

# Install to simulator
fyne-cross ios -name myapp -install

# Build for device (requires signing)
fyne-cross ios -name myapp -certificate "iPhone Developer: Your Name"
```

#### iOS Configuration
Create `Info.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>MyApp</string>
    <key>CFBundleExecutable</key>
    <string>myapp</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.myapp</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>armv7</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
</dict>
</plist>
```

#### Using Custom Info.plist
```bash
fyne-cross ios -name myapp -info-plist Info.plist
```

## WebAssembly (WASM)

### Building for Web
```bash
# Set environment variables
export GOOS=js
export GOARCH=wasm

# Build WASM module
go build -o main.wasm

# Copy JavaScript support file
cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" .

# Create HTML file
cat > index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <script src="wasm_exec.js"></script>
    <script>
        if (!WebAssembly.instantiateStreaming) {
            WebAssembly.instantiateStreaming = async (resp, importObject) => {
                const source = await (await resp).arrayBuffer();
                return WebAssembly.instantiate(source, importObject);
            };
        }

        async function run() {
            const go = new Go();
            const result = await WebAssembly.instantiateStreaming(fetch("main.wasm"), go.importObject);
            go.run(result.instance);
        }

        run();
    </script>
</head>
<body></body>
</html>
EOF
```

### Using a Web Server
```bash
# Serve files locally
python3 -m http.server 8080
# or
go run -tags nethttp ./examples/httpd/
```

## Containerization

### Dockerfile

```dockerfile
# Multi-stage build for Go application
FROM golang:1.19-alpine AS builder

# Install dependencies
RUN apk add --no-cache gcc musl-dev

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=1 GOOS=linux go build -o myapp .

# Final stage
FROM alpine:latest

RUN apk --no-cache add ca-certificates tzdata
WORKDIR /root/

COPY --from=builder /app/myapp .
COPY --from=builder /app/resources ./resources

CMD ["./myapp"]
```

### Building Docker Image
```bash
# Build Docker image
docker build -t myapp .

# Run container
docker run -p 8080:8080 myapp
```

### Docker Compose
```yaml
version: '3.8'
services:
  myapp:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
    environment:
      - MYAPP_ENV=production
```

## Advanced Configuration

### Custom Metadata

Add metadata to your application:

```go
package main

import (
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/metadata"
)

func main() {
    myApp := app.New()
    myApp.SetMetadata(&metadata.AppMetadata{
        ID: "com.example.myapp",
        Name: "MyApp",
        Version: "1.0.0",
        Build: 1,
        Icon: myIconResource,
    })
    // ... rest of application
}
```

### Application Signing

#### Windows Code Signing
```bash
# Sign Windows executable
signtool sign /f certificate.pfx /p password myapp.exe

# Timestamp signature
signtool timestamp /t http://timestamp.digicert.com myapp.exe
```

#### macOS Code Signing
```bash
# Sign macOS app
codesign --force --sign "Developer ID Application: Your Name" MyApp.app

# Verify signature
codesign --verify --verbose MyApp.app

# Notarize (required for distribution)
xcrun altool --notarize-app --primary-bundle-id "com.example.myapp" \
    --username "your@email.com" --password "@keychain:AC_PASSWORD" \
    --file MyApp.app
```

### Resource Management

#### Embedding Resources
```go
import "fyne.io/fyne/v2/storage/repository"

// Embed resources at compile time
//go:embed resources/icon.png
var iconData []byte

func loadIcon() fyne.Resource {
    return fyne.NewStaticResource("icon.png", iconData)
}
```

#### Using Storage Repository
```go
// Set custom repository for resources
repo := repository.NewFileRepository("resources")
app := app.NewWithID("com.example.myapp", storage.NewFileRepository())
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        os: [linux, windows, darwin]
        arch: [amd64, arm64]
        exclude:
          - os: windows
            arch: arm64

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Go
      uses: actions/setup-go@v2
      with:
        go-version: 1.19

    - name: Install Fyne CLI
      run: go install fyne.io/tools/cmd/fyne@latest

    - name: Build for ${{ matrix.os }} (${{ matrix.arch }})
      run: |
        fyne-cross ${{ matrix.os }} -arch ${{ matrix.arch }} -name myapp

    - name: Upload Artifacts
      uses: actions/upload-artifact@v2
      with:
        name: myapp-${{ matrix.os }}-${{ matrix.arch }}
        path: fyne-cross/bin/
```

### GitLab CI

```yaml
stages:
  - build
  - package

variables:
  GO_VERSION: "1.19"

build:
  stage: build
  image: golang:${GO_VERSION}
  before_script:
    - apt-get update -y && apt-get install -y gcc libgl1-mesa-dev
    - go install fyne.io/tools/cmd/fyne@latest
  script:
    - go build -o myapp
  artifacts:
    paths:
      - myapp

package:
  stage: package
  image: fyneio/fyne-cross:base
  dependencies:
    - build
  script:
    - fyne-cross linux -name myapp
    - fyne-cross windows -name myapp
    - fyne-cross darwin -name myapp
  artifacts:
    paths:
      - fyne-cross/dist/
```

## Distribution

### Release Management

1. **Versioning**: Use semantic versioning
2. **Changelog**: Maintain release notes
3. **Automated Builds**: Set up CI/CD pipelines
4. **Code Signing**: Sign binaries for security

### Package Formats

- **Windows**: `.exe` and `.msi` installer
- **macOS**: `.app` bundle and `.dmg` installer
- **Linux**: AppImage, `.deb`, and `.rpm` packages
- **Android**: `.apk` file
- **iOS**: `.ipa` file (App Store distribution)

### Store Distribution

#### Google Play Store
- Create developer account
- Prepare app bundle (AAB)
- Upload to Play Console
- Complete store listing

#### Apple App Store
- Apple Developer account required
- Use Xcode Archive for submission
- Follow App Store guidelines
- Test with TestFlight first

#### Microsoft Store
- Windows Developer account
- Create appx package
- Submit to Partner Center

## Troubleshooting

### Common Build Issues

1. **CGO Disabled**: Set `CGO_ENABLED=1`
2. **Missing Compilers**: Install platform-specific compilers
3. **Library Dependencies**: Install required system libraries
4. **Environment Variables**: Set correct `GOOS` and `GOARCH`

### Platform-Specific Issues

- **Windows**: Ensure Windows 10 SDK is installed
- **macOS**: Install Xcode command-line tools
- **Linux**: Install OpenGL and X11 libraries
- **Mobile**: Verify SDK installation and paths

### Debugging Build Problems

```bash
# Enable verbose output
go build -x -v

# Check Go environment
go env

# Verify Fyne version
fyne version

# Test cross-compilation setup
go tool dist list
```

## Best Practices

1. **Test on target platforms**: Validate builds on actual target systems
2. **Use CI/CD**: Automate builds and testing
3. **Version management**: Use semantic versioning
4. **Code signing**: Sign binaries for security
5. **Resource management**: Embed resources properly
6. **Error handling**: Handle platform-specific errors gracefully
7. **Documentation**: Provide clear build instructions
8. **Testing**: Test builds on all target platforms