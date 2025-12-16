# Driver Repository Code Review & Improvements

## 🔍 Issues Found

### 1. **Missing Driver-Specific Update**
Your current `updateDriver` method only updates **User fields** (name, mobileNumber, etc.), but doesn't update **Driver-specific fields** (batchId, cabId, adminCode).

### 2. **Response Handling**
The backend returns simple strings like `"driver updated"` or `"user updated"`, not JSON objects. Your current check `if (response is Map)` might fail.

### 3. **Need Combined Update Method**
You need a way to update both user and driver data together.

---

## ✅ Improved Code

Here's the corrected and improved version:

```dart
import 'package:cts/api/api_exceptions_handler.dart';
import 'package:cts/api/api_list.dart';
import 'package:cts/api/api_result.dart';
import 'package:cts/appManager/appClass.dart';
import 'package:cts/api/base_api_services.dart';
import 'package:cts/domain/repositories/driver_repository.dart';
import 'package:cts/models/driverModel.dart';

class DriverRepositoryImpl implements DriverRepository {
  final BaseApiServices _apiService;

  DriverRepositoryImpl({required BaseApiServices apiService})
      : _apiService = apiService;

  @override
  Future<ApiResult<List<DriverModel>>> getDrivers() async {
    try {
      final adminCode = AppManager.instance.getString(ManagerKey.adminCode);
      final response = await _apiService.getApi("${ApiUrl.adminDriverUrl}$adminCode");

      if (response is List<dynamic>) {
        final drivers = response
            .map((json) => DriverModel.fromJson(Map<String, dynamic>.from(json)))
            .toList();
        return ApiResult.success(drivers);
      } else {
        return ApiResult.failure(ApiExceptionHandler.handle('Invalid response format'));
      }
    } catch (e) {
      return ApiResult.failure(ApiExceptionHandler.handle(e));
    }
  }

  @override
  Future<ApiResult<DriverModel>> getDriverProfile() async {
    try {
      final userId = AppManager.instance.getString(ManagerKey.userId);
      final response = await _apiService.getApi("${ApiUrl.driverUrl}/$userId");
      final driver = DriverModel.fromJson(response);
      return ApiResult.success(driver);
    } catch (e) {
      return ApiResult.failure(ApiExceptionHandler.handle(e));
    }
  }

  @override
  Future<ApiResult<void>> createDriver(Map<String, dynamic> data) async {
    print("createDriver\n");
    print("${ApiUrl.userUrl}\n");
    print("$data\n");
    try {
      final response = await _apiService.postApi(data, ApiUrl.postUserUrl);
      print("response\n");
      print(response);
      print("\n");
      
      // Backend returns string like "driver created", not JSON
      if (response != null) {
        return ApiResult.success(null);
      } else {
        return ApiResult.failure(ApiFailure(
            type: ApiFailureType.parsing,
            message: response?.toString() ?? "Create Driver failed."));
      }
    } catch (e) {
      return ApiResult.failure(ApiExceptionHandler.handle(e));
    }
  }

  // ============================================
  // UPDATED METHODS
  // ============================================

  /// Update user fields (name, mobileNumber, email, etc.)
  /// This updates the User model
  @override
  Future<ApiResult<void>> updateDriver(int id, Map<String, dynamic> data) async {
    try {
      final response = await _apiService.patchApi(id, data, ApiUrl.userUrl);
      print("updateDriver (user) response: $response\n");

      // Backend returns string like "user updated", not JSON
      if (response != null && response.toString().toLowerCase().contains("updated")) {
        return ApiResult.success(null);
      } else {
        return ApiResult.failure(ApiFailure(
            type: ApiFailureType.parsing,
            message: response?.toString() ?? "Update Driver (user) failed."));
      }
    } catch (e) {
      return ApiResult.failure(ApiExceptionHandler.handle(e));
    }
  }

  /// Update driver-specific fields (batchId, cabId, adminCode)
  /// This updates the Driver model
  /// You need to add this method to your DriverRepository interface
  Future<ApiResult<void>> updateDriverFields(int id, Map<String, dynamic> data) async {
    try {
      // Assuming you have ApiUrl.driverUrl = "/user/driver"
      final driverUrl = "${ApiUrl.driverUrl}/$id"; // or ApiUrl.driverUrl if it already includes the path
      final response = await _apiService.patchApi(id, data, driverUrl);
      print("updateDriverFields response: $response\n");

      // Backend returns string like "driver updated"
      if (response != null && response.toString().toLowerCase().contains("updated")) {
        return ApiResult.success(null);
      } else {
        return ApiResult.failure(ApiFailure(
            type: ApiFailureType.parsing,
            message: response?.toString() ?? "Update Driver fields failed."));
      }
    } catch (e) {
      return ApiResult.failure(ApiExceptionHandler.handle(e));
    }
  }

  /// Update both user and driver fields in one call
  /// userData: {"first_name": "John", "mobileNumber": "1234567890"}
  /// driverData: {"batchId": 2, "cabId": 3}
  Future<ApiResult<void>> updateDriverComplete(
    int id,
    Map<String, dynamic>? userData,
    Map<String, dynamic>? driverData,
  ) async {
    try {
      bool userSuccess = true;
      bool driverSuccess = true;
      String? errorMessage;

      // Update user fields if provided
      if (userData != null && userData.isNotEmpty) {
        final userResult = await updateDriver(id, userData);
        if (userResult is ApiFailure) {
          userSuccess = false;
          errorMessage = userResult.message;
        }
      }

      // Update driver fields if provided
      if (driverData != null && driverData.isNotEmpty) {
        final driverResult = await updateDriverFields(id, driverData);
        if (driverResult is ApiFailure) {
          driverSuccess = false;
          errorMessage = errorMessage != null 
              ? "$errorMessage; ${driverResult.message}" 
              : driverResult.message;
        }
      }

      if (userSuccess && driverSuccess) {
        return ApiResult.success(null);
      } else {
        return ApiResult.failure(ApiFailure(
            type: ApiFailureType.server,
            message: errorMessage ?? "Update Driver failed."));
      }
    } catch (e) {
      return ApiResult.failure(ApiExceptionHandler.handle(e));
    }
  }

  @override
  Future<ApiResult<void>> deleteDriver(int id) async {
    try {
      final response = await _apiService.deleteApi(id, ApiUrl.userUrl);
      print("deleteDriver response: $response\n");

      if (response != null && response.toString().toUpperCase().contains("DELETED")) {
        return ApiResult.success(null);
      } else {
        return ApiResult.failure(ApiFailure(
            type: ApiFailureType.parsing,
            message: response?.toString() ?? "Delete Driver failed."));
      }
    } catch (e) {
      return ApiResult.failure(ApiExceptionHandler.handle(e));
    }
  }
}
```

---

## 📝 Required Changes

### 1. **Add to ApiUrl (api_list.dart)**
Make sure you have:
```dart
class ApiUrl {
  static const String userUrl = "/user";
  static const String driverUrl = "/user/driver";  // Add this if not present
  static const String adminDriverUrl = "/user/admin/driver/";
  // ... other URLs
}
```

### 2. **Update DriverRepository Interface**
Add the new method to your interface:
```dart
abstract class DriverRepository {
  // ... existing methods
  
  Future<ApiResult<void>> updateDriver(int id, Map<String, dynamic> data);
  Future<ApiResult<void>> updateDriverFields(int id, Map<String, dynamic> data); // NEW
  Future<ApiResult<void>> updateDriverComplete(
    int id,
    Map<String, dynamic>? userData,
    Map<String, dynamic>? driverData,
  ); // NEW
  Future<ApiResult<void>> deleteDriver(int id);
}
```

### 3. **Check BaseApiServices.patchApi Method**
Make sure it accepts a full URL path. If it only accepts a base URL, you might need to adjust:
```dart
// Option 1: If patchApi builds URL from base + id
final response = await _apiService.patchApi(id, data, ApiUrl.driverUrl);

// Option 2: If patchApi needs full path
final response = await _apiService.patchApi(id, data, "${ApiUrl.driverUrl}/$id");
```

---

## 🎯 Usage Examples

### Update Only User Fields:
```dart
final result = await driverRepository.updateDriver(userId, {
  'first_name': 'John',
  'mobileNumber': '1234567890',
});
```

### Update Only Driver Fields:
```dart
final result = await driverRepository.updateDriverFields(userId, {
  'batchId': 2,
  'cabId': 3,
});
```

### Update Both (Recommended):
```dart
final result = await driverRepository.updateDriverComplete(
  userId,
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
```

---

## ⚠️ Important Notes

1. **Response Format**: Backend returns strings like `"driver updated"`, not JSON. Check for keywords like "updated" or "DELETED" instead of expecting JSON.

2. **URL Structure**: Make sure your `ApiUrl.driverUrl` is `/user/driver` (without trailing slash for the base, or with `/$id` if it includes the ID).

3. **Error Handling**: The improved code handles both user and driver update failures separately and combines error messages.

4. **Null Safety**: The `updateDriverComplete` method allows updating only user or only driver by passing `null` for the other.

---

## 🔧 If Your BaseApiServices.patchApi Works Differently

If your `patchApi` method signature is different, adjust accordingly:

```dart
// If it's: patchApi(String url, Map<String, dynamic> data)
final response = await _apiService.patchApi(
  "${ApiUrl.driverUrl}/$id",
  data,
);

// If it's: patchApi(int id, Map<String, dynamic> data, String baseUrl)
final response = await _apiService.patchApi(
  id,
  data,
  ApiUrl.driverUrl, // Make sure this is "/user/driver"
);
```

---

## ✅ Summary of Changes

1. ✅ Fixed response handling (check for strings, not just Maps)
2. ✅ Added `updateDriverFields()` method for driver-specific updates
3. ✅ Added `updateDriverComplete()` method for combined updates
4. ✅ Improved error handling and messages
5. ✅ Added better logging

Your code should now properly handle both user and driver updates! 🚀



