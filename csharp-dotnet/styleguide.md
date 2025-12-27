# C#/.NET Style Guide

This style guide provides concrete examples and best practices for writing clean, maintainable C#/.NET code.

## Table of Contents
- [Naming Conventions](#naming-conventions)
- [Code Organization](#code-organization)
- [Dependency Injection](#dependency-injection)
- [Async/Await Patterns](#asyncawait-patterns)
- [Error Handling](#error-handling)
- [LINQ Usage](#linq-usage)
- [Testing](#testing)

## Naming Conventions

### ✅ Good
```csharp
// Classes and methods use PascalCase
public class UserService
{
    private readonly IUserRepository _userRepository;
    private readonly ILogger<UserService> _logger;
    
    // Private fields with underscore prefix
    public async Task<User> GetUserByIdAsync(int userId)
    {
        // Local variables use camelCase
        var user = await _userRepository.GetByIdAsync(userId);
        return user;
    }
}

// Interfaces prefixed with 'I'
public interface IUserRepository
{
    Task<User> GetByIdAsync(int id);
}
```

### ❌ Bad
```csharp
// Incorrect naming conventions
public class userservice  // Should be PascalCase
{
    private IUserRepository UserRepository;  // Should use camelCase with underscore
    
    public User getuser(int ID)  // Should be GetUser, camelCase for parameters
    {
        var User = UserRepository.GetById(ID);  // User should be lowercase
        return User;
    }
}
```

## Code Organization

### ✅ Good
```csharp
// UserService.cs - One class per file
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using MyApp.Domain.Entities;
using MyApp.Domain.Interfaces;

namespace MyApp.Application.Services
{
    public class UserService : IUserService
    {
        // Fields
        private readonly IUserRepository _repository;
        private readonly ILogger<UserService> _logger;
        
        // Constructor
        public UserService(IUserRepository repository, ILogger<UserService> logger)
        {
            _repository = repository ?? throw new ArgumentNullException(nameof(repository));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }
        
        // Properties
        public int MaxRetryCount { get; set; } = 3;
        
        // Methods
        public async Task<User?> GetUserAsync(int userId)
        {
            _logger.LogInformation("Fetching user with ID: {UserId}", userId);
            return await _repository.GetByIdAsync(userId);
        }
    }
}
```

## Dependency Injection

### ✅ Good
```csharp
// Startup.cs or Program.cs
public void ConfigureServices(IServiceCollection services)
{
    services.AddScoped<IUserRepository, UserRepository>();
    services.AddScoped<IUserService, UserService>();
}

// UserService.cs
public class UserService
{
    private readonly IUserRepository _repository;
    private readonly IEmailService _emailService;
    
    public UserService(IUserRepository repository, IEmailService emailService)
    {
        _repository = repository;
        _emailService = emailService;
    }
    
    public async Task CreateUserAsync(User user)
    {
        await _repository.AddAsync(user);
        await _emailService.SendWelcomeEmailAsync(user.Email);
    }
}
```

### ❌ Bad
```csharp
// Creating dependencies directly
public class UserService
{
    public async Task CreateUserAsync(User user)
    {
        // Bad: creating dependencies manually
        var repository = new UserRepository();
        var emailService = new EmailService();
        
        await repository.AddAsync(user);
        await emailService.SendWelcomeEmailAsync(user.Email);
    }
}
```

## Async/Await Patterns

### ✅ Good
```csharp
public class UserService
{
    private readonly IUserRepository _repository;
    
    // Async method with proper naming
    public async Task<User?> GetUserAsync(int userId)
    {
        return await _repository.GetByIdAsync(userId);
    }
    
    // Parallel execution for independent operations
    public async Task<UserProfileData> GetUserProfileDataAsync(int userId)
    {
        var userTask = _repository.GetUserAsync(userId);
        var ordersTask = _orderRepository.GetOrdersByUserIdAsync(userId);
        var preferencesTask = _preferenceRepository.GetPreferencesAsync(userId);
        
        await Task.WhenAll(userTask, ordersTask, preferencesTask);
        
        return new UserProfileData
        {
            User = await userTask,
            Orders = await ordersTask,
            Preferences = await preferencesTask
        };
    }
    
    // ConfigureAwait for library code
    public async Task<bool> IsUserActiveAsync(int userId)
    {
        var user = await _repository.GetByIdAsync(userId).ConfigureAwait(false);
        return user?.IsActive ?? false;
    }
}
```

### ❌ Bad
```csharp
public class UserService
{
    // Missing Async suffix
    public async Task<User> GetUser(int userId)
    {
        // Bad: blocking on async code
        return _repository.GetByIdAsync(userId).Result;
    }
    
    // Bad: unnecessary async/await
    public async Task<User> FindUserAsync(int userId)
    {
        return await _repository.GetByIdAsync(userId);
    }
    // Should be: public Task<User> FindUserAsync(int userId) => _repository.GetByIdAsync(userId);
}
```

## Error Handling

### ✅ Good
```csharp
public class UserService
{
    private readonly ILogger<UserService> _logger;
    
    public async Task<User> GetUserAsync(int userId)
    {
        try
        {
            if (userId <= 0)
            {
                throw new ArgumentException("User ID must be positive", nameof(userId));
            }
            
            var user = await _repository.GetByIdAsync(userId);
            
            if (user == null)
            {
                throw new UserNotFoundException($"User with ID {userId} not found");
            }
            
            return user;
        }
        catch (SqlException ex) when (ex.Number == 2601)
        {
            _logger.LogWarning(ex, "Duplicate key violation for user {UserId}", userId);
            throw new DuplicateUserException("User already exists", ex);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching user {UserId}", userId);
            throw;
        }
    }
}

// Custom exception
public class UserNotFoundException : Exception
{
    public UserNotFoundException(string message) : base(message) { }
}
```

### ❌ Bad
```csharp
public class UserService
{
    public async Task<User> GetUserAsync(int userId)
    {
        try
        {
            return await _repository.GetByIdAsync(userId);
        }
        catch (Exception)  // Bad: catching generic exception without logging
        {
            return null;  // Bad: swallowing exception
        }
    }
}
```

## LINQ Usage

### ✅ Good
```csharp
public class UserService
{
    public List<User> GetActiveAdultUsers(List<User> users)
    {
        // Clear, readable LINQ query
        return users
            .Where(u => u.IsActive)
            .Where(u => u.Age >= 18)
            .OrderBy(u => u.LastName)
            .ThenBy(u => u.FirstName)
            .ToList();
    }
    
    public Dictionary<string, List<User>> GroupUsersByCountry(List<User> users)
    {
        return users
            .GroupBy(u => u.Country)
            .ToDictionary(g => g.Key, g => g.ToList());
    }
    
    public bool HasActiveUsers(List<User> users)
    {
        // Use Any() for existence checks
        return users.Any(u => u.IsActive);
    }
}
```

### ❌ Bad
```csharp
public class UserService
{
    public List<User> GetActiveAdultUsers(List<User> users)
    {
        // Bad: using loops instead of LINQ
        var result = new List<User>();
        foreach (var user in users)
        {
            if (user.IsActive && user.Age >= 18)
            {
                result.Add(user);
            }
        }
        return result;
    }
    
    public bool HasActiveUsers(List<User> users)
    {
        // Bad: using Count() when Any() is more efficient
        return users.Where(u => u.IsActive).Count() > 0;
    }
}
```

## Testing

### ✅ Good
```csharp
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _mockRepository;
    private readonly Mock<ILogger<UserService>> _mockLogger;
    private readonly UserService _service;
    
    public UserServiceTests()
    {
        _mockRepository = new Mock<IUserRepository>();
        _mockLogger = new Mock<ILogger<UserService>>();
        _service = new UserService(_mockRepository.Object, _mockLogger.Object);
    }
    
    [Fact]
    public async Task GetUserAsync_WhenUserExists_ReturnsUser()
    {
        // Arrange
        var userId = 1;
        var expectedUser = new User { Id = userId, Name = "John Doe" };
        _mockRepository.Setup(r => r.GetByIdAsync(userId))
            .ReturnsAsync(expectedUser);
        
        // Act
        var result = await _service.GetUserAsync(userId);
        
        // Assert
        Assert.NotNull(result);
        Assert.Equal(expectedUser.Id, result.Id);
        Assert.Equal(expectedUser.Name, result.Name);
    }
    
    [Fact]
    public async Task GetUserAsync_WhenUserDoesNotExist_ReturnsNull()
    {
        // Arrange
        var userId = 999;
        _mockRepository.Setup(r => r.GetByIdAsync(userId))
            .ReturnsAsync((User?)null);
        
        // Act
        var result = await _service.GetUserAsync(userId);
        
        // Assert
        Assert.Null(result);
    }
    
    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public async Task GetUserAsync_WhenUserIdIsInvalid_ThrowsArgumentException(int invalidId)
    {
        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(() => _service.GetUserAsync(invalidId));
    }
}
```

## Resource Management

### ✅ Good
```csharp
public class DataService
{
    // Using statement for automatic disposal
    public async Task<string> ReadFileAsync(string path)
    {
        using var stream = File.OpenRead(path);
        using var reader = new StreamReader(stream);
        return await reader.ReadToEndAsync();
    }
    
    // Using declaration (C# 8+)
    public async Task ProcessDataAsync()
    {
        using var connection = new SqlConnection(_connectionString);
        await connection.OpenAsync();
        
        using var command = new SqlCommand("SELECT * FROM Users", connection);
        using var reader = await command.ExecuteReaderAsync();
        
        while (await reader.ReadAsync())
        {
            // Process data
        }
    }
    
    // IDisposable implementation
    public class CustomResource : IDisposable
    {
        private bool _disposed = false;
        
        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }
        
        protected virtual void Dispose(bool disposing)
        {
            if (!_disposed)
            {
                if (disposing)
                {
                    // Dispose managed resources
                }
                // Dispose unmanaged resources
                _disposed = true;
            }
        }
    }
}
```

### ❌ Bad
```csharp
public class DataService
{
    // Not disposing resources
    public string ReadFile(string path)
    {
        var stream = File.OpenRead(path);
        var reader = new StreamReader(stream);
        return reader.ReadToEnd();
        // Bad: stream and reader not disposed
    }
}
```

## Summary

- Use consistent naming conventions (PascalCase, camelCase, interfaces with 'I')
- Organize code logically (fields, constructor, properties, methods)
- Leverage dependency injection for loose coupling
- Use async/await for I/O operations
- Handle errors appropriately with specific exceptions
- Prefer LINQ for collection operations
- Write comprehensive unit tests
- Always dispose of resources properly
