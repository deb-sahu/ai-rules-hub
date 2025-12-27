# React Style Guide

This style guide provides concrete examples and best practices for writing clean, maintainable React applications with TypeScript.

## Table of Contents
- [Component Structure](#component-structure)
- [Hooks](#hooks)
- [State Management](#state-management)
- [Event Handling](#event-handling)
- [Conditional Rendering](#conditional-rendering)
- [Performance Optimization](#performance-optimization)
- [Forms](#forms)
- [Testing](#testing)

## Component Structure

### ✅ Good
```typescript
// UserProfile.tsx
import React, { useState, useEffect, useCallback } from 'react';
import { User } from '../types';
import { fetchUser } from '../api/userApi';

interface UserProfileProps {
    userId: number;
    onUpdate?: (user: User) => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId, onUpdate }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    useEffect(() => {
        let cancelled = false;
        
        const loadUser = async () => {
            try {
                setLoading(true);
                const data = await fetchUser(userId);
                if (!cancelled) {
                    setUser(data);
                    setError(null);
                }
            } catch (err) {
                if (!cancelled) {
                    setError('Failed to load user');
                }
            } finally {
                if (!cancelled) {
                    setLoading(false);
                }
            }
        };
        
        loadUser();
        
        return () => {
            cancelled = true;
        };
    }, [userId]);
    
    const handleUpdate = useCallback(() => {
        if (user && onUpdate) {
            onUpdate(user);
        }
    }, [user, onUpdate]);
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!user) return <div>User not found</div>;
    
    return (
        <div className="user-profile">
            <h2>{user.name}</h2>
            <p>{user.email}</p>
            <button onClick={handleUpdate}>Update</button>
        </div>
    );
};
```

### ❌ Bad
```typescript
// Bad: Multiple components in one file, no types, class component
export default class extends React.Component {
    state = {
        user: null,
        loading: true
    };
    
    componentDidMount() {
        fetch(`/api/users/${this.props.userId}`)
            .then(res => res.json())
            .then(user => this.setState({ user, loading: false }));
    }
    
    render() {
        return <div>{this.state.loading ? 'Loading' : this.state.user.name}</div>;
    }
}

function AnotherComponent() {  // Bad: multiple components per file
    return <div>Another</div>;
}
```

## Hooks

### ✅ Good
```typescript
// Custom hook for data fetching
function useFetchUser(userId: number) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
    
    useEffect(() => {
        let cancelled = false;
        
        const fetchData = async () => {
            try {
                setLoading(true);
                const data = await fetchUser(userId);
                if (!cancelled) {
                    setUser(data);
                    setError(null);
                }
            } catch (err) {
                if (!cancelled) {
                    setError(err as Error);
                }
            } finally {
                if (!cancelled) {
                    setLoading(false);
                }
            }
        };
        
        fetchData();
        
        return () => {
            cancelled = true;
        };
    }, [userId]);
    
    return { user, loading, error };
}

// Using the custom hook
const UserComponent: React.FC<{ userId: number }> = ({ userId }) => {
    const { user, loading, error } = useFetchUser(userId);
    
    if (loading) return <Spinner />;
    if (error) return <ErrorMessage error={error} />;
    if (!user) return <NotFound />;
    
    return <UserDisplay user={user} />;
};

// useCallback for event handlers
const TodoList: React.FC = () => {
    const [todos, setTodos] = useState<Todo[]>([]);
    
    const addTodo = useCallback((text: string) => {
        setTodos(prev => [...prev, { id: Date.now(), text, completed: false }]);
    }, []);
    
    const toggleTodo = useCallback((id: number) => {
        setTodos(prev => 
            prev.map(todo => 
                todo.id === id ? { ...todo, completed: !todo.completed } : todo
            )
        );
    }, []);
    
    return (
        <div>
            {todos.map(todo => (
                <TodoItem 
                    key={todo.id} 
                    todo={todo} 
                    onToggle={toggleTodo}
                />
            ))}
        </div>
    );
};

// useMemo for expensive computations
const DataTable: React.FC<{ data: Item[] }> = ({ data }) => {
    const sortedData = useMemo(() => {
        return [...data].sort((a, b) => a.name.localeCompare(b.name));
    }, [data]);
    
    const statistics = useMemo(() => {
        return {
            total: data.length,
            average: data.reduce((sum, item) => sum + item.value, 0) / data.length
        };
    }, [data]);
    
    return (
        <div>
            <Stats stats={statistics} />
            <Table data={sortedData} />
        </div>
    );
};
```

### ❌ Bad
```typescript
// Bad: Missing dependencies in useEffect
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    
    useEffect(() => {
        fetchUser(userId).then(setUser);
    }, []);  // Bad: missing userId dependency
    
    return <div>{user?.name}</div>;
}

// Bad: Not using useCallback for props
function TodoList() {
    const [todos, setTodos] = useState([]);
    
    return (
        <div>
            {todos.map(todo => (
                <TodoItem 
                    key={todo.id}
                    todo={todo}
                    // Bad: inline function creates new reference on each render
                    onToggle={() => toggleTodo(todo.id)}
                />
            ))}
        </div>
    );
}
```

## State Management

### ✅ Good
```typescript
// Local state
const Counter: React.FC = () => {
    const [count, setCount] = useState(0);
    
    const increment = () => setCount(prev => prev + 1);
    const decrement = () => setCount(prev => prev - 1);
    
    return (
        <div>
            <button onClick={decrement}>-</button>
            <span>{count}</span>
            <button onClick={increment}>+</button>
        </div>
    );
};

// Context for global state
interface AuthContextType {
    user: User | null;
    login: (credentials: Credentials) => Promise<void>;
    logout: () => void;
}

const AuthContext = React.createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    
    const login = useCallback(async (credentials: Credentials) => {
        const userData = await api.login(credentials);
        setUser(userData);
    }, []);
    
    const logout = useCallback(() => {
        setUser(null);
    }, []);
    
    const value = useMemo(
        () => ({ user, login, logout }),
        [user, login, logout]
    );
    
    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};

// Using the context
const UserMenu: React.FC = () => {
    const { user, logout } = useAuth();
    
    if (!user) return <LoginButton />;
    
    return (
        <div>
            <span>Welcome, {user.name}</span>
            <button onClick={logout}>Logout</button>
        </div>
    );
};
```

### ❌ Bad
```typescript
// Bad: Prop drilling instead of context
function App() {
    const [user, setUser] = useState(null);
    
    return (
        <Header user={user} setUser={setUser} />
        <Main user={user} setUser={setUser} />
        <Footer user={user} />
    );
}

function Header({ user, setUser }) {
    return <Nav user={user} setUser={setUser} />;
}

function Nav({ user, setUser }) {
    return <UserMenu user={user} setUser={setUser} />;
}
```

## Event Handling

### ✅ Good
```typescript
// Properly typed event handlers
const LoginForm: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    
    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value);
    };
    
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            await login({ email, password });
        } catch (error) {
            console.error('Login failed:', error);
        }
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <input
                type="email"
                value={email}
                onChange={handleEmailChange}
            />
            <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
            />
            <button type="submit">Login</button>
        </form>
    );
};

// Debounced search input
const SearchInput: React.FC<{ onSearch: (query: string) => void }> = ({ onSearch }) => {
    const [query, setQuery] = useState('');
    
    useEffect(() => {
        const timeoutId = setTimeout(() => {
            onSearch(query);
        }, 300);
        
        return () => clearTimeout(timeoutId);
    }, [query, onSearch]);
    
    return (
        <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search..."
        />
    );
};
```

### ❌ Bad
```typescript
// Bad: Not preventing default, untyped events
function LoginForm() {
    const handleSubmit = (e) => {  // Bad: no type
        login(email, password);  // Bad: didn't prevent default
    };
    
    return (
        <form onSubmit={handleSubmit}>
            {/* Form fields */}
        </form>
    );
}
```

## Conditional Rendering

### ✅ Good
```typescript
// Early returns for loading/error states
const UserProfile: React.FC<{ userId: number }> = ({ userId }) => {
    const { user, loading, error } = useFetchUser(userId);
    
    if (loading) {
        return <Spinner />;
    }
    
    if (error) {
        return <ErrorMessage message={error.message} />;
    }
    
    if (!user) {
        return <NotFound />;
    }
    
    return (
        <div className="user-profile">
            <h2>{user.name}</h2>
            <p>{user.email}</p>
        </div>
    );
};

// Ternary for simple conditions
const Badge: React.FC<{ count: number }> = ({ count }) => (
    <span className={count > 0 ? 'badge active' : 'badge'}>
        {count > 99 ? '99+' : count}
    </span>
);

// Logical AND for optional rendering
const Notification: React.FC<{ message?: string }> = ({ message }) => (
    <div>
        {message && <Alert message={message} />}
    </div>
);

// Using fragments
const UserInfo: React.FC<{ user: User }> = ({ user }) => (
    <>
        <h3>{user.name}</h3>
        <p>{user.email}</p>
    </>
);
```

### ❌ Bad
```typescript
// Bad: Nested ternaries
const Status = ({ user }) => (
    <div>
        {user ? (
            user.isActive ? (
                user.isPremium ? 'Premium Active' : 'Active'
            ) : 'Inactive'
        ) : 'No User'}
    </div>
);

// Bad: Using index as key
function TodoList({ todos }) {
    return (
        <ul>
            {todos.map((todo, index) => (
                <li key={index}>{todo.text}</li>  // Bad: index as key
            ))}
        </ul>
    );
}
```

## Performance Optimization

### ✅ Good
```typescript
// React.memo for pure components
interface UserCardProps {
    user: User;
    onSelect: (id: number) => void;
}

export const UserCard = React.memo<UserCardProps>(({ user, onSelect }) => {
    return (
        <div onClick={() => onSelect(user.id)}>
            <h3>{user.name}</h3>
            <p>{user.email}</p>
        </div>
    );
});

// Lazy loading components
const Dashboard = React.lazy(() => import('./Dashboard'));
const Settings = React.lazy(() => import('./Settings'));

const App: React.FC = () => (
    <Suspense fallback={<Spinner />}>
        <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/settings" element={<Settings />} />
        </Routes>
    </Suspense>
);

// Virtualization for long lists
import { FixedSizeList } from 'react-window';

const LargeList: React.FC<{ items: Item[] }> = ({ items }) => (
    <FixedSizeList
        height={600}
        width="100%"
        itemCount={items.length}
        itemSize={50}
    >
        {({ index, style }) => (
            <div style={style}>
                {items[index].name}
            </div>
        )}
    </FixedSizeList>
);
```

## Forms

### ✅ Good
```typescript
// Controlled form with validation
const RegistrationForm: React.FC = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [errors, setErrors] = useState<Record<string, string>>({});
    
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };
    
    const validate = (): boolean => {
        const newErrors: Record<string, string> = {};
        
        if (!formData.email.includes('@')) {
            newErrors.email = 'Invalid email address';
        }
        
        if (formData.password.length < 8) {
            newErrors.password = 'Password must be at least 8 characters';
        }
        
        if (formData.password !== formData.confirmPassword) {
            newErrors.confirmPassword = 'Passwords do not match';
        }
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };
    
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!validate()) {
            return;
        }
        
        try {
            await register(formData);
        } catch (error) {
            setErrors({ form: 'Registration failed' });
        }
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <div>
                <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    aria-invalid={!!errors.email}
                />
                {errors.email && <span className="error">{errors.email}</span>}
            </div>
            <div>
                <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    aria-invalid={!!errors.password}
                />
                {errors.password && <span className="error">{errors.password}</span>}
            </div>
            <button type="submit">Register</button>
        </form>
    );
};
```

## Testing

### ✅ Good
```typescript
// UserProfile.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserProfile } from './UserProfile';
import { fetchUser } from '../api/userApi';

jest.mock('../api/userApi');

describe('UserProfile', () => {
    it('displays loading state initially', () => {
        render(<UserProfile userId={1} />);
        expect(screen.getByText(/loading/i)).toBeInTheDocument();
    });
    
    it('displays user data when loaded', async () => {
        const mockUser = { id: 1, name: 'John Doe', email: 'john@example.com' };
        (fetchUser as jest.Mock).mockResolvedValue(mockUser);
        
        render(<UserProfile userId={1} />);
        
        await waitFor(() => {
            expect(screen.getByText('John Doe')).toBeInTheDocument();
        });
        
        expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });
    
    it('displays error message when fetch fails', async () => {
        (fetchUser as jest.Mock).mockRejectedValue(new Error('Network error'));
        
        render(<UserProfile userId={1} />);
        
        await waitFor(() => {
            expect(screen.getByText(/failed to load user/i)).toBeInTheDocument();
        });
    });
    
    it('calls onUpdate when update button is clicked', async () => {
        const mockUser = { id: 1, name: 'John Doe', email: 'john@example.com' };
        const mockOnUpdate = jest.fn();
        (fetchUser as jest.Mock).mockResolvedValue(mockUser);
        
        render(<UserProfile userId={1} onUpdate={mockOnUpdate} />);
        
        await waitFor(() => {
            expect(screen.getByText('John Doe')).toBeInTheDocument();
        });
        
        const updateButton = screen.getByRole('button', { name: /update/i });
        await userEvent.click(updateButton);
        
        expect(mockOnUpdate).toHaveBeenCalledWith(mockUser);
    });
});
```

## Summary

- Use functional components with hooks
- Define explicit TypeScript types for props
- Extract complex logic into custom hooks
- Use Context API for global state
- Implement proper error boundaries
- Optimize performance with React.memo, useMemo, useCallback
- Write accessible, semantic HTML
- Test user interactions, not implementation details
