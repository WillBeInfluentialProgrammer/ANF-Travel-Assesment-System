/**
 * Deterministic Flight ID Construction - Examples
 * 
 * This document demonstrates how to use the deterministic Flight ID construction
 * logic in the FlightIdentifier class.
 */

// ============ EXAMPLE 1: Basic Flight ID Construction ============

Map<String, String> row = new HashMap<>();
row.put("carrier", "PK");
row.put("flightNumber", "353");
row.put("flightDate", "2026-01-16");

FlightIdentifier id = FlightDataExtractor.extractFromRow(row);

// Deterministic ID (no separators, validated)
String deterministicId = id.getDeterministicFlightId();
// Result: "PK035320260116"

// Human-readable format (separate)
String humanReadable = id.getHumanReadableId();
// Result: "PK353 on 2026-01-16"

// Full flight number
String fullFlight = id.getFullFlightNumber();
// Result: "PK0353"


// ============ EXAMPLE 2: Multi-Leg Flight ============

FlightIdentifier multiLegId = FlightIdentifier.builder()
    .carrierCode("PK")
    .flightNumber("353")
    .flightDate(LocalDate.of(2026, 1, 16))
    .legNumber(1)  // Multi-leg flight
    .build();

String deterministicWithLeg = multiLegId.getDeterministicFlightId();
// Result: "PK035320260116L1"


// ============ EXAMPLE 3: ICAO Carrier Code (3 characters) ============

FlightIdentifier icaoId = FlightIdentifier.builder()
    .carrierCode("UAE")  // 3-character ICAO code
    .flightNumber("1234")
    .flightDate(LocalDate.of(2026, 1, 16))
    .build();

String icaoDeterministic = icaoId.getDeterministicFlightId();
// Result: "UAE123420260116"


// ============ EXAMPLE 4: Single-Digit Flight Number ============

FlightIdentifier singleDigit = FlightIdentifier.builder()
    .carrierCode("EK")
    .flightNumber("1")  // Will be zero-padded to 0001
    .flightDate(LocalDate.of(2026, 1, 16))
    .build();

String paddedDeterministic = singleDigit.getDeterministicFlightId();
// Result: "EK000120260116"


// ============ EXAMPLE 5: Validation ============

// Valid deterministic IDs
boolean valid1 = FlightIdentifier.isValidDeterministicFlightId("PK035320260116");     // true
boolean valid2 = FlightIdentifier.isValidDeterministicFlightId("PK035320260116L1");   // true
boolean valid3 = FlightIdentifier.isValidDeterministicFlightId("UAE123420260116");    // true

// Invalid deterministic IDs
boolean invalid1 = FlightIdentifier.isValidDeterministicFlightId("PK35320260116");    // false (3 digits)
boolean invalid2 = FlightIdentifier.isValidDeterministicFlightId("PK_0353_20260116"); // false (separators)
boolean invalid3 = FlightIdentifier.isValidDeterministicFlightId("PK0353202601");     // false (6-digit date)


// ============ EXAMPLE 6: Complete Usage in Processing ============

public void processFlightManifest(Map<String, String> rowData) {
    // Extract and normalize
    FlightIdentifier id = FlightDataExtractor.extractFromRow(rowData);
    
    if (id == null) {
        logger.error("Cannot extract valid flight identifier");
        return;
    }
    
    // Get deterministic ID for internal tracking
    String internalId = id.getDeterministicFlightId();
    logger.info("Processing flight with deterministic ID: {}", internalId);
    
    // Get human-readable format for logs/UI
    String displayId = id.getHumanReadableId();
    logger.info("Flight: {}", displayId);
    
    // Store in database with validated components
    Flight flight = new Flight();
    flight.setCarrier(id.getCarrierCode());
    flight.setFlightNumber(id.getFlightNumber());
    flight.setEtdDate(java.sql.Date.valueOf(id.getFlightDate()));
    flight.setInternalId(internalId);  // Store deterministic ID
    
    flightRepository.save(flight);
}


// ============ REGEX PATTERN ============

// The deterministic Flight ID follows this pattern:
// ^[A-Z0-9]{2,3}[0-9]{4}[0-9]{8}(L[1-9])?$
//
// Breakdown:
// [A-Z0-9]{2,3}  - Carrier code (2-3 characters, IATA or ICAO)
// [0-9]{4}       - Flight number (4 digits, zero-padded)
// [0-9]{8}       - Date (YYYYMMDD format, 8 digits)
// (L[1-9])?      - Optional leg number (L followed by 1-9)


// ============ COMPARISON OF ID FORMATS ============

FlightIdentifier id = FlightIdentifier.builder()
    .carrierCode("PK")
    .flightNumber("353")
    .flightDate(LocalDate.of(2026, 1, 16))
    .originAirport("KHI")
    .destinationAirport("DXB")
    .legNumber(1)
    .build();

// Different ID formats for different purposes:
id.getFlightNumber()           // "0353" (zero-padded for storage)
id.getRawFlightNumber()        // "353" (no padding)
id.getFullFlightNumber()       // "PK0353" (carrier + padded number)
id.getDeterministicFlightId()  // "PK035320260116L1" (internal unique ID)
id.getCompositeFlightId()      // "PK_0353_20260116_KHI_DXB_L1" (database constraint)
id.getHumanReadableId()        // "PK353 from KHI to DXB on 2026-01-16 (Leg 1)" (display)


// ============ KEY RULES ============

/**
 * Rule 1: Concatenate without separators for internal ID
 * - Deterministic ID has NO underscores, dashes, or spaces
 * - Example: PK035320260116 (not PK_0353_20260116)
 */

/**
 * Rule 2: Preserve human-readable format separately
 * - Use getHumanReadableId() for display/logging
 * - Use getDeterministicFlightId() for internal tracking
 */

/**
 * Rule 3: Validate constructed ID against regex
 * - getDeterministicFlightId() throws IllegalStateException if validation fails
 * - Use isValidDeterministicFlightId() to pre-validate strings
 */

/**
 * Rule 4: Support multi-leg flights
 * - Append "L" + leg number if legNumber is present
 * - Example: PK035320260116L1 for leg 1
 */
