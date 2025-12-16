# Driver Update Format - Correct Implementation

## 🔍 Issues in Your Current Code

1. ❌ **Mixing user and driver fields** in one API call
2. ❌ **Using "first"** instead of **"first_name"**
3. ❌ **Not splitting name** into `first_name` and `last_name`
4. ❌ **Including driver fields** (batchId, cabId) in user update call

---

## ✅ Correct Format

You need **TWO separate API calls** or use the combined method:

### Option 1: Two Separate Calls (Current Approach)

#### Call 1: Update User Fields
**Endpoint**: `PATCH /user/<user_id>`

**Request Body Format**:
```dart
{
  "first_name": "John",           // ✅ Use first_name, not "first"
  "last_name": "Doe",             // ✅ Split the name
  "mobileNumber": "1234567890",
  "username": "John Doe",         // Optional
  "address": "123 Main St",       // Optional
  "email": "john@example.com"     // Optional
  // ❌ DO NOT include: userType, batchId, cabId, adminCode
}
```

#### Call 2: Update Driver Fields
**Endpoint**: `PATCH /user/driver/<user_id>`

**Request Body Format**:
```dart
{
  "batchId": 2,                   // Integer
  "cabId": 3,                     // Integer
  "adminCode": "uuid-string"      // UUID string (optional if not changing)
  // ❌ DO NOT include: first_name, mobileNumber, username, etc.
}
```

---

## 🔧 Corrected Driver Form Code

Here's your corrected `DriverForm` widget:

```dart
// In your onPressed handler, replace the update section:

if (formProvider.forUpdate) {
  // Split name into first_name and last_name
  final nameParts = formProvider.driverNameCtrl.text.trim().split(' ');
  final firstName = nameParts.isNotEmpty ? nameParts[0].toUpperCase() : '';
  final lastName = nameParts.length > 1 
      ? nameParts.sublist(1).join(' ').toUpperCase() 
      : '';

  // Prepare user data (for PATCH /user/<id>)
  final userData = {
    "first_name": firstName,
    "last_name": lastName,
    "mobileNumber": formProvider.driverMobileCtrl.text.trim(),
    "username": formProvider.driverNameCtrl.text.trim().toUpperCase(),
    if (formProvider.driverAddressCtrl.text.trim().isNotEmpty)
      "address": formProvider.driverAddressCtrl.text.trim().toUpperCase(),
  };

  // Prepare driver data (for PATCH /user/driver/<id>)
  final driverData = {
    "batchId": formProvider.selectedBatchId,
    "cabId": formProvider.selectedCabId,
    "adminCode": AppManager.instance.getString(ManagerKey.adminCode),
  };

  // Option A: Update both separately
  final userSuccess = await _driverProvider.updateDriver(
    formProvider.updateId, 
    userData
  );
  
  final driverSuccess = await _driverProvider.updateDriverFields(
    formProvider.updateId, 
    driverData
  );
  
  success = userSuccess.isSuccess && driverSuccess.isSuccess;

  // Option B: Use combined method (if you implement it)
  // final result = await _driverProvider.updateDriverComplete(
  //   formProvider.updateId,
  //   userData,
  //   driverData,
  // );
  // success = result.isSuccess;
}
```

---

## 📋 Complete Field Reference

### User Fields (PATCH /user/<user_id>)
```dart
{
  "first_name": "John",        // ✅ Required (use this, not "first")
  "last_name": "Doe",          // ✅ Required
  "mobileNumber": "1234567890", // ✅ Required
  "username": "John Doe",      // Optional
  "email": "john@example.com", // Optional
  "address": "123 Main St"    // Optional
}
```

### Driver Fields (PATCH /user/driver/<user_id>)
```dart
{
  "batchId": 2,               // Integer - Optional
  "cabId": 3,                 // Integer - Optional
  "adminCode": "uuid-string"  // UUID string - Optional
}
```

---

## 🎯 Updated Repository Methods

Add these methods to your `DriverRepositoryImpl`:

```dart
/// Update user fields only
@override
Future<ApiResult<void>> updateDriver(int id, Map<String, dynamic> data) async {
  try {
    final response = await _apiService.patchApi(id, data, ApiUrl.userUrl);
    
    if (response != null && 
        response.toString().toLowerCase().contains("updated")) {
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

/// Update driver-specific fields only
Future<ApiResult<void>> updateDriverFields(
  int id, 
  Map<String, dynamic> data
) async {
  try {
    // Make sure ApiUrl.driverUrl = "/user/driver"
    final response = await _apiService.patchApi(id, data, ApiUrl.driverUrl);
    
    if (response != null && 
        response.toString().toLowerCase().contains("updated")) {
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

/// Update both user and driver in one call
Future<ApiResult<void>> updateDriverComplete(
  int id,
  Map<String, dynamic>? userData,
  Map<String, dynamic>? driverData,
) async {
  try {
    bool userSuccess = true;
    bool driverSuccess = true;
    String? errorMessage;

    // Update user if data provided
    if (userData != null && userData.isNotEmpty) {
      final userResult = await updateDriver(id, userData);
      if (userResult is ApiFailure) {
        userSuccess = false;
        errorMessage = userResult.message;
      }
    }

    // Update driver if data provided
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
```

---

## 🔄 Updated DriverProvider Method

In your `DriverController` or `DriverProvider`, add:

```dart
// Add this method
Future<ApiResult<void>> updateDriverFields(int id, Map<String, dynamic> data) async {
  return await _driverRepository.updateDriverFields(id, data);
}

// Update existing method or add new one
Future<bool> updateDriverComplete(
  int id,
  Map<String, dynamic>? userData,
  Map<String, dynamic>? driverData,
) async {
  final result = await _driverRepository.updateDriverComplete(
    id,
    userData,
    driverData,
  );
  
  if (result.isSuccess) {
    // Show success message
    SnackbarService.showSuccess("Driver updated successfully");
    return true;
  } else {
    // Show error message
    SnackbarService.showError(result.error?.message ?? "Failed to update driver");
    return false;
  }
}
```

---

## ✅ Final Corrected Form Code

```dart
CommonPrimaryButton(
  label: formProvider.forUpdate ? "Update Driver" : "Create Driver",
  onPressed: () async {
    if (_formKey.currentState!.validate()) {
      bool success = false;

      if (formProvider.forUpdate) {
        // Split name
        final nameParts = formProvider.driverNameCtrl.text.trim().split(' ');
        final firstName = nameParts.isNotEmpty ? nameParts[0].toUpperCase() : '';
        final lastName = nameParts.length > 1 
            ? nameParts.sublist(1).join(' ').toUpperCase() 
            : '';

        // User data
        final userData = {
          "first_name": firstName,
          "last_name": lastName,
          "mobileNumber": formProvider.driverMobileCtrl.text.trim(),
          "username": formProvider.driverNameCtrl.text.trim().toUpperCase(),
          if (formProvider.driverAddressCtrl.text.trim().isNotEmpty)
            "address": formProvider.driverAddressCtrl.text.trim().toUpperCase(),
        };

        // Driver data
        final driverData = {
          "batchId": formProvider.selectedBatchId,
          "cabId": formProvider.selectedCabId,
          "adminCode": AppManager.instance.getString(ManagerKey.adminCode),
        };

        // Use combined method (recommended)
        success = await _driverProvider.updateDriverComplete(
          formProvider.updateId,
          userData,
          driverData,
        );

        // OR use separate calls
        // final userResult = await _driverProvider.updateDriver(
        //   formProvider.updateId, 
        //   userData
        // );
        // final driverResult = await _driverProvider.updateDriverFields(
        //   formProvider.updateId, 
        //   driverData
        // );
        // success = userResult.isSuccess && driverResult.isSuccess;

      } else {
        // Create driver (your existing code is fine)
        final data = {
          "user": {
            "username": formProvider.driverNameCtrl.text.trim().toUpperCase(),
            "password": formProvider.driverPasswordCtrl.text.trim(),
            "first": formProvider.driverNameCtrl.text.trim().toUpperCase(),
            "mobileNumber": formProvider.driverMobileCtrl.text.trim(),
            'userType': "DRIVER",
          },
          "user_data": {
            "cabId": formProvider.selectedCabId,
            "adminCode": AppManager.instance.getString(ManagerKey.adminCode),
            "batchId": formProvider.selectedBatchId,
            'address': formProvider.driverAddressCtrl.text.trim().toUpperCase(),
          }
        };
        success = await _driverProvider.createDriver(data);
      }

      if (success) {
        Navigator.pop(context);
      }
    }
  },
  backgroundColor: AppColors.acBlack,
  textColor: Colors.white,
),
```

---

## 📝 Key Changes Summary

1. ✅ **Split name**: Use `first_name` and `last_name` instead of `"first"`
2. ✅ **Separate calls**: User fields → `/user/<id>`, Driver fields → `/user/driver/<id>`
3. ✅ **Remove userType**: Don't include `userType` in update (it's set during creation)
4. ✅ **Correct field names**: Use `first_name` not `"first"`

---

## 🎯 Quick Reference

| Field | User Update | Driver Update | Notes |
|-------|-------------|---------------|-------|
| `first_name` | ✅ | ❌ | Required |
| `last_name` | ✅ | ❌ | Required |
| `mobileNumber` | ✅ | ❌ | Required |
| `username` | ✅ | ❌ | Optional |
| `address` | ✅ | ❌ | Optional |
| `batchId` | ❌ | ✅ | Integer |
| `cabId` | ❌ | ✅ | Integer |
| `adminCode` | ❌ | ✅ | UUID string |
| `userType` | ❌ | ❌ | Don't update |

---

This should fix your driver update functionality! 🚀



