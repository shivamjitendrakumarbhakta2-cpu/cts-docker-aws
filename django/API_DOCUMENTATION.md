# API Documentation for Flutter Integration

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Base URL Structure](#base-url-structure)
3. [Authentication](#authentication)
4. [User Services APIs](#user-services-apis)
5. [Cab Services APIs](#cab-services-apis)
6. [D2D Log APIs](#d2d-log-apis)
7. [Common Update Operations](#common-update-operations)
8. [Flutter Integration Examples](#flutter-integration-examples)

---

## Project Overview

This is a Django REST Framework backend for a cab/transport service management system. The project has three main apps:

1. **user_servcies** - User management (Users, Commuters, Drivers, Admins)
2. **cab_services** - Cab/Route management (Routes, Batches, Pickup Points, Cabs)
3. **d2d_log** - Day-to-day trip logging and management

**Base URL Pattern**: All APIs are prefixed with:
- `/user/` - User services
- `/cab/` - Cab services  
- `/d2d/` - D2D log services

---

## Base URL Structure

Assuming your Django server runs on `http://localhost:8000` or your deployed domain:

```
Base URL: http://your-domain.com
```

---

## Authentication

### Login
**Endpoint**: `POST /user/login`

**Request Body**:
```json
{
  "mobileNumber": "1234567890",
  "password": "your_password"
}
```

**Response** (Success - 200):
```json
{
  "user_id": 1,
  "user_type": "COMMUTER" // or "DRIVER" or "ADMIN"
}
```

**Response** (Error - 400):
```json
{
  "error": "Invalid credentials"
}
```

### Logout
**Endpoint**: `POST /user/logout`

**Response**:
```
"User Logged Out"
```

---

## User Services APIs

### 1. Create User (Register)
**Endpoint**: `POST /user/`

**Request Body**:
```json
{
  "user": {
    "username": "John Doe",
    "mobileNumber": "1234567890",
    "password": "password123",
    "email": "john@example.com",
    "userType": "COMMUTER" // or "DRIVER" or "ADMIN"
  },
  "user_data": {
    // For COMMUTER:
    "collegeName": "ABC College",
    "batchId": 1,
    "popId": 1,
    "adminCode": "uuid-string",
    "isComing": true
    
    // For DRIVER:
    "batchId": 1,
    "cabId": 1,
    "adminCode": "uuid-string"
    
    // For ADMIN:
    // (no additional fields needed, adminCode is auto-generated)
  }
}
```

**Response**:
- Success: `"commuter created"` or `"driver created"` or `"admin created"`
- Error: Error message with details

---

### 2. Get All Users
**Endpoint**: `GET /user/`

**Response**: Array of user objects

---

### 3. Get/Update/Delete Single User
**Endpoint**: `GET /user/<user_id>`
**Endpoint**: `PATCH /user/<user_id>`
**Endpoint**: `DELETE /user/<user_id>`

**Update Request Body** (PATCH):
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "newemail@example.com",
  "address": "New Address"
}
```

**Response**: Updated user data or `"user updated"`

---

### 4. Commuter Operations

#### Get All Commuters
**Endpoint**: `GET /user/commuter`

#### Get Single Commuter by User ID
**Endpoint**: `GET /user/commuter/<user_id>`

**Response**:
```json
{
  "id": 1,
  "userId": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "username": "John Doe",
    "mobileNumber": "1234567890"
  },
  "batchId": {
    "id": 1,
    "batchName": "Morning Batch",
    "batchTime": "08:00:00",
    "end_time": "09:00:00",
    "startDate": "2024-01-01",
    "endDate": "2024-12-31"
  },
  "popId": {
    "id": 1,
    "pickUpPointName": "Station",
    "routeId": {
      "id": 1,
      "routeName": "Route A"
    },
    "inLine": 1
  },
  "cabId": {
    "id": 1,
    "regNumber": "ABC123",
    "capacity": 4,
    "routeId": {
      "id": 1,
      "routeName": "Route A"
    },
    "km": 100
  },
  "collegeName": "ABC College",
  "isComing": true,
  "adminCode": {
    "userId": {
      "id": 2,
      "mobileNumber": "9876543210",
      "username": "Admin"
    }
  }
}
```

#### Update Commuter
**Endpoint**: `PATCH /user/commuter/<user_id>`

**Request Body**:
```json
{
  "collegeName": "New College Name",
  "batchId": 2,
  "popId": 2,
  "cabId": 2,
  "isComing": false
}
```

**Response**: `"commuter updated"`

**⚠️ Important**: To update both commuter-specific fields (collegeName, batchId, popId) AND user fields (name, mobileNumber), you need to make **2 separate API calls**:
1. `PATCH /user/<user_id>` - for user fields (first_name, last_name, mobileNumber, email, etc.)
2. `PATCH /user/commuter/<user_id>` - for commuter fields (collegeName, batchId, popId, cabId, isComing)

#### Delete Commuter
**Endpoint**: `DELETE /user/commuter/<user_id>`

**Response**: `"COMMUTER DELETED, PLEASE DETLETE THE USER AS WELL"`

---

### 5. Driver Operations

#### Get All Drivers
**Endpoint**: `GET /user/driver`

#### Get Single Driver by User ID
**Endpoint**: `GET /user/driver/<user_id>`

#### Update Driver
**Endpoint**: `PATCH /user/driver/<user_id>`

**Request Body**:
```json
{
  "batchId": 2,
  "cabId": 2,
  "adminCode": "uuid-string"
}
```

**Response**: `"driver updated"`

**⚠️ Important**: To update both driver-specific fields (batchId, cabId) AND user fields (name, mobileNumber), you need to make **2 separate API calls**:
1. `PATCH /user/<user_id>` - for user fields (first_name, last_name, mobileNumber, email, etc.)
2. `PATCH /user/driver/<user_id>` - for driver fields (batchId, cabId, adminCode)

See the Flutter example file for a helper method `updateDriverComplete()` that does both in one function call.

#### Delete Driver
**Endpoint**: `DELETE /user/driver/<user_id>`

---

### 6. Admin Operations

#### Get All Admins
**Endpoint**: `GET /user/admin`

#### Get Single Admin by User ID
**Endpoint**: `GET /user/admin/<user_id>`

#### Update Admin
**Endpoint**: `PATCH /user/admin/<user_id>`

**Response**: Updated admin data

---

### 7. Custom Admin Queries

#### Get Commuters by Admin Code
**Endpoint**: `GET /user/admin/commuter/<admin_code>`

#### Get Drivers by Admin Code
**Endpoint**: `GET /user/admin/driver/<admin_code>`

---

### 8. Get Driver by Batch
**Endpoint**: `GET /user/driver/batch/<batch_id>`

**Response**: Driver contact details for the batch

---

## Cab Services APIs

### 1. Route Operations

#### Get All Routes
**Endpoint**: `GET /cab/route`

#### Create Route
**Endpoint**: `POST /cab/route`

**Request Body**:
```json
{
  "routeName": "Route A",
  "adminCode": "uuid-string"
}
```

**Response**: `"ROUTE CREATED"` (201) or error message

#### Get Single Route
**Endpoint**: `GET /cab/route/<route_id>`

#### Update Route
**Endpoint**: `PATCH /cab/route/<route_id>`

**Request Body**:
```json
{
  "routeName": "Updated Route Name",
  "adminCode": "uuid-string"
}
```

**Response**: Updated route data

#### Delete Route
**Endpoint**: `DELETE /cab/route/<route_id>`

**Response**: `"DELETED"`

---

### 2. Batch Operations

#### Get All Batches
**Endpoint**: `GET /cab/batch`

#### Create Batch
**Endpoint**: `POST /cab/batch`

**Request Body**:
```json
{
  "batchName": "Morning Batch",
  "batchTime": "08:00:00",
  "end_time": "09:00:00",
  "startDate": "2024-01-01",
  "endDate": "2024-12-31",
  "adminCode": "uuid-string"
}
```

**Response**: `"BATCH CREATED"`

#### Get Single Batch
**Endpoint**: `GET /cab/batch/<batch_id>`

#### Update Batch
**Endpoint**: `PATCH /cab/batch/<batch_id>`

**Request Body**:
```json
{
  "batchName": "Updated Batch Name",
  "batchTime": "09:00:00",
  "end_time": "10:00:00"
}
```

**Response**: `"BATCH UPDATED"`

#### Delete Batch
**Endpoint**: `DELETE /cab/batch/<batch_id>`

**Response**: `"BATCH DELETED"`

---

### 3. Pickup Point Operations

#### Get All Pickup Points
**Endpoint**: `GET /cab/pickUpPoint`

#### Create Pickup Point
**Endpoint**: `POST /cab/pickUpPoint`

**Request Body**:
```json
{
  "pickUpPointName": "Station",
  "lat": 28.7041,
  "longitude": 77.1025,
  "routeId": 1,
  "adminCode": "uuid-string",
  "inLine": 1
}
```

**Response**: `"PICK UP POINT CREATED"` or `"PICK UP ALREADY EXSITS"`

#### Get Single Pickup Point
**Endpoint**: `GET /cab/pickUpPoint/<pickup_point_id>`

#### Update Pickup Point
**Endpoint**: `PATCH /cab/pickUpPoint/<pickup_point_id>`

**Request Body**:
```json
{
  "pickUpPointName": "Updated Station",
  "lat": 28.7041,
  "longitude": 77.1025,
  "inLine": 2
}
```

**Response**: `"PICK UP POINT UPDATED"`

#### Delete Pickup Point
**Endpoint**: `DELETE /cab/pickUpPoint/<pickup_point_id>`

**Response**: `"DATA DELETED"`

---

### 4. Cab Operations

#### Get All Cabs
**Endpoint**: `GET /cab/cab`

#### Create Cab
**Endpoint**: `POST /cab/cab`

**Request Body**:
```json
{
  "regNumber": "ABC123",
  "capacity": 4,
  "km": 100,
  "adminCode": "uuid-string",
  "routeId": 1
}
```

**Response**: `"CAB CREATED"`

#### Get Single Cab
**Endpoint**: `GET /cab/cab/<cab_id>`

#### Update Cab
**Endpoint**: `PATCH /cab/cab/<cab_id>`

**Request Body**:
```json
{
  "regNumber": "XYZ789",
  "capacity": 6,
  "km": 150,
  "routeId": 2
}
```

**Response**: `"CAB UPDATED"`

#### Delete Cab
**Endpoint**: `DELETE /cab/cab/<cab_id>`

**Response**: `"CAB DELETED"`

---

### 5. Custom Admin Queries (Cab Services)

#### Get Cabs by Admin Code
**Endpoint**: `GET /cab/admin/cab/<admin_code>`

#### Get Routes by Admin Code
**Endpoint**: `GET /cab/admin/route/<admin_code>`

#### Get Batches by Admin Code
**Endpoint**: `GET /cab/admin/batch/<admin_code>`

#### Get Pickup Points by Admin Code
**Endpoint**: `GET /cab/admin/pickuppoint/<admin_code>`

---

## D2D Log APIs

### 1. Get Running Batches
**Endpoint**: `GET /d2d/running_batches/<admin_code>`

**Response**: Array of active D2D logs for today
```json
[
  {
    "id": 1,
    "batchId": {
      "id": 1,
      "batchName": "Morning Batch"
    }
  }
]
```

---

### 2. Get Return Trip Commuters
**Endpoint**: `GET /d2d/return_batch/view/<batch_id>`

**Response**: Array of commuters with `isComing: true`
```json
[
  {
    "userId": {
      "id": 1,
      "mobileNumber": "1234567890",
      "username": "John Doe"
    },
    "popId": {
      "inLine": 1,
      "pickUpPointName": "Station",
      "routeId": {
        "routeName": "Route A"
      }
    }
  }
]
```

---

### 3. Get Cache Data (Current Commuters in Return Trip)
**Endpoint**: `GET /d2d/return_batch/get_commuter/<batch_id>`

**Response**:
```json
{
  "commuter_list": [1, 2, 3],
  "total_capacity": 4,
  "current_capacity": 1
}
```

---

### 4. Add Commuter to Return Trip
**Endpoint**: `POST /d2d/return_batch/add_commuter`

**Request Body**:
```json
{
  "batch_id": "1",
  "commuter_id": "1"
}
```

**Response**:
- Success (201): `"commuter added"`
- Out of capacity (204): `"out of capcaity"`
- Invalid data (400): `"Invalid Data"`

---

### 5. Remove Commuter from Return Trip
**Endpoint**: `POST /d2d/return_batch/remove_commuter`

**Request Body**:
```json
{
  "batch_id": "1",
  "commuter_id": "1"
}
```

**Response**: `"commuter removed"` (200)

---

### 6. Clear Cache Data (End Return Trip)
**Endpoint**: `GET /d2d/return_batch/end/<batch_id>`

**Response**: `{}` (200)

---

### 7. Check D2D Log Status
**Endpoint**: `GET /d2d/get_d2d_log_status/<batch_id>`

**Response**:
- `"2"` - Trip in progress (endTime is null)
- `"3"` - Trip completed (endTime is set)

---

## Common Update Operations

### How to Update Data in Flutter

All update operations use **PATCH** method with partial data. You only need to send the fields you want to update.

#### Example 1: Update User Profile
```dart
// Flutter example
final response = await http.patch(
  Uri.parse('http://your-domain.com/user/1'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'newemail@example.com',
  }),
);
```

#### Example 2: Update Commuter Details
```dart
final response = await http.patch(
  Uri.parse('http://your-domain.com/user/commuter/1'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'collegeName': 'New College',
    'isComing': false,
  }),
);
```

#### Example 3: Update Cab Details
```dart
final response = await http.patch(
  Uri.parse('http://your-domain.com/cab/cab/1'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'capacity': 6,
    'km': 200,
  }),
);
```

#### Example 4: Update Batch Time
```dart
final response = await http.patch(
  Uri.parse('http://your-domain.com/cab/batch/1'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'batchTime': '09:00:00',
    'end_time': '10:00:00',
  }),
);
```

---

## Flutter Integration Examples

### Complete Flutter Service Class Example

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = 'http://your-domain.com';
  
  // Login
  Future<Map<String, dynamic>?> login(String mobileNumber, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/user/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'mobileNumber': mobileNumber,
          'password': password,
        }),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Login error: $e');
      return null;
    }
  }
  
  // Update User
  Future<bool> updateUser(int userId, Map<String, dynamic> data) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/user/$userId'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      print('Update user error: $e');
      return false;
    }
  }
  
  // Update Commuter
  Future<bool> updateCommuter(int userId, Map<String, dynamic> data) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/user/commuter/$userId'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      print('Update commuter error: $e');
      return false;
    }
  }
  
  // Update Cab
  Future<bool> updateCab(int cabId, Map<String, dynamic> data) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/cab/cab/$cabId'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      print('Update cab error: $e');
      return false;
    }
  }
  
  // Get Commuter Details
  Future<Map<String, dynamic>?> getCommuter(int userId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/user/commuter/$userId'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Get commuter error: $e');
      return null;
    }
  }
  
  // Add Commuter to Return Trip
  Future<String> addCommuterToReturnTrip(String batchId, String commuterId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/d2d/return_batch/add_commuter'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'batch_id': batchId,
          'commuter_id': commuterId,
        }),
      );
      
      if (response.statusCode == 201) {
        return 'success';
      } else if (response.statusCode == 204) {
        return 'out_of_capacity';
      }
      return 'error';
    } catch (e) {
      print('Add commuter error: $e');
      return 'error';
    }
  }
  
  // Get Running Batches
  Future<List<dynamic>?> getRunningBatches(String adminCode) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/d2d/running_batches/$adminCode'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Get running batches error: $e');
      return null;
    }
  }
}
```

### Usage in Flutter Widget

```dart
class UpdateProfileScreen extends StatefulWidget {
  @override
  _UpdateProfileScreenState createState() => _UpdateProfileScreenState();
}

class _UpdateProfileScreenState extends State<UpdateProfileScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _nameController = TextEditingController();
  
  Future<void> _updateProfile() async {
    final success = await _apiService.updateUser(
      1, // user ID
      {
        'first_name': _nameController.text,
        'email': 'newemail@example.com',
      },
    );
    
    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Profile updated successfully!')),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to update profile')),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Update Profile')),
      body: Column(
        children: [
          TextField(
            controller: _nameController,
            decoration: InputDecoration(labelText: 'Name'),
          ),
          ElevatedButton(
            onPressed: _updateProfile,
            child: Text('Update'),
          ),
        ],
      ),
    );
  }
}
```

---

## Important Notes

1. **Partial Updates**: All PATCH requests support partial updates - you only need to send the fields you want to change.

2. **Foreign Keys**: When updating foreign key fields (like `batchId`, `cabId`, `routeId`), send the ID as an integer.

3. **Admin Code**: Admin codes are UUIDs (strings), not integers.

4. **Date/Time Formats**:
   - Date: `"YYYY-MM-DD"` (e.g., `"2024-01-15"`)
   - Time: `"HH:MM:SS"` (e.g., `"08:00:00"`)

5. **Error Handling**: Always check response status codes:
   - `200` - Success
   - `201` - Created
   - `204` - No Content (sometimes used for errors)
   - `400` - Bad Request (validation errors)
   - `404` - Not Found

6. **Response Messages**: Most endpoints return simple string messages like `"user updated"` or `"CAB UPDATED"` on success.

7. **Authentication**: Currently, the login endpoint uses session-based authentication. You may need to handle cookies or implement token-based auth if required.

---

## Quick Reference: Update Endpoints

| Resource | Update Endpoint | Method |
|----------|----------------|--------|
| User | `/user/<user_id>` | PATCH |
| Commuter | `/user/commuter/<user_id>` | PATCH |
| Driver | `/user/driver/<user_id>` | PATCH |
| Admin | `/user/admin/<user_id>` | PATCH |
| Route | `/cab/route/<route_id>` | PATCH |
| Batch | `/cab/batch/<batch_id>` | PATCH |
| Pickup Point | `/cab/pickUpPoint/<pickup_point_id>` | PATCH |
| Cab | `/cab/cab/<cab_id>` | PATCH |

---

## Need Help?

If you need to add new endpoints or modify existing ones, the main files to check are:
- `views.py` in each app folder
- `urls.py` in each app folder
- `serializers.py` for request/response format
- `models.py` for data structure

Good luck with your Flutter integration! 🚀

