# TypeScript Style Guide

## Table of Contents
- [Naming Conventions](#naming-conventions)
- [Type System](#type-system)
- [Code Organization](#code-organization)
- [Best Practices](#best-practices)
- [Async/Await](#asyncawait)
- [Error Handling](#error-handling)
- [Testing](#testing)

## Naming Conventions

### Classes, Interfaces, and Types

✅ **Good:**
```typescript
class UserService {
  // Implementation
}

interface User {
  id: number;
  name: string;
  email: string;
}

type UserRole = 'admin' | 'user' | 'guest';

enum UserStatus {
  Active,
  Inactive,
  Pending
}
```

❌ **Bad:**
```typescript
class userService { }  // Should be PascalCase

interface IUser { }  // Don't use 'I' prefix in TypeScript

type userRole = 'admin' | 'user';  // Should be PascalCase

enum userStatus {  // Should be PascalCase
  active,  // Should be PascalCase
  inactive
}
```

### Variables and Functions

✅ **Good:**
```typescript
const MAX_RETRIES = 3;
const API_ENDPOINT = 'https://api.example.com';

const userName = 'John Doe';
let userCount = 0;

function getUserById(id: number): User | null {
  // Implementation
}

const calculateTotal = (items: Item[]): number => {
  return items.reduce((sum, item) => sum + item.price, 0);
};
```

❌ **Bad:**
```typescript
const maxRetries = 3;  // Constants should be UPPER_SNAKE_CASE
var UserName = 'John';  // Don't use var, should be camelCase

function GetUserById(id) {  // Should be camelCase, missing types
  // Implementation
}
```

## Type System

### Type Annotations

✅ **Good:**
```typescript
interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
  createdAt: Date;
}

function createUser(
  name: string,
  email: string,
  role: UserRole = 'user'
): User {
  return {
    id: generateId(),
    name,
    email,
    role,
    createdAt: new Date()
  };
}

const users: User[] = [];
const userMap: Map<number, User> = new Map();
const userRecord: Record<string, User> = {};
```

❌ **Bad:**
```typescript
function createUser(name, email, role) {  // Missing types
  return {
    id: generateId(),
    name,
    email,
    role,
    createdAt: new Date()
  };
}

const users = [];  // Should explicitly type as User[]
const userMap = new Map();  // Missing type parameters
```

### Union Types and Type Guards

✅ **Good:**
```typescript
type Result<T> = 
  | { success: true; data: T }
  | { success: false; error: string };

function isSuccess<T>(result: Result<T>): result is { success: true; data: T } {
  return result.success === true;
}

function processResult<T>(result: Result<T>): T {
  if (isSuccess(result)) {
    return result.data;  // TypeScript knows this is success case
  }
  throw new Error(result.error);
}

// Using 'in' operator for type guards
type Dog = { bark: () => void };
type Cat = { meow: () => void };

function makeSound(animal: Dog | Cat): void {
  if ('bark' in animal) {
    animal.bark();
  } else {
    animal.meow();
  }
}
```

### Generics

✅ **Good:**
```typescript
interface Repository<T> {
  getById(id: number): Promise<T | null>;
  getAll(): Promise<T[]>;
  create(entity: T): Promise<T>;
  update(id: number, entity: Partial<T>): Promise<T>;
  delete(id: number): Promise<void>;
}

class UserRepository implements Repository<User> {
  async getById(id: number): Promise<User | null> {
    // Implementation
  }
  
  async getAll(): Promise<User[]> {
    // Implementation
  }
  
  // ... other methods
}

// Generic with constraints
function sortByProperty<T, K extends keyof T>(
  items: T[],
  key: K
): T[] {
  return items.sort((a, b) => {
    if (a[key] < b[key]) return -1;
    if (a[key] > b[key]) return 1;
    return 0;
  });
}
```

### Utility Types

✅ **Good:**
```typescript
interface User {
  id: number;
  name: string;
  email: string;
  password: string;
  role: UserRole;
}

// Partial - make all properties optional
type UserUpdate = Partial<User>;

// Omit - exclude properties
type UserPublic = Omit<User, 'password'>;

// Pick - select specific properties
type UserCredentials = Pick<User, 'email' | 'password'>;

// Required - make all properties required
type UserRequired = Required<User>;

// Record - key-value mapping
type UserRolePermissions = Record<UserRole, string[]>;

// Example usage
const permissions: UserRolePermissions = {
  admin: ['read', 'write', 'delete'],
  user: ['read', 'write'],
  guest: ['read']
};
```

## Code Organization

### File Structure

✅ **Good:**
```typescript
// types.ts
export interface User {
  id: number;
  name: string;
  email: string;
}

export type UserRole = 'admin' | 'user' | 'guest';

// constants.ts
export const MAX_LOGIN_ATTEMPTS = 3;
export const SESSION_TIMEOUT = 3600000; // 1 hour in ms

// userService.ts
import { User, UserRole } from './types';
import { MAX_LOGIN_ATTEMPTS } from './constants';

export class UserService {
  private users: User[] = [];

  async getUserById(id: number): Promise<User | null> {
    // Implementation
  }

  async createUser(name: string, email: string): Promise<User> {
    // Implementation
  }
}

// index.ts
export { User, UserRole } from './types';
export { UserService } from './userService';
export * from './constants';
```

### Import Organization

✅ **Good:**
```typescript
// External dependencies first
import { Request, Response } from 'express';
import { Logger } from 'winston';

// Internal dependencies
import { UserService } from '@/services/userService';
import { validateEmail } from '@/utils/validation';

// Types
import type { User, UserRole } from '@/types';
```

## Best Practices

### Immutability

✅ **Good:**
```typescript
// Use const for variables that won't be reassigned
const users: readonly User[] = [
  { id: 1, name: 'John' },
  { id: 2, name: 'Jane' }
];

// Use readonly for object properties
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

// Use as const for literal types
const ROLES = {
  ADMIN: 'admin',
  USER: 'user',
  GUEST: 'guest'
} as const;

type Role = typeof ROLES[keyof typeof ROLES];

// Array operations that don't mutate
const addUser = (users: User[], newUser: User): User[] => {
  return [...users, newUser];
};

const updateUser = (users: User[], id: number, updates: Partial<User>): User[] => {
  return users.map(user => 
    user.id === id ? { ...user, ...updates } : user
  );
};
```

❌ **Bad:**
```typescript
let users = [];  // Should use const
users.push(newUser);  // Mutating array

const config = {
  apiUrl: 'https://api.example.com'
};
config.apiUrl = 'https://new-api.example.com';  // Should be readonly
```

### Function Design

✅ **Good:**
```typescript
// Clear function signature with types
function calculateDiscount(
  price: number,
  discountPercent: number = 0
): number {
  if (price < 0 || discountPercent < 0 || discountPercent > 100) {
    throw new Error('Invalid input parameters');
  }
  return price * (1 - discountPercent / 100);
}

// Arrow function for callbacks
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);

// Use optional parameters
function greetUser(name: string, title?: string): string {
  return title ? `Hello, ${title} ${name}` : `Hello, ${name}`;
}

// Use rest parameters
function sum(...numbers: number[]): number {
  return numbers.reduce((total, n) => total + n, 0);
}
```

## Async/Await

✅ **Good:**
```typescript
async function fetchUserData(userId: number): Promise<User> {
  try {
    const response = await fetch(`/api/users/${userId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const user: User = await response.json();
    return user;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}

// Parallel operations with Promise.all
async function fetchMultipleUsers(userIds: number[]): Promise<User[]> {
  const promises = userIds.map(id => fetchUserData(id));
  return Promise.all(promises);
}

// Sequential operations when needed
async function processUserWorkflow(userId: number): Promise<void> {
  const user = await fetchUserData(userId);
  const preferences = await fetchUserPreferences(userId);
  await updateUserSettings(user, preferences);
}
```

❌ **Bad:**
```typescript
function fetchUserData(userId: number): Promise<User> {
  return fetch(`/api/users/${userId}`)
    .then(response => response.json())
    .then(user => {
      return user;
    })
    .catch(error => {
      console.error(error);
      throw error;
    });
}

// Don't mix async/await with .then()
async function badExample() {
  const user = await fetchUser().then(u => u);  // Don't do this
}
```

## Error Handling

✅ **Good:**
```typescript
// Custom error classes
class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

class NotFoundError extends Error {
  constructor(resource: string, id: number | string) {
    super(`${resource} with id ${id} not found`);
    this.name = 'NotFoundError';
  }
}

// Proper error handling
async function getUserById(id: number): Promise<User> {
  if (id <= 0) {
    throw new ValidationError('User ID must be positive');
  }

  try {
    const response = await fetch(`/api/users/${id}`);
    
    if (response.status === 404) {
      throw new NotFoundError('User', id);
    }
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof ValidationError || error instanceof NotFoundError) {
      throw error;
    }
    
    // Log unexpected errors
    console.error('Unexpected error fetching user:', error);
    throw new Error('Failed to fetch user');
  }
}

// Type-safe error handling
function handleError(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unknown error occurred';
}
```

## Testing

✅ **Good:**
```typescript
import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { UserService } from './userService';

describe('UserService', () => {
  let userService: UserService;

  beforeEach(() => {
    userService = new UserService();
  });

  describe('getUserById', () => {
    it('should return user when user exists', async () => {
      // Arrange
      const userId = 1;
      const expectedUser: User = {
        id: userId,
        name: 'John Doe',
        email: 'john@example.com'
      };

      // Act
      const result = await userService.getUserById(userId);

      // Assert
      expect(result).toEqual(expectedUser);
    });

    it('should return null when user does not exist', async () => {
      // Arrange
      const userId = 999;

      // Act
      const result = await userService.getUserById(userId);

      // Assert
      expect(result).toBeNull();
    });

    it('should throw ValidationError for invalid user ID', async () => {
      // Arrange
      const invalidUserId = -1;

      // Act & Assert
      await expect(
        userService.getUserById(invalidUserId)
      ).rejects.toThrow(ValidationError);
    });
  });

  describe('createUser', () => {
    it('should create and return new user', async () => {
      // Arrange
      const name = 'Jane Doe';
      const email = 'jane@example.com';

      // Act
      const result = await userService.createUser(name, email);

      // Assert
      expect(result).toMatchObject({
        name,
        email
      });
      expect(result.id).toBeDefined();
    });
  });
});
```

## Documentation

✅ **Good:**
```typescript
/**
 * Retrieves a user by their unique identifier.
 * 
 * @param id - The unique identifier of the user
 * @returns A promise that resolves to the user if found, or null otherwise
 * @throws {ValidationError} If the user ID is invalid
 * @throws {Error} If there's a network or server error
 * 
 * @example
 * ```typescript
 * const user = await getUserById(123);
 * if (user) {
 *   console.log(user.name);
 * }
 * ```
 */
async function getUserById(id: number): Promise<User | null> {
  // Implementation
}

/**
 * Configuration options for the API client.
 */
interface ApiConfig {
  /** Base URL for API requests */
  baseUrl: string;
  /** Request timeout in milliseconds */
  timeout: number;
  /** API authentication token */
  token?: string;
}
```
