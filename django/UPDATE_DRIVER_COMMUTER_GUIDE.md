# Updating Driver/Commuter with User Data - Quick Guide

## 🎯 The Problem

When you want to update a **Driver** or **Commuter**, you need to update data in **two separate models**:

1. **User Model** - Contains: `first_name`, `last_name`, `mobileNumber`, `email`, `address`, etc.
2. **Driver/Commuter Model** - Contains: `batchId`, `cabId`, `collegeName`, `popId`, etc.

## ✅ Solution: Two API Calls

You need to make **2 separate PATCH requests**:

### For Driver:
```dart
// 1. Update User fields
PATCH /user/<user_id>
Body: {
  "first_name": "John",
  "last_name": "Doe",
  "mobileNumber": "1234567890"
}

// 2. Update Driver fields
PATCH /user/driver/<user_id>
Body: {
  "batchId": 2,
  "cabId": 3
}
```

### For Commuter:
```dart
// 1. Update User fields
PATCH /user/<user_id>
Body: {
  "first_name": "Jane",
  "mobileNumber": "9876543210"
}

// 2. Update Commuter fields
PATCH /user/commuter/<user_id>
Body: {
  "collegeName": "New College",
  "batchId": 2,
  "popId": 1
}
```

## 🚀 Easy Way: Use Helper Methods

I've added helper methods in `flutter_api_example.dart` that do both calls for you:

### Update Driver (Complete):
```dart
final api = BackendApiService();

final success = await api.updateDriverComplete(
  userId, // e.g., 1
  {
    // User fields
    'first_name': 'John',
    'mobileNumber': '1234567890',
  },
  {
    // Driver fields
    'batchId': 2,
    'cabId': 3,
  },
);

if (success) {
  print('Both user and driver updated!');
}
```

### Update Commuter (Complete):
```dart
final api = BackendApiService();

final success = await api.updateCommuterComplete(
  userId, // e.g., 1
  {
    // User fields
    'first_name': 'Jane',
    'mobileNumber': '9876543210',
  },
  {
    // Commuter fields
    'collegeName': 'New College',
    'batchId': 2,
    'isComing': true,
  },
);

if (success) {
  print('Both user and commuter updated!');
}
```

## 📝 Manual Implementation (If You Prefer)

If you want to do it manually:

```dart
Future<bool> updateDriverManually(int userId, Map<String, dynamic> userData, Map<String, dynamic> driverData) async {
  // Update user
  final userResponse = await http.patch(
    Uri.parse('$baseUrl/user/$userId'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode(userData),
  );
  
  // Update driver
  final driverResponse = await http.patch(
    Uri.parse('$baseUrl/user/driver/$userId'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode(driverData),
  );
  
  return userResponse.statusCode == 200 && driverResponse.statusCode == 200;
}
```

## ⚠️ Important Notes

1. **Both calls use the same `user_id`** - This is the User model's ID
2. **You can update only one part** - If you only want to update user OR driver, just pass `null` for the other:
   ```dart
   // Only update user, not driver
   await api.updateDriverComplete(userId, {'first_name': 'John'}, null);
   
   // Only update driver, not user
   await api.updateDriverComplete(userId, null, {'batchId': 2});
   ```
3. **Partial updates work** - You don't need to send all fields, just what you want to change
4. **Order doesn't matter** - Both API calls are independent, so you can call them in any order

## 🎨 Flutter Widget Example

```dart
class UpdateDriverScreen extends StatefulWidget {
  final int userId;
  
  @override
  _UpdateDriverScreenState createState() => _UpdateDriverScreenState();
}

class _UpdateDriverScreenState extends State<UpdateDriverScreen> {
  final _api = BackendApiService();
  final _nameController = TextEditingController();
  final _mobileController = TextEditingController();
  int? _selectedBatchId;
  int? _selectedCabId;
  bool _isLoading = false;
  
  Future<void> _updateDriver() async {
    setState(() => _isLoading = true);
    
    final success = await _api.updateDriverComplete(
      widget.userId,
      {
        'first_name': _nameController.text,
        'mobileNumber': _mobileController.text,
      },
      {
        if (_selectedBatchId != null) 'batchId': _selectedBatchId,
        if (_selectedCabId != null) 'cabId': _selectedCabId,
      },
    );
    
    setState(() => _isLoading = false);
    
    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Driver updated successfully!')),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to update driver')),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Update Driver')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _nameController,
              decoration: InputDecoration(labelText: 'Name'),
            ),
            TextField(
              controller: _mobileController,
              decoration: InputDecoration(labelText: 'Mobile Number'),
            ),
            // Add dropdowns for batch and cab selection
            ElevatedButton(
              onPressed: _isLoading ? null : _updateDriver,
              child: _isLoading 
                ? CircularProgressIndicator() 
                : Text('Update Driver'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 🔍 Why Two Calls?

The database structure separates:
- **User** (base user info) - shared by all user types
- **Driver/Commuter** (role-specific info) - specific to that role

This design allows:
- One user can potentially have multiple roles (though not implemented here)
- Cleaner data organization
- Easier to query and manage

## ✅ Summary

- **Yes, you need 2 API calls** to update both user and driver/commuter data
- **Use the helper methods** (`updateDriverComplete` or `updateCommuterComplete`) to make it easier
- **Both calls use the same `user_id`**
- **You can update only one part** by passing `null` for the other



