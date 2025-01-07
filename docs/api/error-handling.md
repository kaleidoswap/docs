---
id: error-handling
title: Error Handling
sidebar_position: 6
---

# Error Handling


The Kaleidoswap API uses standard HTTP status codes and detailed error messages to communicate the outcome of API requests. This section provides an overview of common error types and how to handle them effectively.

---

## HTTP Status Codes

### 2xx: Success
- **200 OK**: The request was successful, and the server returned the expected response.

### 4xx: Client Errors
These errors indicate an issue with the client’s request:
- **400 Bad Request**: The request is malformed or contains invalid parameters.
- **401 Unauthorized**: Authentication is required but missing or invalid (not currently applicable as of the latest version).
- **403 Forbidden**: The client does not have permission to access the requested resource.
- **404 Not Found**: The requested resource could not be found.
- **429 Too Many Requests**: The client has exceeded the allowed rate limit.

### 5xx: Server Errors
These errors indicate an issue on the server side:
- **500 Internal Server Error**: An unexpected error occurred on the server.
- **502 Bad Gateway**: The server received an invalid response from an upstream server.
- **503 Service Unavailable**: The service is temporarily unavailable, possibly due to maintenance or overload.

---

## Error Response Format

When an error occurs, the API returns a JSON response containing the following fields:

### Example Error Response
```json
{
  "detail": "Error message here"
}
```

## Fields

- `detail`: `array<object>`.
  - `Items`: `object`.
    - `loc`: `array<(string | integer)>`.
      - `Items`: `string | integer`.
        - `Any of`: `string | integer`.
          - `#0`: `string`.
          - `#1`: `integer`. 
    - `msg`: `string`.
    - `type`: `string`.

---

## Common Errors
Here are some typical errors and their resolutions:

### 400 Bad Request
- **Cause**: Missing or invalid parameters in the request.
- **Solution**: Verify the request payload and ensure all required fields are provided with valid data.

### 404 Not Found
- **Cause**: The requested endpoint or resource does not exist.
- **Solution**: Check the endpoint URL and resource identifiers.

### 429 Too Many Requests
- **Cause**: The client has sent too many requests in a short period.
- **Solution**: Implement rate-limiting in your client application and retry after the specified wait time (if provided).

### 500 Internal Server Error
- **Cause**: An unexpected error occurred on the server.
- **Solution**: Retry the request later. If the issue persists, contact support with details about the request.

---

## WebSocket Error Handling
For WebSocket connections, errors are communicated as JSON messages. If a critical error occurs, the server may close the connection.

### Reconnection Strategy
If a WebSocket connection is closed unexpectedly:

1. Wait for a few seconds (e.g., 5-10 seconds).
2. Re-establish the connection.
3. Resend any required subscription messages.

---

### Debugging Tips
1. **Check Logs**: Monitor your application logs for details about failed requests.
2. **Validate Inputs**: Ensure all request parameters and payloads meet the API requirements.
3. **Contact Support**: For persistent or unclear errors, provide the following details:
   - Request URL
   - HTTP method
   - Request payload
   - Timestamp of the error
   - Full error response from the API

---

## Best Practices
1. **Handle Errors Gracefully**: Implement proper error-handling logic in your application to avoid crashes or user frustration.
2. **Rate-Limiting**: Respect the API rate limits to avoid `429 Too Many Requests` errors.
3. **Retry Mechanism**: For transient errors (e.g., 500 Internal Server Error), implement a retry mechanism with exponential backoff.

---

For additional details on error codes and troubleshooting, refer to the API documentation.
