# Project Overview - Django Backend for Flutter Developer

## 🎯 What This Project Does

This is a **cab/transport service management system** backend. It manages:
- **Users**: Commuters (passengers), Drivers, and Admins
- **Routes**: Different travel routes
- **Batches**: Time slots for trips (Morning, Evening, etc.)
- **Pickup Points**: Locations where passengers are picked up
- **Cabs**: Vehicle information
- **D2D Logs**: Day-to-day trip tracking and return trip management

---

## 📁 Project Structure Explained

### Main Project Folder: `c2s/`
- `settings.py` - Configuration (database, apps, etc.)
- `urls.py` - Main URL routing (connects all apps)

### Three Main Apps:

#### 1. **user_servcies** (User Management)
**What it does**: Handles all user-related operations

**Key Models**:
- `User` - Base user (login, profile)
- `commuter` - Passenger details (college, pickup point, batch)
- `Driver` - Driver details (assigned cab, batch)
- `subAdmin` - Admin users

**Main APIs**:
- `/user/` - User CRUD operations
- `/user/commuter/` - Commuter operations
- `/user/driver/` - Driver operations
- `/user/login` - Authentication

---

#### 2. **cab_services** (Cab & Route Management)
**What it does**: Manages routes, batches, pickup points, and cabs

**Key Models**:
- `Routes` - Travel routes
- `Batch` - Time slots (Morning 8AM, Evening 5PM, etc.)
- `pickUpPoints` - Pickup locations with GPS coordinates
- `cab` - Vehicle information (registration, capacity, etc.)

**Main APIs**:
- `/cab/route/` - Route operations
- `/cab/batch/` - Batch operations
- `/cab/pickUpPoint/` - Pickup point operations
- `/cab/cab/` - Cab operations

---

#### 3. **d2d_log** (Trip Logging)
**What it does**: Tracks daily trips and manages return trips

**Key Models**:
- `DTODLOG` - Daily trip log (tracks which batch is running, start/end times)

**Main APIs**:
- `/d2d/running_batches/` - Get active trips for today
- `/d2d/return_batch/` - Manage return trip commuters
- `/d2d/get_d2d_log_status/` - Check trip status

---

## 🔄 How Data Flows

### Example: A Commuter's Journey

1. **Registration**: 
   - Create User → `/user/` (POST)
   - Creates commuter record with batch, pickup point, etc.

2. **Daily Trip**:
   - Driver starts trip → Creates D2D log
   - Commuters board → Tracked in system
   - Return trip → Commuters added via `/d2d/return_batch/add_commuter`

3. **Updates**:
   - Change pickup point → `PATCH /user/commuter/<id>`
   - Change batch → `PATCH /user/commuter/<id>` with new `batchId`
   - Update cab capacity → `PATCH /cab/cab/<id>`

---

## 🔑 Key Concepts for Flutter Integration

### 1. **Foreign Keys (Relationships)**
When updating, you send the **ID** of related objects:
```json
{
  "batchId": 1,      // Integer ID
  "cabId": 2,        // Integer ID
  "routeId": 3       // Integer ID
}
```

### 2. **Admin Code (UUID)**
Admin codes are **UUID strings**, not integers:
```json
{
  "adminCode": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 3. **Partial Updates**
All PATCH requests support partial updates - only send what you want to change:
```json
// Only update the name
{
  "first_name": "John"
}

// Don't need to send all fields!
```

### 4. **Date/Time Formats**
- **Date**: `"2024-01-15"` (YYYY-MM-DD)
- **Time**: `"08:00:00"` (HH:MM:SS)

---

## 📊 Common Update Scenarios

### Scenario 1: User Changes Their Profile
```
PATCH /user/1
Body: {"first_name": "John", "email": "new@email.com"}
```

### Scenario 2: Commuter Changes Their Batch
```
PATCH /user/commuter/1
Body: {"batchId": 2}
```

### Scenario 3: Commuter Marks They're Not Coming
```
PATCH /user/commuter/1
Body: {"isComing": false}
```

### Scenario 4: Driver Updates Cab Assignment
```
PATCH /user/driver/1
Body: {"cabId": 3}
```

### Scenario 5: Admin Updates Batch Time
```
PATCH /cab/batch/1
Body: {"batchTime": "09:00:00", "end_time": "10:00:00"}
```

### Scenario 6: Add Commuter to Return Trip
```
POST /d2d/return_batch/add_commuter
Body: {"batch_id": "1", "commuter_id": "1"}
```

---

## 🚨 Important Things to Know

1. **Authentication**: Currently uses session-based auth. Login returns `user_id` and `user_type`.

2. **Error Responses**: Most errors return simple strings like `"ERROR"` or `"INVALID DATA"`. Check status codes:
   - `200` = Success
   - `201` = Created
   - `204` = No Content (sometimes means error)
   - `400` = Bad Request

3. **Response Format**: Success responses are often simple strings:
   - `"user updated"`
   - `"CAB UPDATED"`
   - `"commuter added"`

4. **Capacity Management**: Return trips check cab capacity. If full, returns `204` with `"out of capcaity"`.

5. **Cache System**: D2D log uses Redis cache to temporarily store return trip commuters before finalizing.

---

## 🛠️ Testing Your API Calls

### Using Postman/Thunder Client:
1. Set method to `PATCH` or `POST`
2. Set URL: `http://localhost:8000/user/1` (or your domain)
3. Add header: `Content-Type: application/json`
4. Add body (raw JSON):
```json
{
  "first_name": "John"
}
```

### Using cURL:
```bash
curl -X PATCH http://localhost:8000/user/1 \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John"}'
```

---

## 📝 Quick Checklist for Flutter Integration

- [ ] Set correct base URL in your API service
- [ ] Handle login and store user_id/user_type
- [ ] Use PATCH for updates (not PUT)
- [ ] Send only fields you want to update
- [ ] Handle foreign keys as integers (except adminCode)
- [ ] Format dates as "YYYY-MM-DD"
- [ ] Format times as "HH:MM:SS"
- [ ] Check response status codes
- [ ] Handle error messages appropriately

---

## 🆘 Common Issues & Solutions

### Issue: "ERROR WHILE CREATING" or "INVALID DATA"
**Solution**: Check that all required fields are present and foreign key IDs exist.

### Issue: Update not working
**Solution**: 
- Verify you're using PATCH (not POST/PUT)
- Check the ID in URL is correct
- Ensure JSON is valid

### Issue: "out of capcaity"
**Solution**: Cab is full. Check capacity with `/d2d/return_batch/get_commuter/<batch_id>`

### Issue: Foreign key error
**Solution**: Make sure the ID you're referencing exists (e.g., batchId, cabId)

---

## 📚 Files to Reference

- **Full API Docs**: `API_DOCUMENTATION.md`
- **Quick Reference**: `QUICK_REFERENCE.md`
- **Flutter Example**: `flutter_api_example.dart`

---

## 💡 Tips

1. **Start Simple**: Test with GET requests first to see data structure
2. **Use Postman**: Test API calls before coding in Flutter
3. **Check Models**: Look at `models.py` files to understand data structure
4. **Read Serializers**: Check `serializers.py` to see request/response format
5. **Partial Updates**: You don't need to send all fields, just what changes

---

Good luck with your integration! 🚀

If you need to add new endpoints or modify existing ones, the main files are:
- `views.py` - API logic
- `urls.py` - URL routing
- `serializers.py` - Data format
- `models.py` - Database structure



