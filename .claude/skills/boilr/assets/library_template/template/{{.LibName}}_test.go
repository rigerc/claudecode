package {{.LibName}}

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNew(t *testing.T) {
	name := "test-lib"
	description := "A test library"

	lib := New(name, description)

	assert.Equal(t, name, lib.Name())
	assert.Equal(t, description, lib.Description())
	assert.WithinDuration(t, time.Now(), lib.Created(), time.Second)
}

func TestNewWithOptions(t *testing.T) {
	name := "test-lib"
	description := "A test library"

	lib := New(name, description, WithDebug(true))

	assert.Equal(t, name, lib.Name())
	assert.Equal(t, description, lib.Description())
}

func TestString(t *testing.T) {
	lib := New("test-lib", "A test library")
	expected := "test-lib: A test library"
	actual := lib.String()

	assert.Equal(t, expected, actual)
}

func TestGreet(t *testing.T) {
	lib := New("test-lib", "A test library")
	who := "World"
	expected := "Hello World! Welcome to test-lib."
	actual := lib.Greet(who)

	assert.Equal(t, expected, actual)
}

func TestInfo(t *testing.T) {
	lib := New("test-lib", "A test library")
	info := lib.Info()

	assert.Equal(t, "test-lib", info["name"])
	assert.Equal(t, "A test library", info["description"])
	assert.NotEmpty(t, info["created"])
	assert.NotEmpty(t, info["uptime"])
}

func TestVersion(t *testing.T) {
	version := Version()
	assert.Equal(t, "1.0.0", version)
}

func TestValidate(t *testing.T) {
	tests := []struct {
		name        string
		description string
		expectError bool
	}{
		{"valid-lib", "A valid library", false},
		{"", "Empty name", true},
		{"valid-lib", "", true},
		{"", "", true},
	}

	for _, tt := range tests {
		t.Run(tt.name+"-"+tt.description, func(t *testing.T) {
			lib := New(tt.name, tt.description)
			err := lib.Validate()

			if tt.expectError {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

func BenchmarkNew(b *testing.B) {
	for i := 0; i < b.N; i++ {
		New("bench-lib", "A benchmark library")
	}
}

func BenchmarkGreet(b *testing.B) {
	lib := New("bench-lib", "A benchmark library")
	for i := 0; i < b.N; i++ {
		_ = lib.Greet("World")
	}
}

// ExampleNew demonstrates how to create a new Library instance
func ExampleNew() {
	lib := New("my-lib", "My awesome library")
	fmt.Println(lib.String())
	// Output: my-lib: My awesome library
}

// ExampleNew_withOptions demonstrates how to create a Library instance with options
func ExampleNew_withOptions() {
	lib := New("my-lib", "My awesome library", WithDebug(true))
	fmt.Println(lib.Name())
	// Output: my-lib
}

// ExampleLibrary_Greet demonstrates how to use the Greet method
func ExampleLibrary_Greet() {
	lib := New("my-lib", "My awesome library")
	fmt.Println(lib.Greet("Alice"))
	// Output: Hello Alice! Welcome to my-lib.
}

// ExampleLibrary_Info demonstrates how to get library information
func ExampleLibrary_Info() {
	lib := New("my-lib", "My awesome library")
	info := lib.Info()
	fmt.Printf("Name: %s\n", info["name"])
	// Output: Name: my-lib
}

// ExampleVersion demonstrates how to get the library version
func ExampleVersion() {
	fmt.Println("Library version:", Version())
	// Output: Library version: 1.0.0
}