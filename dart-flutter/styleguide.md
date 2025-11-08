# Dart/Flutter Style Guide

## Table of Contents
- [Project Structure](#project-structure)
- [Widget Development](#widget-development)
- [State Management](#state-management)
- [Async Programming](#async-programming)
- [Navigation](#navigation)
- [Testing](#testing)

## Project Structure

✅ **Good:**
```
lib/
├── main.dart
├── screens/
│   ├── home_screen.dart
│   ├── profile_screen.dart
│   └── settings_screen.dart
├── widgets/
│   ├── custom_button.dart
│   ├── user_card.dart
│   └── common/
│       ├── loading_indicator.dart
│       └── error_widget.dart
├── models/
│   ├── user.dart
│   └── product.dart
├── services/
│   ├── api_service.dart
│   ├── auth_service.dart
│   └── database_service.dart
├── providers/
│   ├── user_provider.dart
│   └── theme_provider.dart
├── utils/
│   ├── constants.dart
│   ├── validators.dart
│   └── helpers.dart
└── constants/
    ├── colors.dart
    └── strings.dart
```

## Widget Development

### StatelessWidget

✅ **Good:**
```dart
import 'package:flutter/material.dart';

class UserCard extends StatelessWidget {
  final String name;
  final String email;
  final VoidCallback? onTap;

  const UserCard({
    Key? key,
    required this.name,
    required this.email,
    this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(name),
        subtitle: Text(email),
        onTap: onTap,
        leading: const CircleAvatar(
          child: Icon(Icons.person),
        ),
      ),
    );
  }
}
```

### StatefulWidget

✅ **Good:**
```dart
import 'package:flutter/material.dart';

class CounterWidget extends StatefulWidget {
  final int initialCount;

  const CounterWidget({
    Key? key,
    this.initialCount = 0,
  }) : super(key: key);

  @override
  State<CounterWidget> createState() => _CounterWidgetState();
}

class _CounterWidgetState extends State<CounterWidget> {
  late int _count;

  @override
  void initState() {
    super.initState();
    _count = widget.initialCount;
  }

  void _increment() {
    setState(() {
      _count++;
    });
  }

  void _decrement() {
    setState(() {
      _count--;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          'Count: $_count',
          style: Theme.of(context).textTheme.headlineMedium,
        ),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _decrement,
              child: const Icon(Icons.remove),
            ),
            const SizedBox(width: 16),
            ElevatedButton(
              onPressed: _increment,
              child: const Icon(Icons.add),
            ),
          ],
        ),
      ],
    );
  }
}
```

### Using const Constructors

✅ **Good:**
```dart
class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
      body: const Center(
        child: Text('Welcome!'),
      ),
    );
  }
}
```

## State Management

### Provider Pattern

✅ **Good:**
```dart
// user_provider.dart
import 'package:flutter/foundation.dart';

class User {
  final String id;
  final String name;
  final String email;

  User({
    required this.id,
    required this.name,
    required this.email,
  });
}

class UserProvider with ChangeNotifier {
  User? _user;
  bool _isLoading = false;
  String? _error;

  User? get user => _user;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> fetchUser(String userId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // Simulate API call
      await Future.delayed(const Duration(seconds: 1));
      _user = User(
        id: userId,
        name: 'John Doe',
        email: 'john@example.com',
      );
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void logout() {
    _user = null;
    notifyListeners();
  }
}

// Usage in widget
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class UserProfileScreen extends StatelessWidget {
  const UserProfileScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
      ),
      body: Consumer<UserProvider>(
        builder: (context, userProvider, child) {
          if (userProvider.isLoading) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          if (userProvider.error != null) {
            return Center(
              child: Text('Error: ${userProvider.error}'),
            );
          }

          final user = userProvider.user;
          if (user == null) {
            return const Center(
              child: Text('No user logged in'),
            );
          }

          return Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  user.name,
                  style: Theme.of(context).textTheme.headlineMedium,
                ),
                const SizedBox(height: 8),
                Text(user.email),
              ],
            ),
          );
        },
      ),
    );
  }
}
```

## Async Programming

### FutureBuilder

✅ **Good:**
```dart
class UserListScreen extends StatelessWidget {
  const UserListScreen({Key? key}) : super(key: key);

  Future<List<User>> _fetchUsers() async {
    // Simulate API call
    await Future.delayed(const Duration(seconds: 2));
    return [
      User(id: '1', name: 'John Doe', email: 'john@example.com'),
      User(id: '2', name: 'Jane Smith', email: 'jane@example.com'),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Users'),
      ),
      body: FutureBuilder<List<User>>(
        future: _fetchUsers(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          if (snapshot.hasError) {
            return Center(
              child: Text('Error: ${snapshot.error}'),
            );
          }

          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(
              child: Text('No users found'),
            );
          }

          final users = snapshot.data!;
          return ListView.builder(
            itemCount: users.length,
            itemBuilder: (context, index) {
              final user = users[index];
              return UserCard(
                name: user.name,
                email: user.email,
                onTap: () {
                  // Handle tap
                },
              );
            },
          );
        },
      ),
    );
  }
}
```

### StreamBuilder

✅ **Good:**
```dart
class MessageScreen extends StatelessWidget {
  const MessageScreen({Key? key}) : super(key: key);

  Stream<List<Message>> _messageStream() async* {
    // Simulate real-time messages
    while (true) {
      await Future.delayed(const Duration(seconds: 2));
      yield [
        Message(id: '1', text: 'Hello!', timestamp: DateTime.now()),
        Message(id: '2', text: 'How are you?', timestamp: DateTime.now()),
      ];
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Messages'),
      ),
      body: StreamBuilder<List<Message>>(
        stream: _messageStream(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          if (snapshot.hasError) {
            return Center(
              child: Text('Error: ${snapshot.error}'),
            );
          }

          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(
              child: Text('No messages'),
            );
          }

          final messages = snapshot.data!;
          return ListView.builder(
            itemCount: messages.length,
            itemBuilder: (context, index) {
              final message = messages[index];
              return ListTile(
                title: Text(message.text),
                subtitle: Text(message.timestamp.toString()),
              );
            },
          );
        },
      ),
    );
  }
}
```

## Navigation

✅ **Good:**
```dart
// Define routes
class AppRoutes {
  static const String home = '/';
  static const String profile = '/profile';
  static const String settings = '/settings';
}

// Main app with routes
class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      initialRoute: AppRoutes.home,
      routes: {
        AppRoutes.home: (context) => const HomeScreen(),
        AppRoutes.profile: (context) => const ProfileScreen(),
        AppRoutes.settings: (context) => const SettingsScreen(),
      },
      onGenerateRoute: (settings) {
        // Handle dynamic routes
        if (settings.name == '/user') {
          final userId = settings.arguments as String;
          return MaterialPageRoute(
            builder: (context) => UserDetailScreen(userId: userId),
          );
        }
        return null;
      },
    );
  }
}

// Navigate to a route
void _navigateToProfile(BuildContext context) {
  Navigator.pushNamed(context, AppRoutes.profile);
}

// Navigate with arguments
void _navigateToUser(BuildContext context, String userId) {
  Navigator.pushNamed(
    context,
    '/user',
    arguments: userId,
  );
}

// Navigate and replace
void _logout(BuildContext context) {
  Navigator.pushReplacementNamed(context, AppRoutes.home);
}

// Pop with result
Future<void> _selectUser(BuildContext context) async {
  final result = await Navigator.push<User>(
    context,
    MaterialPageRoute(
      builder: (context) => const UserSelectionScreen(),
    ),
  );

  if (result != null) {
    // Handle selected user
  }
}
```

## Models

✅ **Good:**
```dart
class User {
  final String id;
  final String name;
  final String email;
  final DateTime createdAt;

  const User({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
  });

  // JSON serialization
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'created_at': createdAt.toIso8601String(),
    };
  }

  // CopyWith method for immutability
  User copyWith({
    String? id,
    String? name,
    String? email,
    DateTime? createdAt,
  }) {
    return User(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is User && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() {
    return 'User(id: $id, name: $name, email: $email)';
  }
}
```

## Testing

### Widget Tests

✅ **Good:**
```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('CounterWidget', () {
    testWidgets('displays initial count', (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CounterWidget(initialCount: 5),
          ),
        ),
      );

      // Assert
      expect(find.text('Count: 5'), findsOneWidget);
    });

    testWidgets('increments count when add button is pressed', 
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CounterWidget(initialCount: 0),
          ),
        ),
      );

      // Act
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();

      // Assert
      expect(find.text('Count: 1'), findsOneWidget);
    });

    testWidgets('decrements count when remove button is pressed',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CounterWidget(initialCount: 5),
          ),
        ),
      );

      // Act
      await tester.tap(find.byIcon(Icons.remove));
      await tester.pump();

      // Assert
      expect(find.text('Count: 4'), findsOneWidget);
    });
  });
}
```

### Unit Tests

✅ **Good:**
```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('User', () {
    test('fromJson creates User from JSON', () {
      // Arrange
      final json = {
        'id': '1',
        'name': 'John Doe',
        'email': 'john@example.com',
        'created_at': '2024-01-01T00:00:00.000Z',
      };

      // Act
      final user = User.fromJson(json);

      // Assert
      expect(user.id, '1');
      expect(user.name, 'John Doe');
      expect(user.email, 'john@example.com');
    });

    test('toJson converts User to JSON', () {
      // Arrange
      final user = User(
        id: '1',
        name: 'John Doe',
        email: 'john@example.com',
        createdAt: DateTime(2024, 1, 1),
      );

      // Act
      final json = user.toJson();

      // Assert
      expect(json['id'], '1');
      expect(json['name'], 'John Doe');
      expect(json['email'], 'john@example.com');
    });

    test('copyWith creates new User with updated fields', () {
      // Arrange
      final user = User(
        id: '1',
        name: 'John Doe',
        email: 'john@example.com',
        createdAt: DateTime(2024, 1, 1),
      );

      // Act
      final updatedUser = user.copyWith(name: 'Jane Doe');

      // Assert
      expect(updatedUser.id, user.id);
      expect(updatedUser.name, 'Jane Doe');
      expect(updatedUser.email, user.email);
    });

    test('equality compares by id', () {
      // Arrange
      final user1 = User(
        id: '1',
        name: 'John Doe',
        email: 'john@example.com',
        createdAt: DateTime(2024, 1, 1),
      );
      final user2 = User(
        id: '1',
        name: 'Jane Doe',
        email: 'jane@example.com',
        createdAt: DateTime(2024, 1, 2),
      );

      // Assert
      expect(user1, equals(user2));
    });
  });
}
```

## Error Handling

✅ **Good:**
```dart
class ApiService {
  Future<User> fetchUser(String userId) async {
    try {
      final response = await http.get(
        Uri.parse('https://api.example.com/users/$userId'),
      );

      if (response.statusCode == 200) {
        return User.fromJson(jsonDecode(response.body));
      } else if (response.statusCode == 404) {
        throw UserNotFoundException(userId);
      } else {
        throw ApiException(
          'Failed to fetch user: ${response.statusCode}',
        );
      }
    } on SocketException {
      throw NetworkException('No internet connection');
    } on FormatException {
      throw DataParseException('Invalid data format');
    } catch (e) {
      throw ApiException('Unexpected error: $e');
    }
  }
}

// Custom exceptions
class UserNotFoundException implements Exception {
  final String userId;
  UserNotFoundException(this.userId);
  
  @override
  String toString() => 'User not found: $userId';
}

class NetworkException implements Exception {
  final String message;
  NetworkException(this.message);
  
  @override
  String toString() => message;
}
```
