# C#/.NET Style Guide

## Table of Contents
- [Naming Conventions](#naming-conventions)
- [Code Organization](#code-organization)
- [Best Practices](#best-practices)
- [Security](#security)
- [Performance](#performance)
- [Testing](#testing)

## Naming Conventions

### Classes and Interfaces

✅ **Good:**
```csharp
public class UserRepository { }
public interface IUserService { }
public class OrderProcessor { }
```

❌ **Bad:**
```csharp
public class userRepository { }
public interface UserService { }  // Missing 'I' prefix
public class order_processor { }
```

### Methods and Properties

✅ **Good:**
```csharp
public class UserService
{
    public async Task<User> GetUserByIdAsync(int userId)
    {
        // Implementation
    }

    public string FullName { get; set; }
}
```

❌ **Bad:**
```csharp
public class UserService
{
    public async Task<User> getUserById(int userId)  // Should be PascalCase
    {
        // Implementation
    }

    public string full_name { get; set; }  // Should be PascalCase
}
```

### Fields and Variables

✅ **Good:**
```csharp
public class OrderService
{
    private readonly ILogger<OrderService> _logger;
    private readonly IOrderRepository _orderRepository;

    public void ProcessOrder(int orderId)
    {
        var order = _orderRepository.GetById(orderId);
        var totalAmount = CalculateTotal(order);
    }
}
```

❌ **Bad:**
```csharp
public class OrderService
{
    private readonly ILogger<OrderService> logger;  // Missing underscore
    private readonly IOrderRepository OrderRepository;  // Should be camelCase with underscore

    public void ProcessOrder(int OrderId)  // Parameter should be camelCase
    {
        var Order = _orderRepository.GetById(OrderId);
        var TotalAmount = CalculateTotal(Order);
    }
}
```

## Code Organization

### Using Directives

✅ **Good:**
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using MyApp.Core.Interfaces;
using MyApp.Core.Models;

namespace MyApp.Services
{
    public class UserService : IUserService
    {
        // Implementation
    }
}
```

### Class Member Order

✅ **Good:**
```csharp
public class UserService
{
    // Constants
    private const int MaxRetries = 3;

    // Fields
    private readonly IUserRepository _userRepository;
    private readonly ILogger<UserService> _logger;

    // Constructor
    public UserService(IUserRepository userRepository, ILogger<UserService> logger)
    {
        _userRepository = userRepository;
        _logger = logger;
    }

    // Properties
    public int ActiveUsers { get; private set; }

    // Public methods
    public async Task<User> GetUserAsync(int userId)
    {
        return await _userRepository.GetByIdAsync(userId);
    }

    // Private methods
    private void LogUserActivity(int userId)
    {
        _logger.LogInformation("User {UserId} accessed", userId);
    }
}
```

## Best Practices

### Async/Await

✅ **Good:**
```csharp
public class OrderService
{
    private readonly IOrderRepository _orderRepository;

    public async Task<Order> CreateOrderAsync(Order order)
    {
        ValidateOrder(order);
        var createdOrder = await _orderRepository.AddAsync(order);
        await _orderRepository.SaveChangesAsync();
        return createdOrder;
    }
}
```

❌ **Bad:**
```csharp
public class OrderService
{
    private readonly IOrderRepository _orderRepository;

    public Order CreateOrder(Order order)  // Should be async
    {
        ValidateOrder(order);
        var createdOrder = _orderRepository.AddAsync(order).Result;  // Don't use .Result
        _orderRepository.SaveChangesAsync().Wait();  // Don't use .Wait()
        return createdOrder;
    }
}
```

### Dependency Injection

✅ **Good:**
```csharp
public interface IEmailService
{
    Task SendEmailAsync(string to, string subject, string body);
}

public class EmailService : IEmailService
{
    private readonly IConfiguration _configuration;
    private readonly ILogger<EmailService> _logger;

    public EmailService(IConfiguration configuration, ILogger<EmailService> logger)
    {
        _configuration = configuration;
        _logger = logger;
    }

    public async Task SendEmailAsync(string to, string subject, string body)
    {
        // Implementation
    }
}

// Registration in Program.cs
builder.Services.AddScoped<IEmailService, EmailService>();
```

### Error Handling

✅ **Good:**
```csharp
public async Task<User> GetUserAsync(int userId)
{
    try
    {
        if (userId <= 0)
        {
            throw new ArgumentException("User ID must be positive", nameof(userId));
        }

        var user = await _userRepository.GetByIdAsync(userId);
        
        if (user == null)
        {
            throw new UserNotFoundException($"User with ID {userId} not found");
        }

        return user;
    }
    catch (UserNotFoundException ex)
    {
        _logger.LogWarning(ex, "User not found: {UserId}", userId);
        throw;
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error retrieving user: {UserId}", userId);
        throw;
    }
}
```

❌ **Bad:**
```csharp
public async Task<User> GetUserAsync(int userId)
{
    try
    {
        return await _userRepository.GetByIdAsync(userId);
    }
    catch (Exception ex)  // Too generic
    {
        // Swallowing the exception
        return null;
    }
}
```

### LINQ Usage

✅ **Good:**
```csharp
// Method syntax for complex queries
var activeUsers = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.LastName)
    .ThenBy(u => u.FirstName)
    .Select(u => new UserDto
    {
        Id = u.Id,
        FullName = $"{u.FirstName} {u.LastName}",
        Email = u.Email
    })
    .ToList();

// Query syntax for readable queries
var query = from user in users
            where user.IsActive
            orderby user.LastName
            select user;
```

### Nullable Reference Types

✅ **Good:**
```csharp
#nullable enable

public class UserService
{
    private readonly IUserRepository _userRepository;

    public async Task<User?> FindUserAsync(string? email)
    {
        if (string.IsNullOrWhiteSpace(email))
        {
            return null;
        }

        return await _userRepository.FindByEmailAsync(email);
    }

    public string GetUserDisplayName(User user)
    {
        return user?.FullName ?? "Unknown User";
    }
}
```

## Security

### Input Validation

✅ **Good:**
```csharp
public class UserRegistrationModel
{
    [Required]
    [EmailAddress]
    public string Email { get; set; } = string.Empty;

    [Required]
    [MinLength(8)]
    [RegularExpression(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")]
    public string Password { get; set; } = string.Empty;
}

public class UserController : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> Register([FromBody] UserRegistrationModel model)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        // Process registration
        return Ok();
    }
}
```

### Parameterized Queries

✅ **Good:**
```csharp
public async Task<User> GetUserByEmailAsync(string email)
{
    var query = "SELECT * FROM Users WHERE Email = @Email";
    return await _connection.QueryFirstOrDefaultAsync<User>(
        query, 
        new { Email = email }
    );
}
```

❌ **Bad:**
```csharp
public async Task<User> GetUserByEmailAsync(string email)
{
    // SQL Injection vulnerability!
    var query = $"SELECT * FROM Users WHERE Email = '{email}'";
    return await _connection.QueryFirstOrDefaultAsync<User>(query);
}
```

## Performance

### StringBuilder for String Concatenation

✅ **Good:**
```csharp
public string BuildReport(List<string> items)
{
    var sb = new StringBuilder();
    foreach (var item in items)
    {
        sb.AppendLine($"Item: {item}");
    }
    return sb.ToString();
}
```

❌ **Bad:**
```csharp
public string BuildReport(List<string> items)
{
    string report = "";
    foreach (var item in items)
    {
        report += $"Item: {item}\n";  // Creates new string each iteration
    }
    return report;
}
```

### Proper Resource Disposal

✅ **Good:**
```csharp
public async Task<string> ReadFileAsync(string path)
{
    using var stream = new FileStream(path, FileMode.Open);
    using var reader = new StreamReader(stream);
    return await reader.ReadToEndAsync();
}

// Or with using statement
public async Task<string> ReadFileAsync(string path)
{
    using (var stream = new FileStream(path, FileMode.Open))
    using (var reader = new StreamReader(stream))
    {
        return await reader.ReadToEndAsync();
    }
}
```

## Testing

### Unit Test Structure

✅ **Good:**
```csharp
public class UserServiceTests
{
    [Fact]
    public async Task GetUserAsync_ValidUserId_ReturnsUser()
    {
        // Arrange
        var userId = 1;
        var expectedUser = new User { Id = userId, Name = "Test User" };
        var mockRepository = new Mock<IUserRepository>();
        mockRepository
            .Setup(r => r.GetByIdAsync(userId))
            .ReturnsAsync(expectedUser);
        
        var service = new UserService(mockRepository.Object);

        // Act
        var result = await service.GetUserAsync(userId);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(expectedUser.Id, result.Id);
        Assert.Equal(expectedUser.Name, result.Name);
    }

    [Fact]
    public async Task GetUserAsync_InvalidUserId_ThrowsArgumentException()
    {
        // Arrange
        var service = new UserService(Mock.Of<IUserRepository>());

        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(
            () => service.GetUserAsync(-1)
        );
    }
}
```

## Documentation

### XML Documentation

✅ **Good:**
```csharp
/// <summary>
/// Retrieves a user by their unique identifier.
/// </summary>
/// <param name="userId">The unique identifier of the user.</param>
/// <returns>A task that represents the asynchronous operation. The task result contains the user if found.</returns>
/// <exception cref="ArgumentException">Thrown when userId is less than or equal to zero.</exception>
/// <exception cref="UserNotFoundException">Thrown when the user is not found.</exception>
public async Task<User> GetUserAsync(int userId)
{
    // Implementation
}
```
