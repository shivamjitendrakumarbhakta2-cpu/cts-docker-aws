// Flutter API Service Example
// Add this to your Flutter project and customize as needed

import 'dart:convert';
import 'package:http/http.dart' as http;

class BackendApiService {
  // Update this with your actual backend URL
  final String baseUrl = 'http://localhost:8000'; // or your deployed URL
  
  // ============================================
  // AUTHENTICATION
  // ============================================
  
  /// Login user
  /// Returns: {"user_id": 1, "user_type": "COMMUTER"} or null on error
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
  
  /// Logout user
  Future<bool> logout() async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/user/logout'),
      );
      return response.statusCode == 200;
    } catch (e) {
      print('Logout error: $e');
      return false;
    }
  }
  
  // ============================================
  // USER OPERATIONS
  // ============================================
  
  /// Get user details by ID
  Future<Map<String, dynamic>?> getUser(int userId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/user/$userId'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Get user error: $e');
      return null;
    }
  }
  
  /// Update user profile
  /// data: {"first_name": "John", "last_name": "Doe", "email": "new@email.com"}
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
  
  // ============================================
  // COMMUTER OPERATIONS
  // ============================================
  
  /// Get commuter details by user ID
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
  
  /// Update commuter details
  /// data: {"collegeName": "New College", "isComing": false, "batchId": 2, "popId": 1}
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
  
  /// Update both user and commuter in one call
  /// userData: {"first_name": "John", "mobileNumber": "1234567890"}
  /// commuterData: {"collegeName": "New College", "batchId": 2}
  /// Returns: true if both updates succeed, false otherwise
  Future<bool> updateCommuterComplete(
    int userId, 
    Map<String, dynamic>? userData, 
    Map<String, dynamic>? commuterData
  ) async {
    bool userSuccess = true;
    bool commuterSuccess = true;
    
    // Update user if data provided
    if (userData != null && userData.isNotEmpty) {
      userSuccess = await updateUser(userId, userData);
    }
    
    // Update commuter if data provided
    if (commuterData != null && commuterData.isNotEmpty) {
      commuterSuccess = await updateCommuter(userId, commuterData);
    }
    
    return userSuccess && commuterSuccess;
  }
  
  // ============================================
  // DRIVER OPERATIONS
  // ============================================
  
  /// Get driver details by user ID
  Future<Map<String, dynamic>?> getDriver(int userId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/user/driver/$userId'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Get driver error: $e');
      return null;
    }
  }
  
  /// Update driver details
  /// data: {"batchId": 2, "cabId": 3}
  Future<bool> updateDriver(int userId, Map<String, dynamic> data) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/user/driver/$userId'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      print('Update driver error: $e');
      return false;
    }
  }
  
  /// Update both user and driver in one call
  /// userData: {"first_name": "John", "mobileNumber": "1234567890"}
  /// driverData: {"batchId": 2, "cabId": 3}
  /// Returns: true if both updates succeed, false otherwise
  Future<bool> updateDriverComplete(
    int userId, 
    Map<String, dynamic>? userData, 
    Map<String, dynamic>? driverData
  ) async {
    bool userSuccess = true;
    bool driverSuccess = true;
    
    // Update user if data provided
    if (userData != null && userData.isNotEmpty) {
      userSuccess = await updateUser(userId, userData);
    }
    
    // Update driver if data provided
    if (driverData != null && driverData.isNotEmpty) {
      driverSuccess = await updateDriver(userId, driverData);
    }
    
    return userSuccess && driverSuccess;
  }
  
  // ============================================
  // CAB OPERATIONS
  // ============================================
  
  /// Get all cabs
  Future<List<dynamic>?> getAllCabs() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/cab/cab'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Get all cabs error: $e');
      return null;
    }
  }
  
  /// Get single cab by ID
  Future<Map<String, dynamic>?> getCab(int cabId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/cab/cab/$cabId'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Get cab error: $e');
      return null;
    }
  }
  
  /// Update cab details
  /// data: {"capacity": 6, "km": 200, "routeId": 2}
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
  
  // ============================================
  // BATCH OPERATIONS
  // ============================================
  
  /// Get all batches
  Future<List<dynamic>?> getAllBatches() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/cab/batch'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Get all batches error: $e');
      return null;
    }
  }
  
  /// Update batch
  /// data: {"batchTime": "09:00:00", "end_time": "10:00:00", "batchName": "New Name"}
  Future<bool> updateBatch(int batchId, Map<String, dynamic> data) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/cab/batch/$batchId'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      print('Update batch error: $e');
      return false;
    }
  }
  
  // ============================================
  // ROUTE OPERATIONS
  // ============================================
  
  /// Get all routes
  Future<List<dynamic>?> getAllRoutes() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/cab/route'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Get all routes error: $e');
      return null;
    }
  }
  
  /// Update route
  /// data: {"routeName": "New Route Name"}
  Future<bool> updateRoute(int routeId, Map<String, dynamic> data) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/cab/route/$routeId'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      print('Update route error: $e');
      return false;
    }
  }
  
  // ============================================
  // PICKUP POINT OPERATIONS
  // ============================================
  
  /// Update pickup point
  /// data: {"pickUpPointName": "New Station", "lat": 28.7, "longitude": 77.1, "inLine": 2}
  Future<bool> updatePickupPoint(int pickupPointId, Map<String, dynamic> data) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/cab/pickUpPoint/$pickupPointId'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      print('Update pickup point error: $e');
      return false;
    }
  }
  
  // ============================================
  // D2D LOG OPERATIONS
  // ============================================
  
  /// Get running batches for today
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
  
  /// Get return trip commuters
  Future<List<dynamic>?> getReturnTripCommuters(String batchId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/d2d/return_batch/view/$batchId'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Get return trip commuters error: $e');
      return null;
    }
  }
  
  /// Get cache data (current capacity)
  Future<Map<String, dynamic>?> getCacheData(String batchId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/d2d/return_batch/get_commuter/$batchId'),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Get cache data error: $e');
      return null;
    }
  }
  
  /// Add commuter to return trip
  /// Returns: 'success', 'out_of_capacity', or 'error'
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
      print('Add commuter to return trip error: $e');
      return 'error';
    }
  }
  
  /// Remove commuter from return trip
  Future<bool> removeCommuterFromReturnTrip(String batchId, String commuterId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/d2d/return_batch/remove_commuter'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'batch_id': batchId,
          'commuter_id': commuterId,
        }),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      print('Remove commuter from return trip error: $e');
      return false;
    }
  }
  
  /// Check D2D log status
  /// Returns: "2" (in progress) or "3" (completed)
  Future<String?> getD2dLogStatus(String batchId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/d2d/get_d2d_log_status/$batchId'),
      );
      
      if (response.statusCode == 200) {
        return response.body;
      }
      return null;
    } catch (e) {
      print('Get D2D log status error: $e');
      return null;
    }
  }
  
  /// Clear cache data (end return trip)
  Future<bool> clearCacheData(String batchId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/d2d/return_batch/end/$batchId'),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      print('Clear cache data error: $e');
      return false;
    }
  }
}

// ============================================
// USAGE EXAMPLE
// ============================================

/*
// Example usage in a Flutter widget:

class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  final BackendApiService _api = BackendApiService();
  
  Future<void> updateUserProfile() async {
    final success = await _api.updateUser(1, {
      'first_name': 'John',
      'last_name': 'Doe',
      'email': 'john@example.com',
    });
    
    if (success) {
      print('User updated successfully!');
    } else {
      print('Failed to update user');
    }
  }
  
  Future<void> updateCommuterStatus() async {
    final success = await _api.updateCommuter(1, {
      'isComing': false,
      'collegeName': 'New College Name',
    });
    
    if (success) {
      print('Commuter updated successfully!');
    }
  }
  
  Future<void> addToReturnTrip() async {
    final result = await _api.addCommuterToReturnTrip('1', '1');
    
    if (result == 'success') {
      print('Commuter added to return trip!');
    } else if (result == 'out_of_capacity') {
      print('Cab is full!');
    } else {
      print('Error adding commuter');
    }
  }
  
  // Example: Update driver with both user and driver data
  Future<void> updateDriverComplete() async {
    final success = await _api.updateDriverComplete(
      1, // user ID
      {
        // User fields
        'first_name': 'John',
        'last_name': 'Doe',
        'mobileNumber': '1234567890',
      },
      {
        // Driver fields
        'batchId': 2,
        'cabId': 3,
      },
    );
    
    if (success) {
      print('Driver updated successfully (both user and driver data)!');
    } else {
      print('Failed to update driver');
    }
  }
  
  // Example: Update commuter with both user and commuter data
  Future<void> updateCommuterComplete() async {
    final success = await _api.updateCommuterComplete(
      1, // user ID
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
      print('Commuter updated successfully (both user and commuter data)!');
    } else {
      print('Failed to update commuter');
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          ElevatedButton(
            onPressed: updateUserProfile,
            child: Text('Update Profile'),
          ),
          ElevatedButton(
            onPressed: updateCommuterStatus,
            child: Text('Update Commuter'),
          ),
          ElevatedButton(
            onPressed: updateDriverComplete,
            child: Text('Update Driver (Complete)'),
          ),
          ElevatedButton(
            onPressed: updateCommuterComplete,
            child: Text('Update Commuter (Complete)'),
          ),
          ElevatedButton(
            onPressed: addToReturnTrip,
            child: Text('Add to Return Trip'),
          ),
        ],
      ),
    );
  }
}
*/

