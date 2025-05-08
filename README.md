# Flight Board

A Home Assistant integration to show upcoming and recent commercial flights for a specific airport.

## Installation

1. Add this repository as a **Custom Repository** in HACS under "Integrations."
2. Install the **Flight Board** integration via HACS.
3. Add configuration to your `configuration.yaml`:

```yaml
flight_board:
  api_key: "your_aeroapi_key_here"
  airport: "DAB"
  update_interval: 30
```

## Features

- Shows 3 most recent arrivals and departures.
- Shows upcoming flights for the next 24 hours.
- Data refreshes every 30 minutes by default.
- Powered by FlightAware AeroAPI.
