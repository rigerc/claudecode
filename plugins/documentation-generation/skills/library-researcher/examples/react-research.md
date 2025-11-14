# React Research Example

This example demonstrates how the Library Researcher skill analyzes React for frontend development.

## User Query
*"How do I use React for building web applications? I'm new to frontend development."*

## Research Process

### Phase 1: Library Resolution
1. **Library Name**: "React"
2. **Context7 Resolution**: Successfully resolved to React documentation
3. **Verification**: Confirmed latest React 18+ documentation

### Phase 2: Documentation Retrieval
1. **Comprehensive Docs**: Retrieved React documentation with focus on "getting started"
2. **Targeted Topics**: Components, hooks, state management, JSX
3. **Cross-reference**: Supplemented with community resources and tutorials

### Phase 3: Analysis and Synthesis
1. **Key Information Extraction**: Core concepts, setup, examples
2. **Best Practices**: Modern React patterns and common pitfalls
3. **Practical Guidance**: Actionable steps for beginners

## Library Analysis

### React Analysis

### Overview
**Primary Purpose**: A JavaScript library for building user interfaces
**Use Cases**: Single-page applications, progressive web apps, component-based UI
**Current Version**: 18.2.0
**License**: MIT

### Key Features
- **Component-Based Architecture**: Build encapsulated components that manage their own state
- **Virtual DOM**: Efficient updates through virtual DOM diffing
- **Hooks**: Stateful logic in functional components
- **JSX**: XML-like syntax for JavaScript
- **React Developer Tools**: Browser extension for debugging

### Getting Started
**Installation**:
```bash
npx create-react-app my-app
cd my-app
npm start
```

**Basic Setup**:
```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  return <h1>Hello, React!</h1>;
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
```

**First Example**: A counter component
```jsx
import React, { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
}
```

### Core API/Usage

#### Essential Hooks
1. **useState**
   - **Purpose**: Manage component state
   - **Parameters**: Initial state value
   - **Returns**: [state, setState] array
   - **Example**: `const [name, setName] = useState('')`

2. **useEffect**
   - **Purpose**: Handle side effects (API calls, subscriptions)
   - **Parameters**: Callback function, dependency array
   - **Returns**: Cleanup function
   - **Example**:
   ```jsx
   useEffect(() => {
     document.title = `Count: ${count}`;
   }, [count]);
   ```

3. **useContext**
   - **Purpose**: Access context values
   - **Parameters**: Context object
   - **Returns**: Context value
   - **Example**: `const theme = useContext(ThemeContext)`

### Best Practices

#### Recommended Patterns
1. **Functional Components with Hooks**: Prefer over class components
2. **Custom Hooks**: Extract reusable stateful logic
3. **Component Composition**: Build complex UIs from simple components
4. **Prop Drilling Avoidance**: Use context for deeply nested state

#### Common Pitfalls to Avoid
- **Direct State Mutation**: Always use setState functions
- **Missing Dependencies**: Include all dependencies in useEffect arrays
- **Infinite Renders**: Be careful with object/array dependencies
- **Overusing Context**: Don't put everything in global context

### Integration Examples

#### With CSS Frameworks (Tailwind)
```jsx
function Button({ children, variant = 'primary' }) {
  const baseClasses = 'px-4 py-2 rounded font-medium';
  const variantClasses = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300'
  };

  return (
    <button className={`${baseClasses} ${variantClasses[variant]}`}>
      {children}
    </button>
  );
}
```

#### With State Management (Redux Toolkit)
```jsx
import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement } from './counterSlice';

function Counter() {
  const count = useSelector(state => state.counter.value);
  const dispatch = useDispatch();

  return (
    <div>
      <button onClick={() => dispatch(decrement())}>-</button>
      <span>{count}</span>
      <button onClick={() => dispatch(increment())}>+</button>
    </div>
  );
}
```

### Testing

#### Unit Testing with React Testing Library
```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Counter from './Counter';

test('counter increments when button is clicked', () => {
  render(<Counter />);
  const button = screen.getByText('Click me');

  expect(screen.getByText('You clicked 0 times')).toBeInTheDocument();

  fireEvent.click(button);
  expect(screen.getByText('You clicked 1 times')).toBeInTheDocument();
});
```

### Ecosystem and Community

#### Official Resources
- **Documentation**: https://react.dev
- **API Reference**: https://react.dev/reference/react
- **Tutorials**: https://react.dev/learn

#### Community Resources
- **GitHub**: https://github.com/facebook/react
- **Stack Overflow**: [reactjs] tag
- **Reddit**: r/reactjs

#### Popular Libraries
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **Formik**: Form handling
- **React Query**: Server state management

### Alternatives

| Alternative | Pros | Cons | When to Choose |
|-------------|------|------|----------------|
| Vue.js | Gentler learning curve, excellent docs | Smaller ecosystem | Rapid prototyping, teams new to frameworks |
| Angular | Full framework opinionated approach | Steep learning curve | Large enterprise applications |
| Svelte | No virtual DOM, smaller bundles | Smaller ecosystem | Performance-critical applications |

### Maintenance and Support

#### Release Cadence
- **Frequency**: Major versions every 1-2 years
- **Versioning**: Semantic versioning
- **Breaking Changes**: Carefully managed with migration guides

#### Community
- **Corporate Backing**: Facebook/Meta
- **Active Development**: 2000+ contributors
- **Regular Updates**: Monthly patches

### Final Assessment

#### Overall Score: 9/10

**Strengths**:
- Huge ecosystem and community support
- Excellent documentation and learning resources
- Flexible and composable
- Strong corporate backing
- Performance optimizations with concurrent features

**Weaknesses**:
- JSX learning curve for pure JavaScript developers
- Requires additional libraries for complete applications
- Frequent updates can be overwhelming

**Recommendation**: Excellent choice for frontend development, especially for applications requiring complex state management and component reusability. Start with Create React App for learning, then consider custom setups for production applications.

## Learning Path for Beginners

1. **JavaScript Fundamentals**: Ensure strong ES6+ knowledge
2. **React Basics**: Components, props, state, JSX
3. **Hooks**: useState, useEffect, useContext
4. **State Management**: Context API, then Redux Toolkit if needed
5. **Routing**: React Router for navigation
6. **Advanced Topics**: Performance optimization, testing
7. **Build Tools**: Webpack, Vite for custom setups

## Next Steps

1. **Try the official React tutorial**: https://react.dev/learn
2. **Build a small project**: Todo app, weather app, or calculator
3. **Explore the ecosystem**: React Router, form libraries, state management
4. **Join the community**: React Discord, Reddit, or local meetups
5. **Read the documentation**: Deep dive into specific concepts as needed