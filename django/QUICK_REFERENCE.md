# Quick API Reference Guide

## 🔑 Authentication
```
POST /user/login
Body: {"mobileNumber": "1234567890", "password": "password"}
Response: {"user_id": 1, "user_type": "COMMUTER"}
```

## 📝 Common Update Operations

### Update User Profile
```
PATCH /user/<user_id>
Body: {"first_name": "John", "email": "new@email.com"}
```

### Update Commuter
```
PATCH /user/commuter/<user_id>
Body: {"collegeName": "New College", "isComing": false, "batchId": 2}
```

### Update Driver
```
PATCH /user/driver/<user_id>
Body: {"batchId": 2, "cabId": 3}
```

### Update Cab
```
PATCH /cab/cab/<cab_id>
Body: {"capacity": 6, "km": 200, "routeId": 2}
```

### Update Batch
```
PATCH /cab/batch/<batch_id>
Body: {"batchTime": "09:00:00", "end_time": "10:00:00"}
```

### Update Route
```
PATCH /cab/route/<route_id>
Body: {"routeName": "New Route Name"}
```

### Update Pickup Point
```
PATCH /cab/pickUpPoint/<pickup_point_id>
Body: {"pickUpPointName": "New Station", "lat": 28.7, "longitude": 77.1}
```

## 📊 Get Data

### Get User Details
```
GET /user/<user_id>
```

### Get Commuter Details
```
GET /user/commuter/<user_id>
```

### Get Driver Details
```
GET /user/driver/<user_id>
```

### Get All Cabs
```
GET /cab/cab
```

### Get All Batches
```
GET /cab/batch
```

### Get Running Batches (Today)
```
GET /d2d/running_batches/<admin_code>
```

## 🔄 D2D Log Operations

### Add Commuter to Return Trip
```
POST /d2d/return_batch/add_commuter
Body: {"batch_id": "1", "commuter_id": "1"}
```

### Remove Commuter from Return Trip
```
POST /d2d/return_batch/remove_commuter
Body: {"batch_id": "1", "commuter_id": "1"}
```

### Get Return Trip Commuters
```
GET /d2d/return_batch/view/<batch_id>
```

### Get Cache Data (Current Capacity)
```
GET /d2d/return_batch/get_commuter/<batch_id>
Response: {"commuter_list": [1,2,3], "total_capacity": 4, "current_capacity": 1}
```

### Check Trip Status
```
GET /d2d/get_d2d_log_status/<batch_id>
Response: "2" (in progress) or "3" (completed)
```

## 📋 Data Types Reference

- **IDs**: Integers (except adminCode which is UUID string)
- **Date**: "YYYY-MM-DD" format
- **Time**: "HH:MM:SS" format
- **Boolean**: true/false
- **Foreign Keys**: Send as integer ID

## ⚠️ Important Notes

1. All PATCH requests support **partial updates** - only send fields you want to change
2. Check response status codes: 200 = success, 201 = created, 400 = error
3. Most success responses are simple strings like "user updated"
4. Foreign key fields (batchId, cabId, routeId, etc.) accept integer IDs



