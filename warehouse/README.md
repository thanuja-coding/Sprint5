# Sprint5
# Warehouse Dispatch Management System

## 1. Problem Statement

A logistics company operates a warehouse where packages arrive from different sources and need to be dispatched to various destinations.

Warehouse staff need to organize packages, track their current status, and group them into dispatch batches before assigning them to delivery vehicles.

Currently, these operations are handled manually, making it difficult to track pending packages, manage dispatches, and monitor warehouse activity.

The goal is to build a **Warehouse Dispatch Management System** that simplifies package management and provides visibility into warehouse dispatch operations.

## 2. Objectives

- Register and maintain package details.
- Track the status of packages inside the warehouse.
- Search and filter packages based on different criteria.
- Organize packages into dispatch batches.
- View dispatch information and warehouse statistics.

## 3. Functional Requirements

### Package Management

- Register a new package with details such as package name, destination, weight, arrival date and status.
- View the details of a specific package.
- Update package information partially.
- Delete a package if it has not yet been dispatched.
- Retrieve packages using filters such as destination, status and arrival date.

### Dispatch Management

- View dispatch batches with filters such as destination, vehicle and dispatch status.

### Warehouse Analytics

Generate a dispatch summary containing:

- Total packages received.
- Total packages pending dispatch.
- Total packages dispatched.
- Destination-wise package count.

## 4. API Requirements

| # | Description | Method | Endpoint | Path / Query Params | Request Body | Response Body | Status Codes |
|---|---|---|---|---|---|---|---|
| 1 | Register a package | POST | /packages | name, destination, weight, arrival_date, status | – | Package details | 200, 422 |
| 2 | Get a specific package | GET | /packages/{package_id} | package_id | – | Package details | 200, 404 |
| 3 | Update package details | PATCH | /packages/{package_id} | package_id, fields to update | – | Updated package | 200, 404 |
| 4 | Delete a package | DELETE | /packages/{package_id} | package_id | – | Message | 200, 404, 400 |
| 5 | Search packages | GET | /packages | destination, status, arrival_date | – | List of packages | 200 |
| 6 | View dispatch batches | GET | /dispatches | destination, vehicle, status | – | List of dispatches | 200 |
| 7 | Warehouse statistics | GET | /stats | – | – | total, pending, dispatched, destination-wise count | 200 |
| 8 | Create dispatch batch | POST | /dispatches | vehicle, destination, dispatch_date | – | Dispatch details | 200, 404 |


> **Your task:** Complete the table before you start building. For each API, decide the HTTP method, endpoint path, path and query parameters, request body, response body, and status codes — including error cases (e.g. package not found, deleting a dispatched package).

> **Note:** To have data to work with, your app needs an endpoint to add data manually (row 8) — the other requirements only cover viewing dispatch batches, not creating them.

## 5. Scope

The application will focus on warehouse package management and dispatch visibility.

The following are **outside the scope**:

- User authentication and authorization.
- Live vehicle tracking.
- Route optimization.
- Payment processing.
- External logistics integrations.

## 6. Technology Stack

| Area | Technology |
| --- | --- |
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| API Documentation | Swagger UI |
| API Testing | Postman |

## 7. Expected Outcome

A working REST API application that allows warehouse staff to manage packages, view dispatch batches, filter records and generate basic warehouse statistics.
