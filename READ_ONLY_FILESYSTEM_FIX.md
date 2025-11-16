# Read-Only Filesystem Fix Summary

## Issue

User reported error on Vercel deployment:
```json
{"error":"Failed to create storage directory. The server may have limited write permissions."}
```

## Root Cause

On serverless platforms like Vercel, the filesystem is read-only except for `/tmp`. The original implementation required:
1. Creating local directories with `os.makedirs()`
2. Writing files to local filesystem
3. Then uploading to blob storage as a secondary step

This failed when the filesystem was read-only, even though blob storage was configured and working.

## Solution

Made local filesystem storage **optional** when blob storage is enabled:

### 1. Directory Creation (lines 946-961)
```python
# Before: Failed if directory couldn't be created
os.makedirs(lang_dir, exist_ok=True)

# After: Continue with blob storage if creation fails
try:
    os.makedirs(lang_dir, exist_ok=True)
except OSError as e:
    if BLOB_STORAGE_ENABLED and blob_client:
        local_storage_available = False  # Continue without local storage
    else:
        return error  # Fail only if no blob storage
```

### 2. File Writing (lines 967-1052)
```python
# Before: Raised exception if file write failed
with open(filepath, 'w') as f:
    f.write(code_content)

# After: Catch permission errors, continue if blob storage succeeds
if local_storage_available:
    try:
        with open(filepath, 'w') as f:
            f.write(code_content)
    except (OSError, PermissionError) as e:
        if not (BLOB_STORAGE_ENABLED and blob_client):
            raise  # Re-raise only if no blob storage

# Always try blob storage
if BLOB_STORAGE_ENABLED and blob_client:
    result = blob_client.put(pathname, content)
    blob_url = result.get('url')
```

### 3. Metadata Saving (lines 391-426)
```python
# Before: Failed if local write failed
with open(metadata_path, 'w') as f:
    json.dump(metadata, f)

# After: Try local, fall back to blob
try:
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)
except (OSError, PermissionError) as e:
    local_save_failed = True

# Try blob storage
if BLOB_STORAGE_ENABLED:
    blob_client.put(pathname, json.dumps(metadata))

# Fail only if BOTH failed
if local_save_failed and blob_save_failed:
    raise Exception("Both storages failed")
```

## Storage Strategy

### With Blob Storage Enabled
1. ✅ **Try local storage** (for immediate access)
2. ✅ **Use blob storage** (for persistence)
3. ✅ **Succeed if blob works** (even if local fails)

### Without Blob Storage
1. ✅ **Require local storage** (must work)
2. ❌ **Fail if local storage unavailable**

## Benefits

1. **Works on Vercel**: No longer requires writable filesystem
2. **Graceful Degradation**: Still uses local storage when available
3. **Clear Errors**: Helpful messages guide configuration
4. **Backward Compatible**: Existing deployments unaffected

## Error Messages

### When Blob Storage Enabled
- ✅ Upload succeeds (uses blob storage)
- 🔍 Logs: "Using blob storage only (read-only filesystem)"

### When Blob Storage Disabled
- ❌ Upload fails
- 💡 Error: "Failed to create storage directory. The server may have limited write permissions."

### When Both Fail
- ❌ Upload fails
- 💡 Error: "No storage available. Please configure BLOB_READ_WRITE_TOKEN or fix filesystem permissions."

## Testing

- ✅ All 14 unit tests passing
- ✅ Python syntax validation passed
- ✅ No breaking changes

## Deployment

On Vercel with blob storage:
1. Set environment variable: `BLOB_READ_WRITE_TOKEN=vercel_blob_rw_...`
2. Deploy application
3. Upload works without local filesystem access
4. Files stored in blob, accessible via URLs

## Commit

**Hash:** 92a0150
**Message:** Fix read-only filesystem error by making local storage optional when blob storage is enabled
