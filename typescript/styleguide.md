# TypeScript Style Guide

This style guide provides concrete examples and best practices for writing clean, type-safe TypeScript code.

## Table of Contents
- [Type Safety](#type-safety)
- [Naming Conventions](#naming-conventions)
- [Interfaces and Types](#interfaces-and-types)
- [Functions](#functions)
- [Async/Await](#asyncawait)
- [Error Handling](#error-handling)
- [Modern JavaScript Features](#modern-javascript-features)

## Type Safety

### ✅ Good
```typescript
// Explicit types for function parameters and return values
function calculateTotal(price: number, quantity: number): number {
    return price * quantity;
}

// Using interfaces for object shapes
interface User {
    id: number;
    name: string;
    email: string;
    age?: number;  // Optional property
}

function createUser(name: string, email: string): User {
    return {
        id: Date.now(),
        name,
        email
    };
}

// Using unknown instead of any
function processData(data: unknown): string {
    if (typeof data === 'string') {
        return data.toUpperCase();
    }
    if (typeof data === 'number') {
        return data.toString();
    }
    throw new Error('Unsupported data type');
}

// Strict null checking
function getUserName(user: User | null): string {
    return user?.name ?? 'Guest';
}
```

### ❌ Bad
```typescript
// Missing types
function calculateTotal(price, quantity) {  // Bad: implicit any
    return price * quantity;
}

// Using any unnecessarily
function processData(data: any): string {  // Bad: use unknown instead
    return data.toUpperCase();
}

// Not handling null/undefined
function getUserName(user: User): string {
    return user.name;  // Bad: user might be null
}
```

## Naming Conventions

### ✅ Good
```typescript
// Interfaces and types use PascalCase
interface UserProfile {
    firstName: string;
    lastName: string;
}

type UserStatus = 'active' | 'inactive' | 'pending';

// Classes use PascalCase
class UserService {
    private readonly apiUrl: string;
    
    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }
    
    async getUser(id: number): Promise<User> {
        // Method implementation
    }
}

// Variables and functions use camelCase
const userName = 'John Doe';
const isActive = true;

function calculateAge(birthDate: Date): number {
    // Implementation
}

// Constants use UPPER_SNAKE_CASE
const MAX_RETRY_ATTEMPTS = 3;
const API_BASE_URL = 'https://api.example.com';
```

### ❌ Bad
```typescript
// Inconsistent naming
interface user_profile {  // Bad: should be PascalCase
    FirstName: string;  // Bad: should be camelCase
}

const UserName = 'John';  // Bad: variables should be camelCase
const max_retry = 3;  // Bad: constants should be UPPER_SNAKE_CASE
```

## Interfaces and Types

### ✅ Good
```typescript
// Use type for unions and intersections
type Status = 'pending' | 'approved' | 'rejected';
type Result = Success | Failure;

interface Success {
    status: 'success';
    data: unknown;
}

interface Failure {
    status: 'error';
    error: Error;
}

// Use interface for object shapes
interface User {
    id: number;
    name: string;
    email: string;
}

// Extend interfaces
interface Employee extends User {
    employeeId: string;
    department: string;
}

// Utility types
type PartialUser = Partial<User>;  // All properties optional
type ReadonlyUser = Readonly<User>;  // All properties readonly
type UserWithoutEmail = Omit<User, 'email'>;  // Exclude email
type UserIdAndName = Pick<User, 'id' | 'name'>;  // Pick specific properties

// Generic types
interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
}

function fetchUser(id: number): Promise<ApiResponse<User>> {
    // Implementation
}
```

### ❌ Bad
```typescript
// Using interface for simple unions
interface Status {  // Bad: use type for unions
    status: 'pending' | 'approved' | 'rejected';
}

// Duplicating shapes instead of extending
interface Employee {  // Bad: duplicates User properties
    id: number;
    name: string;
    email: string;
    employeeId: string;
}
```

## Functions

### ✅ Good
```typescript
// Arrow functions for callbacks
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);

// Type-safe function declarations
function add(a: number, b: number): number {
    return a + b;
}

// Optional and default parameters
function greet(name: string, title?: string): string {
    return title ? `Hello, ${title} ${name}` : `Hello, ${name}`;
}

function createUser(name: string, role: string = 'user'): User {
    return { id: Date.now(), name, role };
}

// Rest parameters
function sum(...numbers: number[]): number {
    return numbers.reduce((total, n) => total + n, 0);
}

// Function overloads
function process(value: string): string;
function process(value: number): number;
function process(value: string | number): string | number {
    if (typeof value === 'string') {
        return value.toUpperCase();
    }
    return value * 2;
}

// Generic functions
function identity<T>(value: T): T {
    return value;
}

function firstElement<T>(arr: T[]): T | undefined {
    return arr[0];
}
```

### ❌ Bad
```typescript
// Missing return type
function add(a: number, b: number) {  // Bad: implicit return type
    return a + b;
}

// Using regular function where arrow function is clearer
const doubled = numbers.map(function(n) {  // Bad: verbose
    return n * 2;
});
```

## Async/Await

### ✅ Good
```typescript
// Async function with proper error handling
async function fetchUser(id: number): Promise<User | null> {
    try {
        const response = await fetch(`/api/users/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const user = await response.json();
        return user;
    } catch (error) {
        console.error('Failed to fetch user:', error);
        return null;
    }
}

// Parallel execution with Promise.all
async function fetchAllUsers(ids: number[]): Promise<User[]> {
    const promises = ids.map(id => fetchUser(id));
    const users = await Promise.all(promises);
    return users.filter((user): user is User => user !== null);
}

// Using async/await with retry logic
async function fetchWithRetry<T>(
    fn: () => Promise<T>,
    maxRetries: number = 3
): Promise<T> {
    let lastError: Error;
    
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await fn();
        } catch (error) {
            lastError = error as Error;
            if (i < maxRetries - 1) {
                await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
            }
        }
    }
    
    throw lastError!;
}
```

### ❌ Bad
```typescript
// Using .then() instead of async/await
function fetchUser(id: number): Promise<User> {
    return fetch(`/api/users/${id}`)
        .then(response => response.json())
        .then(data => data)
        .catch(error => {
            console.error(error);
            throw error;
        });
}

// Not handling promise rejection
async function processUsers() {
    const users = await fetchUsers();  // Bad: no error handling
    return users.map(u => u.name);
}
```

## Error Handling

### ✅ Good
```typescript
// Custom error types
class ValidationError extends Error {
    constructor(
        message: string,
        public field: string,
        public value: unknown
    ) {
        super(message);
        this.name = 'ValidationError';
    }
}

class ApiError extends Error {
    constructor(
        message: string,
        public statusCode: number,
        public response?: unknown
    ) {
        super(message);
        this.name = 'ApiError';
    }
}

// Type guard for errors
function isApiError(error: unknown): error is ApiError {
    return error instanceof ApiError;
}

// Proper error handling
async function createUser(data: unknown): Promise<User> {
    try {
        // Validate input
        if (!isValidUserData(data)) {
            throw new ValidationError('Invalid user data', 'data', data);
        }
        
        const response = await fetch('/api/users', {
            method: 'POST',
            body: JSON.stringify(data),
        });
        
        if (!response.ok) {
            throw new ApiError(
                'Failed to create user',
                response.status,
                await response.json()
            );
        }
        
        return await response.json();
    } catch (error) {
        if (isApiError(error)) {
            console.error(`API Error: ${error.statusCode} - ${error.message}`);
        } else if (error instanceof ValidationError) {
            console.error(`Validation Error on ${error.field}: ${error.message}`);
        } else {
            console.error('Unknown error:', error);
        }
        throw error;
    }
}

// Result type pattern (alternative to exceptions)
type Result<T, E = Error> = 
    | { success: true; value: T }
    | { success: false; error: E };

async function fetchUserSafe(id: number): Promise<Result<User>> {
    try {
        const user = await fetchUser(id);
        return { success: true, value: user };
    } catch (error) {
        return { success: false, error: error as Error };
    }
}
```

### ❌ Bad
```typescript
// Generic error handling without types
async function createUser(data: any) {
    try {
        return await fetch('/api/users', { method: 'POST', body: data });
    } catch (error) {  // Bad: error type is unknown
        console.log(error.message);  // Bad: error might not have message
    }
}

// Swallowing errors
async function processData() {
    try {
        await someOperation();
    } catch (error) {
        // Bad: empty catch block
    }
}
```

## Modern JavaScript Features

### ✅ Good
```typescript
// Destructuring
const user = { id: 1, name: 'John', email: 'john@example.com' };
const { id, name } = user;

// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];

// Spread operator
const newUser = { ...user, age: 30 };
const allNumbers = [...numbers, 6, 7, 8];

// Optional chaining
const city = user?.address?.city;
const firstItem = items?.[0];
const result = getFunction?.();

// Nullish coalescing
const displayName = user.name ?? 'Anonymous';
const port = config.port ?? 3000;

// Template literals
const greeting = `Hello, ${name}!`;
const multiLine = `
    This is a
    multi-line string
`;

// Object shorthand
const name = 'John';
const age = 30;
const person = { name, age };  // Same as { name: name, age: age }

// Computed property names
const propName = 'score';
const obj = {
    [propName]: 100,
    [`${propName}Total`]: 500
};
```

### ❌ Bad
```typescript
// Not using destructuring
const id = user.id;
const name = user.name;
const email = user.email;

// Manual null checking instead of optional chaining
const city = user && user.address && user.address.city;

// Using || instead of ??
const port = config.port || 3000;  // Bad: 0 is falsy but valid
```

## Type Guards

### ✅ Good
```typescript
// Type predicates
function isString(value: unknown): value is string {
    return typeof value === 'string';
}

function isUser(value: unknown): value is User {
    return (
        typeof value === 'object' &&
        value !== null &&
        'id' in value &&
        'name' in value &&
        'email' in value
    );
}

// Using type guards
function processValue(value: string | number): string {
    if (typeof value === 'string') {
        return value.toUpperCase();
    }
    return value.toFixed(2);
}

// Discriminated unions
type Shape =
    | { kind: 'circle'; radius: number }
    | { kind: 'square'; size: number }
    | { kind: 'rectangle'; width: number; height: number };

function calculateArea(shape: Shape): number {
    switch (shape.kind) {
        case 'circle':
            return Math.PI * shape.radius ** 2;
        case 'square':
            return shape.size ** 2;
        case 'rectangle':
            return shape.width * shape.height;
    }
}
```

## Summary

- Always use explicit types for parameters and return values
- Use `unknown` instead of `any` when type is truly unknown
- Prefer `type` for unions, `interface` for object shapes
- Use modern JavaScript features (destructuring, spread, optional chaining)
- Implement proper error handling with custom error types
- Use async/await for asynchronous operations
- Leverage utility types (Partial, Pick, Omit, etc.)
- Write type-safe code with type guards and discriminated unions
