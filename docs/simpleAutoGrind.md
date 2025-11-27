# Simple Auto Grind Feature Design

## Overview

A simplified version of autoBarbarians that provides easy-to-use automated barbarian farming with user-friendly configuration and level-based stopping conditions.

## Key Features

### 1. Simple Attack Configuration
- **Single-wave attacks** (no complex multi-wave coordination)
- **User-defined unit composition** (select your own army mix)
- **Automatic looting** with remaining forces
- **Smart ship allocation** based on available capacity

### 2. Level-based Auto Stop
- **Max Level Setting**: User sets maximum barbarian level to attack
- **Auto Termination**: Stops when barbarians exceed chosen level
- **Safety Buffer**: Optional margin (e.g., stop at level 18 if max is 20)

### 3. Streamlined Setup
- **Quick Configuration**: Minimal prompts for faster setup
- **Preset Suggestions**: Recommended army compositions for different levels
- **Resource Validation**: Simple checks for sufficient troops/ships

## Proposed Implementation

### User Interface Flow

```
1. Island Selection
   → Choose target island with barbarians

2. Attack City Selection
   → Choose city to attack from

3. Max Level Setting
   → "Attack barbarians up to level: [1-50]"
   → Optional: "Stop X levels before max for safety"

4. Army Configuration
   → Simple unit selection with current amounts shown
   → Suggested compositions based on current barbarian level
   → Auto-calculate ships needed

5. Confirmation & Start
   → Show summary and begin automated grinding
```

### Core Algorithm

```python
def simpleAutoGrind(session, island, city, max_level, army_config, safety_margin=0):
    while True:
        # Check barbarian status
        barbarian_info = get_barbarians_lv(session, island, ship_capacity)
        current_level = int(barbarian_info["level"])

        # Stop condition
        if current_level > (max_level - safety_margin):
            send_notification("Barbarians exceeded max level, stopping")
            break

        # Wait if barbarians destroyed
        if island["barbarians"]["destroyed"] == 1:
            loot_resources(session, island, city, army_config)
            wait_for_respawn()
            continue

        # Validate resources
        if not has_sufficient_troops(session, city, army_config):
            send_notification("Insufficient troops, stopping")
            break

        # Execute single-wave attack
        execute_simple_attack(session, island, city, army_config)
        wait_for_battle_completion()
```

### Army Configuration Options

#### Option 1: Quick Presets
```
- Light Attack (Levels 1-10): 50 Swordsmen + 20 Carabineers
- Medium Attack (Levels 11-20): 100 Swordsmen + 50 Carabineers + 20 Mortars
- Heavy Attack (Levels 21-30): 200 Swordsmen + 100 Carabineers + 50 Mortars + 10 Rams
- Custom: User defines own composition
```

#### Option 2: Smart Scaling
```
- Base Army: User defines core unit mix
- Auto Scaling: Multiply by factor based on barbarian level
- Example: Base (50 Swordsmen) × Level Factor = Adjusted army size
```

### Safety Features

#### Level Management
- **Progressive Stopping**: Warn when approaching max level
- **Safety Buffer**: Built-in margin to prevent over-leveling
- **Manual Override**: Allow user to increase max level during operation

#### Resource Protection
- **Minimum Reserves**: Keep X units in city for defense
- **Ship Management**: Reserve ships for other operations
- **Cost Monitoring**: Track resource consumption rates

### Configuration Structure

```python
SIMPLE_GRIND_CONFIG = {
    "max_level": 25,
    "safety_margin": 2,
    "army": {
        "302": 100,  # Swordsmen
        "304": 50,   # Carabineers
        "305": 20,   # Mortars
        "307": 5,    # Rams
    },
    "looting_army": {
        "305": 20,   # Mortars for looting
        "308": 30,   # Steam Giants for looting
    },
    "reserves": {
        "min_ships": 3,
        "min_troops_percent": 10,  # Keep 10% of army in city
    }
}
```

## User Benefits

### Accessibility
- **Beginner Friendly**: No complex wave timing or strategy knowledge needed
- **Quick Setup**: Get grinding in under 2 minutes
- **Clear Limits**: Know exactly when it will stop

### Control
- **Level Control**: Prevent barbarians from getting too strong
- **Resource Control**: Simple army management
- **Time Control**: Set and forget automation with clear end conditions

### Safety
- **Automatic Stopping**: Won't run indefinitely if unchecked
- **Resource Protection**: Built-in minimums prevent resource depletion
- **Progressive Warnings**: Alerts as barbarians approach max level

## Implementation Plan

### Phase 1: Core Functionality
1. Basic single-wave attack system
2. Level checking and auto-stop
3. Simple army configuration UI
4. Resource validation

### Phase 2: Enhanced Features
1. Preset army configurations
2. Smart scaling based on barbarian level
3. Advanced safety features
4. Statistics tracking

### Phase 3: Integration
1. Menu integration with existing autoBarbarians
2. Migration path from complex to simple mode
3. Shared utility functions
4. Documentation and examples

## File Structure

```
ikabot/function/simpleAutoGrind.py    # Main implementation
docs/simpleAutoGrind.md              # User documentation
tests/test_simpleAutoGrind.py        # Unit tests
```

## Menu Integration

```
Barbarian Attacks:
(1) Auto Barbarians (Advanced) - Complex multi-wave strategies
(2) Simple Auto Grind (Basic) - Easy automated farming
(3) Manual Attack - Single custom attack
(0) Exit
```

This feature would provide a middle ground between manual attacks and the complex autoBarbarians system, making automated barbarian farming accessible to more users while maintaining safety and control.