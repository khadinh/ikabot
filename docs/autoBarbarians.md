# AutoBarbarians Feature Documentation

## Overview

The AutoBarbarians feature is an advanced automated military system for continuously farming barbarian villages in Ikariam. It provides efficient resource gathering through coordinated attacks and looting operations.

## Core Functionality

### Purpose
- Automated barbarian village farming
- Continuous resource collection
- Optimized troop deployment
- Multi-wave attack coordination

### Key Features
- **Preset Attack Schemes**: 4 configurations based on barbarian levels
- **Multi-Wave System**: Coordinated assault patterns
- **Resource Optimization**: Automatic ship capacity calculations
- **Safety Mechanisms**: Comprehensive validation and error handling

## Attack Configurations

### Default Schematics (Without Hephaestus)

#### Level 1-9 Barbarians
- **Attack Force**: 90 Swordsmen (302) + 21 Sulphur Carabineers (304)
- **Looting Force**: 1 Swordsman (302)
- **Strategy**: Basic assault for low-level villages

#### Level 10-19 Barbarians
- **Attack Force**: 60 Swordsmen (302) + 35 Sulphur Carabineers (304) + 12 Mortars (305) + 50 Steam Giants (308)
- **Looting Force**: 12 Mortars (305) + 50 Steam Giants (308)
- **Strategy**: Mixed unit composition with artillery support

#### Level 20-29 Barbarians
- **Attack Force**: 60 Swordsmen (302) + 70 Sulphur Carabineers (304) + 12 Mortars (305) + 12 Battering Rams (307) + 100 Steam Giants (308) + 30 Balloon-Bombardiers (309) + 5 Cooks (310)
- **Looting Force**: 12 Mortars (305) + 100 Steam Giants (308)
- **Strategy**: Heavy assault with siege weapons and bombers

#### Level 30-39 Barbarians
- **Attack Force**: 300 Swordsmen (302) + 147 Sulphur Carabineers (304) + 24 Mortars (305) + 18 Battering Rams (307) + 300 Steam Giants (308) + 5 Cooks (310) + 10 Doctors (311)
- **Looting Force**: 24 Mortars (305) + 150 Steam Giants (308)
- **Strategy**: Full army deployment with support units

## Unit Reference

| Unit ID | Unit Name | Role |
|---------|-----------|------|
| 301 | Slinger | Ranged |
| 302 | Swordsman | Light Infantry |
| 303 | Hoplite | Heavy Infantry |
| 304 | Sulphur Carabineer | Ranged |
| 305 | Mortar | Artillery |
| 306 | Catapult | Artillery |
| 307 | Battering Ram | Artillery |
| 308 | Steam Giant | Heavy Infantry |
| 309 | Balloon-Bombardier | Bomber |
| 310 | Cook | Support |
| 311 | Doctor | Support |
| 312 | Gyrocopter | Fighter Pilot |
| 313 | Archer | Ranged |
| 315 | Spearman | Light Infantry |

## Setup Process

### Prerequisites
- **Minimum 2 Battering Rams** in attacking city
- **Minimum 3 Merchant Ships** available
- Sufficient troops for selected barbarian level

### Configuration Steps
1. **Island Selection**: Choose target island with barbarian villages
2. **City Selection**: Select attacking city
3. **Float City** (optional): Secondary support city on same island
4. **Resource Validation**: Confirm troop availability
5. **Safety Agreement**: Accept resource loss responsibility

## Battle System

### Wave Mechanics
- **Multi-Wave Attacks**: Coordinated assault timing
- **Travel Time Calculation**: Synchronizes arrivals from multiple cities
- **Battle Rounds**: Waits for appropriate attack windows
- **Looting Phase**: Automated resource collection after victory

### Resource Management
- **Ship Capacity**: Automatically calculates transport needs
- **Cargo Optimization**: Maximizes resource collection efficiency
- **Weight Calculations**: Considers unit weight for ship requirements
- **Available Ships**: Tracks and reserves necessary vessels

## Safety Mechanisms

### Validation Checks
- **Unit Availability**: Verifies sufficient troops before each attack
- **Ship Requirements**: Ensures adequate transport capacity
- **Resource Monitoring**: Tracks barbarian village status
- **Battle Timing**: Coordinates multi-wave arrivals

### Error Handling
- **Ship Shortage**: 20-attempt limit with status updates
- **Insufficient Troops**: Graceful termination with notifications
- **Battle Failures**: Automatic recovery and retry logic
- **Timeout Management**: Prevents infinite waiting

## Automation Loop

### Main Cycle
1. **Monitor**: Check barbarian village status every 5 minutes
2. **Validate**: Confirm troop and ship availability
3. **Attack**: Execute multi-wave assault sequence
4. **Wait**: Monitor battle progress until completion
5. **Loot**: Collect remaining resources
6. **Repeat**: Continue cycle until stopped

### Status Updates
- Real-time progress notifications
- Battle coordination messages
- Resource collection reports
- Error and completion alerts

## Advanced Features

### Hephaestus Integration (Development)
- Miracle activation support
- Enhanced attack efficiency
- Automatic miracle management
- Optimized resource gains

### Custom Schemas (Planned)
- User-defined attack patterns
- Flexible unit compositions
- Personalized strategies
- Advanced configuration options

## Best Practices

### Resource Management
- Keep 2+ extra rams in attacking city
- Maintain 3+ available merchant ships
- Avoid using merchants during grinding
- Monitor troop levels regularly

### Optimization Tips
- Position cities on same island for efficiency
- Use float cities for additional support
- Coordinate with miracle timings
- Plan for extended automation periods

## Troubleshooting

### Common Issues
- **Insufficient Ships**: Increase merchant ship count
- **Missing Troops**: Build required unit types
- **Battle Failures**: Check barbarian level compatibility
- **Resource Shortages**: Ensure adequate preparation

### Error Messages
- "Insufficient cargo ships!" - Need more transport capacity
- "Lack of necessary troops" - Build missing unit types
- "Long unavailability of ships" - Ships tied up elsewhere
- "Level outside attack scheme" - Barbarians too high level

## Technical Implementation

### Core Functions
- `autoBarbarians()` - Main entry point and setup
- `do_it()` - Primary automation loop
- `do_attack()` - Multi-wave battle execution
- `loot()` - Resource collection phase
- `get_barbarians_attack_plan()` - Schema selection logic

### Dependencies
- Session management for HTTP requests
- Naval helpers for ship calculations
- Military advisor for troop data
- Bot communication for notifications
- Process management for automation

## Security Considerations

The AutoBarbarians feature operates within game mechanics and does not:
- Exploit game vulnerabilities
- Use external automation tools
- Bypass game limitations
- Access unauthorized data

All operations use legitimate HTTP requests through the game's web interface.
