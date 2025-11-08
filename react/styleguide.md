# React Style Guide

## Table of Contents
- [Component Structure](#component-structure)
- [Hooks](#hooks)
- [Props and State](#props-and-state)
- [Performance](#performance)
- [Styling](#styling)
- [Testing](#testing)
- [Accessibility](#accessibility)

## Component Structure

### Functional Components

✅ **Good:**
```tsx
import React from 'react';

interface UserProfileProps {
  userId: number;
  userName: string;
  onEdit?: () => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ 
  userId, 
  userName, 
  onEdit 
}) => {
  const [isEditing, setIsEditing] = React.useState(false);

  const handleEditClick = () => {
    setIsEditing(true);
    onEdit?.();
  };

  return (
    <div className="user-profile">
      <h2>{userName}</h2>
      <p>User ID: {userId}</p>
      <button onClick={handleEditClick}>Edit</button>
    </div>
  );
};
```

❌ **Bad:**
```tsx
// Don't use class components
class UserProfile extends React.Component {
  render() {
    return <div>{this.props.userName}</div>;
  }
}

// Don't omit types
export const UserProfile = (props) => {
  return <div>{props.userName}</div>;
};

// Don't use default export for components
export default function UserProfile() { }
```

### File Organization

✅ **Good:**
```tsx
// UserProfile.tsx
import React from 'react';
import { useUserData } from '@/hooks/useUserData';
import { formatDate } from '@/utils/dateUtils';
import type { User } from '@/types';
import './UserProfile.css';

// Types
interface UserProfileProps {
  userId: number;
}

// Component
export const UserProfile: React.FC<UserProfileProps> = ({ userId }) => {
  // Hooks
  const [isEditing, setIsEditing] = React.useState(false);
  const { user, loading, error } = useUserData(userId);

  // Effects
  React.useEffect(() => {
    // Side effects
  }, [userId]);

  // Event handlers
  const handleEdit = () => {
    setIsEditing(true);
  };

  // Render helpers
  const renderUserInfo = () => {
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;
    if (!user) return <div>User not found</div>;

    return (
      <div>
        <h2>{user.name}</h2>
        <p>{user.email}</p>
      </div>
    );
  };

  // Main render
  return (
    <div className="user-profile">
      {renderUserInfo()}
      <button onClick={handleEdit}>Edit</button>
    </div>
  );
};
```

## Hooks

### useState

✅ **Good:**
```tsx
// Simple state
const [count, setCount] = React.useState<number>(0);
const [user, setUser] = React.useState<User | null>(null);
const [isLoading, setIsLoading] = React.useState<boolean>(false);

// Complex state with callback
const [formData, setFormData] = React.useState<FormData>({
  name: '',
  email: '',
  age: 0
});

const handleInputChange = (field: keyof FormData, value: string | number) => {
  setFormData(prev => ({
    ...prev,
    [field]: value
  }));
};

// Lazy initial state for expensive operations
const [data, setData] = React.useState<Data>(() => {
  return expensiveComputation();
});
```

### useEffect

✅ **Good:**
```tsx
// Fetch data on mount
React.useEffect(() => {
  let isMounted = true;

  const fetchUser = async () => {
    try {
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();
      
      if (isMounted) {
        setUser(data);
      }
    } catch (error) {
      if (isMounted) {
        setError(error);
      }
    }
  };

  fetchUser();

  return () => {
    isMounted = false;
  };
}, [userId]);

// Cleanup subscription
React.useEffect(() => {
  const subscription = messageService.subscribe(message => {
    setMessages(prev => [...prev, message]);
  });

  return () => {
    subscription.unsubscribe();
  };
}, []);

// Multiple effects for different concerns
React.useEffect(() => {
  // Effect for user data
}, [userId]);

React.useEffect(() => {
  // Effect for analytics
}, [pageView]);
```

❌ **Bad:**
```tsx
// Missing dependency array
React.useEffect(() => {
  fetchUser(userId);  // Runs on every render!
});

// Missing cleanup
React.useEffect(() => {
  const interval = setInterval(() => {
    updateTime();
  }, 1000);
  // Should return cleanup function
}, []);

// Everything in one effect
React.useEffect(() => {
  // Mixing multiple concerns
  fetchUser();
  trackPageView();
  setupWebSocket();
}, [userId, pageView, wsUrl]);
```

### Custom Hooks

✅ **Good:**
```tsx
// useUserData.ts
import { useState, useEffect } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
}

interface UseUserDataReturn {
  user: User | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export const useUserData = (userId: number): UseUserDataReturn => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchUser = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();
      setUser(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
  }, [userId]);

  return { user, loading, error, refetch: fetchUser };
};

// Usage
const UserProfile: React.FC<{ userId: number }> = ({ userId }) => {
  const { user, loading, error, refetch } = useUserData(userId);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div>
      <h2>{user.name}</h2>
      <button onClick={refetch}>Refresh</button>
    </div>
  );
};
```

### useCallback and useMemo

✅ **Good:**
```tsx
const ExpensiveComponent: React.FC<Props> = ({ data, filter }) => {
  // Memoize expensive computation
  const filteredData = React.useMemo(() => {
    return data.filter(item => item.category === filter);
  }, [data, filter]);

  // Memoize callback to prevent child re-renders
  const handleItemClick = React.useCallback((id: number) => {
    console.log('Item clicked:', id);
    // Handle click
  }, []);

  return (
    <div>
      {filteredData.map(item => (
        <Item 
          key={item.id} 
          item={item} 
          onClick={handleItemClick} 
        />
      ))}
    </div>
  );
};

// Memoize the child component
const Item = React.memo<ItemProps>(({ item, onClick }) => {
  return (
    <div onClick={() => onClick(item.id)}>
      {item.name}
    </div>
  );
});
```

## Props and State

### Props Interface

✅ **Good:**
```tsx
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  children?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  disabled = false,
  children
}) => {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children || label}
    </button>
  );
};

// Props with generics
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string | number;
}

export const List = <T,>({ items, renderItem, keyExtractor }: ListProps<T>) => {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  );
};
```

### State Management

✅ **Good:**
```tsx
// Simple local state
const Counter: React.FC = () => {
  const [count, setCount] = React.useState(0);

  const increment = () => setCount(c => c + 1);
  const decrement = () => setCount(c => c - 1);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
};

// Complex state with useReducer
type State = {
  user: User | null;
  loading: boolean;
  error: string | null;
};

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: User }
  | { type: 'FETCH_ERROR'; payload: string };

const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, loading: true, error: null };
    case 'FETCH_SUCCESS':
      return { ...state, loading: false, user: action.payload };
    case 'FETCH_ERROR':
      return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
};

const UserProfile: React.FC = () => {
  const [state, dispatch] = React.useReducer(reducer, {
    user: null,
    loading: false,
    error: null
  });

  // Use dispatch to update state
  const fetchUser = async () => {
    dispatch({ type: 'FETCH_START' });
    try {
      const user = await api.getUser();
      dispatch({ type: 'FETCH_SUCCESS', payload: user });
    } catch (error) {
      dispatch({ type: 'FETCH_ERROR', payload: error.message });
    }
  };

  return <div>{/* Render based on state */}</div>;
};
```

## Performance

### React.memo

✅ **Good:**
```tsx
// Memoize component to prevent unnecessary re-renders
export const UserCard = React.memo<UserCardProps>(({ user, onEdit }) => {
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      <button onClick={onEdit}>Edit</button>
    </div>
  );
});

// Custom comparison function
export const UserCard = React.memo<UserCardProps>(
  ({ user, onEdit }) => {
    return <div>{/* Component JSX */}</div>;
  },
  (prevProps, nextProps) => {
    return prevProps.user.id === nextProps.user.id;
  }
);
```

### Code Splitting

✅ **Good:**
```tsx
import React, { Suspense } from 'react';

// Lazy load components
const Dashboard = React.lazy(() => import('./Dashboard'));
const UserProfile = React.lazy(() => import('./UserProfile'));
const Settings = React.lazy(() => import('./Settings'));

export const App: React.FC = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<UserProfile />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
};
```

## Styling

### CSS Modules

✅ **Good:**
```tsx
// UserCard.module.css
.card {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.title {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

// UserCard.tsx
import styles from './UserCard.module.css';

export const UserCard: React.FC<UserCardProps> = ({ user }) => {
  return (
    <div className={styles.card}>
      <h3 className={styles.title}>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
};
```

## Testing

✅ **Good:**
```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('renders user information', () => {
    const user = { id: 1, name: 'John Doe', email: 'john@example.com' };
    
    render(<UserProfile user={user} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('calls onEdit when edit button is clicked', () => {
    const user = { id: 1, name: 'John Doe', email: 'john@example.com' };
    const onEdit = jest.fn();
    
    render(<UserProfile user={user} onEdit={onEdit} />);
    
    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
    
    expect(onEdit).toHaveBeenCalledTimes(1);
  });

  it('displays loading state while fetching', async () => {
    render(<UserProfile userId={1} />);
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    });
  });
});
```

## Accessibility

✅ **Good:**
```tsx
export const AccessibleForm: React.FC = () => {
  const [name, setName] = React.useState('');
  const [email, setEmail] = React.useState('');

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="name">
        Name:
        <input
          id="name"
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          aria-required="true"
        />
      </label>

      <label htmlFor="email">
        Email:
        <input
          id="email"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          aria-required="true"
          aria-describedby="email-help"
        />
      </label>
      <span id="email-help">We'll never share your email</span>

      <button type="submit" aria-label="Submit form">
        Submit
      </button>
    </form>
  );
};
```
