# Data Model: Restaurant Analytics Web Application

**Purpose**: Define data structures and entities for restaurant analytics
**Created**: 2025-11-12
**Feature**: Restaurant Analytics Web Application

## Core Entities

### Restaurant

**Description**: Individual restaurant record from zomato.csv

**Attributes**:
- `name: str` - Restaurant name
- `location: str` - Bangalore area/neighborhood
- `restaurant_type: str` - Type (Quick Bites, Casual Dining, Cafe, etc.)
- `cuisines: List[str]` - List of cuisine types
- `rating: Optional[float]` - Rating out of 5.0
- `votes: int` - Number of votes/ratings
- `approx_cost_for_two: Optional[int]` - Cost in INR for two people
- `online_order: bool` - Whether online ordering is available
- `book_table: bool` - Whether table booking is available

**Validation Rules**:
- `name` and `location` are required fields
- `rating` must be between 1.0 and 5.0 if present
- `votes` must be non-negative integer
- `approx_cost_for_two` must be positive integer if present

### RestaurantTypeSummary

**Description**: Aggregated statistics for restaurant types

**Attributes**:
- `restaurant_type: str` - Type name
- `count: int` - Number of restaurants of this type
- `percentage: float` - Percentage of total restaurants
- `avg_rating: Optional[float]` - Average rating for this type
- `avg_cost_for_two: Optional[int]` - Average cost for two people

**Validation Rules**:
- `count` must be positive integer
- `percentage` must be between 0.0 and 100.0
- `avg_rating` between 1.0 and 5.0 if present

### TopRestaurant

**Description**: Restaurant in top rankings

**Attributes**:
- `name: str` - Restaurant name
- `location: str` - Location/area
- `rating: Optional[float]` - Rating out of 5.0
- `votes: int` - Number of votes
- `restaurant_type: str` - Restaurant type
- `cuisines: List[str]` - List of cuisines
- `rank: int` - Position in ranking (1-10)

**Validation Rules**:
- `rank` must be between 1 and 10
- All required fields from Restaurant entity apply

### FoodieArea

**Description**: Area with high restaurant concentration

**Attributes**:
- `area: str` - Bangalore area name
- `restaurant_count: int` - Number of restaurants in area
- `avg_rating: Optional[float]` - Average rating of restaurants in area
- `top_cuisines: List[str]` - Most common cuisines in area
- `restaurant_types: List[str]` - Restaurant types present in area

**Validation Rules**:
- `restaurant_count` must be positive integer
- `avg_rating` between 1.0 and 5.0 if present

### AnalyticsData

**Description**: Complete analytics dataset for dashboard

**Attributes**:
- `restaurant_types: List[RestaurantTypeSummary]` - Type summaries
- `top_restaurants: List[TopRestaurant]` - Top 10 restaurants
- `foodie_areas: List[FoodieArea]` - Area analysis
- `metadata: AnalyticsMetadata` - Processing metadata

### AnalyticsMetadata

**Description**: Metadata about analytics processing

**Attributes**:
- `total_restaurants: int` - Total records processed
- `last_updated: datetime` - When data was last processed
- `processing_time_ms: int` - Time taken to process data
- `data_source: str` - Source file (zomato.csv under repo-root data/)

## API Response Models

### APIResponse

**Description**: Standard API response wrapper

**Attributes**:
- `success: bool` - Whether request was successful
- `data: Optional[Dict[str, Any]]` - Response data payload
- `error: Optional[str]` - Error message if unsuccessful
- `metadata: ResponseMetadata` - Response metadata

### ResponseMetadata

**Description**: Metadata about API response

**Attributes**:
- `timestamp: datetime` - Response timestamp
- `processing_time_ms: int` - Server processing time
- `request_id: str` - Unique request identifier

## Chart Data Models

### ChartData

**Description**: Data for chart generation

**Attributes**:
- `chart_type: str` - Type of chart (bar, pie, heatmap)
- `title: str` - Chart title
- `data: Dict[str, Any]` - Chart-specific data
- `base64_image: str` - Chart as base64 encoded image

## Data Relationships

```
Restaurant (1) → RestaurantTypeSummary (many)
Restaurant (1) → TopRestaurant (many)  
Restaurant (1) → FoodieArea (many)
RestaurantTypeSummary (many) → AnalyticsData (1)
TopRestaurant (many) → AnalyticsData (1)
FoodieArea (many) → AnalyticsData (1)
```

## Data Processing Flow

1. **Data Loading**: Load zomato.csv into Restaurant objects
2. **Validation**: Clean and validate restaurant data
3. **Aggregation**: Calculate RestaurantTypeSummary objects
4. **Ranking**: Generate TopRestaurant objects based on votes/ratings
5. **Area Analysis**: Create FoodieArea objects by location grouping
6. **Assembly**: Combine into AnalyticsData with metadata

## State Management

### Application State

**Description**: In-memory state during application lifecycle

**Components**:
- `restaurants_df: pandas.DataFrame` - Raw restaurant data
- `analytics_data: AnalyticsData` - Processed analytics
- `last_data_refresh: datetime` - When data was last loaded

**State Transitions**:
- **Startup**: Load CSV → Process data → Cache analytics
- **Data Refresh**: Reload CSV → Reprocess → Update cache
- **API Request**: Serve from cached analytics data

## Error Handling

### Data Validation Errors

**Types**:
- Missing required fields
- Invalid data formats
- Out-of-range values

**Handling Strategy**:
- Log validation errors
- Skip invalid records with warning
- Continue processing valid data

### API Error Responses

**Error Types**:
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Data not available
- `500 Internal Server Error` - Processing failures

**Error Format**:
```json
{
  "success": false,
  "error": "Descriptive error message",
  "metadata": {
    "timestamp": "2025-11-12T10:00:00Z",
    "request_id": "uuid-string"
  }
}
```

## Performance Considerations

### Memory Optimization

**Strategies**:
- Use pandas categoricals for string columns
- Pre-calculate aggregations at startup
- Cache results in memory

### Processing Optimization

**Techniques**:
- Vectorized pandas operations
- Efficient grouping and sorting
- Minimal data copying

## Validation Rules Summary

| Entity | Required Fields | Type Validation | Range Validation |
|--------|----------------|----------------|------------------|
| Restaurant | name, location | String types | rating 1-5, votes ≥0 |
| RestaurantTypeSummary | restaurant_type, count | Positive integers | percentage 0-100 |
| TopRestaurant | All Restaurant fields + rank | Inherited | rank 1-10 |
| FoodieArea | area, restaurant_count | String/int | count ≥1, rating 1-5 |
| AnalyticsData | All component lists | List types | Component validation |

This data model supports all functional requirements while maintaining type safety and validation rules required by the project constitution.
