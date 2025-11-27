#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import traceback
from decimal import Decimal

from ikabot.config import *
from ikabot.helpers.botComm import *
from ikabot.helpers.getJson import getCity, getIsland
from ikabot.helpers.gui import *
from ikabot.helpers.naval import *
from ikabot.helpers.pedirInfo import *
from ikabot.helpers.planRoutes import waitForArrival
from ikabot.helpers.process import set_child_mode
from ikabot.helpers.signals import setInfoSignal
from ikabot.helpers.varios import *
from ikabot.helpers.pedirInfo import getShipCapacity

from ikabot.function.attackBarbarians import (
    choose_island,
    get_barbarians_lv,
    get_units,
    get_unit_data,
    wait_until_attack_is_over,
    wait_for_arrival,
)

# Preset army configurations for different barbarian levels
PRESET_ARMIES = {
    "light": {
        "name": "Light Attack (Levels 1-10)",
        "army": {"302": 50, "304": 20},
        "looting": {"302": 10, "304": 5},
        "max_recommended_level": 10,
    },
    "medium": {
        "name": "Medium Attack (Levels 11-20)",
        "army": {"302": 100, "304": 50, "305": 20},
        "looting": {"305": 20, "308": 30},
        "max_recommended_level": 20,
    },
    "heavy": {
        "name": "Heavy Attack (Levels 21-30)",
        "army": {"302": 200, "304": 100, "305": 50, "307": 10},
        "looting": {"305": 30, "308": 50},
        "max_recommended_level": 30,
    },
    "massive": {
        "name": "Massive Attack (Levels 31-40)",
        "army": {"302": 300, "304": 150, "305": 80, "307": 20, "308": 100},
        "looting": {"305": 40, "308": 80},
        "max_recommended_level": 40,
    },
}   

def simpleAutoGrind(session, event, stdin_fd, predetermined_input):
    """
    Simple Auto Grind - Simplified automated barbarian farming

    Parameters
    ----------
    session : ikabot.web.session.Session
    event : multiprocessing.Event
    stdin_fd: int
    predetermined_input : multiprocessing.managers.SyncManager.list
    """
    sys.stdin = os.fdopen(stdin_fd)
    config.predetermined_input = predetermined_input
    ship_capacity, freighter_capacity = getShipCapacity(session)

    try:
        banner()
        print("🗡️  Simple Auto Grind - Easy Barbarian Farming")
        print("=" * 50)
        print("This feature provides simplified automated barbarian attacks:")
        print("• Single-wave attacks with your chosen army")
        print("• Automatic stopping at your chosen max level")
        print("• Simple setup with preset configurations")
        print()

        # Step 1: Choose target island
        island = choose_island(session)
        if island is None:
            event.set()
            return

        # Step 2: Choose attacking city
        banner()
        print("From which city do you want to attack?")
        city = chooseCity(session)
        if city is None:
            event.set()
            return

        # Step 3: Get current barbarian info
        barbarians_info = get_barbarians_lv(session, island, ship_capacity)
        current_level = int(barbarians_info["level"])

        banner()
        print(f"Current barbarian level: {current_level}")
        print()

        # Step 4: Choose max level
        max_level = choose_max_level(current_level)
        if max_level is None:
            event.set()
            return

        # Step 5: Choose army configuration
        army_config = choose_army_configuration(session, city, current_level)
        if army_config is None:
            event.set()
            return

        # Step 6: Safety options
        safety_config = configure_safety_options()
        if safety_config is None:
            event.set()
            return

        # Step 7: Final confirmation
        banner()
        print("🎯 Configuration Summary:")
        print(f"Target: Island [{island['x']}:{island['y']}]")
        print(f"Attacking from: {city['name']}")
        print(f"Current barbarian level: {current_level}")
        print(f"Max level (will stop): {max_level}")
        if safety_config['safety_margin'] > 0:
            print(f"Safety margin: Stop {safety_config['safety_margin']} levels early")
        print()
        print("Army composition:")
        display_army_summary(army_config['army'], session, city)
        print()

        print("⚠️  This will run continuously until:")
        print(f"• Barbarians reach level {max_level - safety_config['safety_margin']}")
        print("• Insufficient troops in city")
        print("• Manual interruption (Ctrl+C)")
        print()

        confirm = read(values=["y", "Y", "n", "N"], msg="Start Simple Auto Grind? [y/N]: ", default="n")
        if confirm.lower() != "y":
            event.set()
            return

    except KeyboardInterrupt:
        event.set()
        return

    # Start automated grinding
    set_child_mode(session)
    event.set()

    info = f"\n🗡️ Simple Auto Grind on [{island['x']}:{island['y']}] (max level: {max_level})\n"
    setInfoSignal(session, info)

    try:
        run_simple_auto_grind(session, island, city, max_level, army_config, safety_config, ship_capacity)
    except Exception as e:
        msg = f"Error in Simple Auto Grind:\n{info}\nCause:\n{traceback.format_exc()}"
        sendToBot(session, msg)
    finally:
        session.logout()


def choose_max_level(current_level):
    """Choose maximum barbarian level to attack"""
    print(f"What is the maximum barbarian level you want to attack?")
    print(f"(Current level: {current_level})")
    print("The grind will stop automatically when barbarians exceed this level.")
    print()

    suggested_max = min(current_level + 10, 50)
    max_level = read(
        min=current_level,
        max=50,
        digit=True,
        msg=f"Max level (1-50, suggested: {suggested_max}): ",
        default=suggested_max
    )

    if max_level < current_level:
        print("⚠️ Max level cannot be lower than current level!")
        return None

    return max_level


def choose_army_configuration(session, city, current_level):
    """Choose army configuration - preset or custom"""
    banner()
    print("🏺 Army Configuration")
    print("Choose your attack strategy:")
    print()

    # Display presets
    presets = list(PRESET_ARMIES.keys())
    for i, preset_key in enumerate(presets, 1):
        preset = PRESET_ARMIES[preset_key]
        suitable = "✅" if current_level <= preset['max_recommended_level'] else "⚠️"
        print(f"({i}) {preset['name']} {suitable}")

    print(f"({len(presets) + 1}) Custom army composition")
    print("(0) Exit")
    print()

    choice = read(min=0, max=len(presets) + 1, digit=True, msg=prompt)
    if choice == 0:
        return None
    elif choice <= len(presets):
        # Use preset
        preset_key = presets[choice - 1]
        return configure_preset_army(session, city, preset_key)
    else:
        # Custom army
        return configure_custom_army(session, city)


def configure_preset_army(session, city, preset_key):
    """Configure army based on preset"""
    preset = PRESET_ARMIES[preset_key]

    banner()
    print(f"📋 {preset['name']}")
    print()

    # Get available units
    available_units = get_units(session, city)

    # Check if we have enough units
    army_config = {
        'army': preset['army'].copy(),
        'looting': preset['looting'].copy(),
        'type': 'preset',
        'name': preset['name']
    }

    print("Required units:")
    missing_units = []
    for unit_id, required in preset['army'].items():
        available = available_units.get(unit_id, {'amount': 0, 'name': f'Unit {unit_id}'})
        status = "✅" if available['amount'] >= required else "❌"
        print(f"  {available['name']}: {required} required, {available['amount']} available {status}")

        if available['amount'] < required:
            missing_units.append(unit_id)

    print()

    if missing_units:
        print("⚠️ You don't have enough units for this preset!")
        print("Options:")
        print("(1) Use what you have available (may be less effective)")
        print("(2) Choose different preset")
        print("(0) Exit")

        option = read(min=0, max=2, digit=True, msg=prompt)
        if option == 0:
            return None
        elif option == 2:
            return None  # Will return to preset selection
        else:
            # Adjust army to available units
            for unit_id in army_config['army']:
                available = available_units.get(unit_id, {'amount': 0})['amount']
                army_config['army'][unit_id] = min(army_config['army'][unit_id], available)

    return army_config


def configure_custom_army(session, city):
    """Configure custom army composition"""
    banner()
    print("🎨 Custom Army Configuration")
    print()

    available_units = get_units(session, city)
    if not available_units:
        print("No units available in this city!")
        return None

    print("Available units:")
    unit_list = []
    for unit_id, unit_info in available_units.items():
        if unit_info['amount'] > 0:
            unit_list.append((unit_id, unit_info))
            print(f"  {unit_info['name']}: {unit_info['amount']} available")
    print()

    army_config = {
        'army': {},
        'looting': {},
        'type': 'custom',
        'name': 'Custom'
    }

    print("Configure your attack army:")
    print("(Enter 0 to skip a unit type)")
    for unit_id, unit_info in unit_list:
        max_amount = unit_info['amount']
        if max_amount > 0:
            amount = read(
                min=0,
                max=max_amount,
                digit=True,
                msg=f"{unit_info['name']} (max {max_amount}): ",
                default=0
            )
            if amount > 0:
                army_config['army'][unit_id] = amount

    if not army_config['army']:
        print("No units selected for attack!")
        return None

    print()
    print("Configure looting army (units to collect resources after victory):")
    remaining_units = {}
    for unit_id, unit_info in unit_list:
        used_in_attack = army_config['army'].get(unit_id, 0)
        remaining = unit_info['amount'] - used_in_attack
        if remaining > 0:
            remaining_units[unit_id] = {'amount': remaining, 'name': unit_info['name']}

    for unit_id, unit_info in remaining_units.items():
        max_amount = unit_info['amount']
        amount = read(
            min=0,
            max=max_amount,
            digit=True,
            msg=f"{unit_info['name']} (max {max_amount}): ",
            default=min(20, max_amount)  # Default to small looting force
        )
        if amount > 0:
            army_config['looting'][unit_id] = amount

    return army_config


def configure_safety_options():
    """Configure safety and stopping options"""
    banner()
    print("🛡️ Safety Options")
    print()

    safety_margin = read(
        min=0,
        max=5,
        digit=True,
        msg="Safety margin (stop X levels before max level, 0-5): ",
        default=1
    )

    min_ships = read(
        min=3,
        max=10,
        digit=True,
        msg="Minimum ships to keep available (3-10): ",
        default=3
    )

    return {
        'safety_margin': safety_margin,
        'min_ships': min_ships
    }


def display_army_summary(army, session, city):
    """Display army composition summary"""
    units_data = {}
    for unit_id in army.keys():
        units_data[unit_id] = get_unit_data(session, city["id"], str(unit_id))

    for unit_id, amount in army.items():
        unit_name = units_data[unit_id]['name']
        print(f"  • {amount} {unit_name}")


def run_simple_auto_grind(session, island, city, max_level, army_config, safety_config, ship_capacity):
    """Main grinding loop"""
    attempts = 0
    max_attempts = 50  # Prevent infinite loops

    sendToBot(session, f"🗡️ Started Simple Auto Grind on [{island['x']}:{island['y']}]")

    while attempts < max_attempts:
        attempts += 1

        try:
            # Wait between attempts (except first)
            if attempts > 1:
                session.setStatus("Waiting 5 minutes before next check...")
                time.sleep(300)  # 5 minutes

            # Check current barbarian status
            html = session.get(island_url + island["id"])
            island = getIsland(html)
            barbarians_info = get_barbarians_lv(session, island, ship_capacity)
            current_level = int(barbarians_info["level"])

            session.setStatus(f"Checking barbarians (Level {current_level})")

            # Check stop condition
            stop_level = max_level - safety_config['safety_margin']
            if current_level > stop_level:
                msg = f"🛑 Barbarians reached level {current_level} (stop threshold: {stop_level}). Stopping grind."
                sendToBot(session, msg)
                break

            # Check if barbarians are destroyed (ready for looting)
            if island["barbarians"]["destroyed"] == 1:
                session.setStatus("Looting remaining resources...")
                execute_looting(session, island, city, army_config, ship_capacity)
                continue

            # Validate we have enough troops
            if not validate_army_available(session, city, army_config['army']):
                msg = f"🛑 Insufficient troops in {city['name']}. Stopping grind."
                sendToBot(session, msg)
                break

            # Check ship availability
            ships_available = waitForArrival(session)
            if ships_available < safety_config['min_ships']:
                session.setStatus(f"Waiting for ships (need {safety_config['min_ships']}, have {ships_available})")
                continue

            # Execute attack
            session.setStatus(f"Attacking barbarians (Level {current_level})")
            sendToBot(session, f"⚔️ Attacking Level {current_level} barbarians on [{island['x']}:{island['y']}]")

            execute_simple_attack(session, island, city, army_config, ship_capacity)
            wait_until_attack_is_over(session, city, island)

        except Exception as e:
            error_msg = f"Error in grinding loop: {str(e)}"
            sendToBot(session, error_msg)
            session.setStatus("Error occurred, waiting before retry...")
            time.sleep(300)  # Wait 5 minutes on error

    # Final message
    if attempts >= max_attempts:
        sendToBot(session, "🛑 Simple Auto Grind stopped due to maximum attempts reached.")
    else:
        sendToBot(session, "✅ Simple Auto Grind completed successfully.")


def validate_army_available(session, city, army):
    """Check if we have sufficient troops for the attack"""
    available_units = get_units(session, city)

    for unit_id, required in army.items():
        available = available_units.get(unit_id, {'amount': 0})['amount']
        if available < required:
            return False
    return True


def execute_simple_attack(session, island, city, army_config, ship_capacity):
    """Execute a simple single-wave attack"""
    # Prepare base attack data
    attack_data = {
        "action": "transportOperations",
        "function": "attackBarbarianVillage",
        "actionRequest": actionRequest,
        "islandId": island["id"],
        "destinationCityId": 0,
        "barbarianVillage": 1,
        "backgroundView": "island",
        "currentIslandId": island["id"],
        "templateView": "plunder",
        "ajax": 1,
        "transporter": 0,
    }

    # Add all unit types with default values
    unit_upkeep = {
        301: 3, 302: 4, 303: 3, 304: 3, 305: 30, 306: 25, 307: 15,
        308: 45, 309: 45, 310: 10, 311: 20, 312: 15, 313: 30, 315: 1
    }

    for unit_id in range(301, 316):
        attack_data[f"cargo_army_{unit_id}"] = 0
        attack_data[f"cargo_army_{unit_id}_upkeep"] = unit_upkeep.get(unit_id, 1)

    # Set actual army amounts and calculate weight
    total_weight = 0
    units_data = {}

    for unit_id, amount in army_config['army'].items():
        unit_id_str = str(unit_id)
        attack_data[f"cargo_army_{unit_id}"] = amount

        # Get unit data for weight calculation
        if unit_id_str not in units_data:
            units_data[unit_id_str] = get_unit_data(session, city["id"], unit_id_str)

        total_weight += amount * units_data[unit_id_str]['weight']

    # Calculate ships needed (minimum 1, plus extra for weight)
    ships_needed = max(1, int(total_weight / ship_capacity) + 1)
    attack_data["transporter"] = ships_needed

    # Send attack
    session.post(params=attack_data)


def execute_looting(session, island, city, army_config, ship_capacity):
    """Execute looting after barbarians are destroyed"""
    if not army_config['looting']:
        return  # No looting army configured

    # Prepare base attack data for looting
    attack_data = {
        "action": "transportOperations",
        "function": "attackBarbarianVillage",
        "actionRequest": actionRequest,
        "islandId": island["id"],
        "destinationCityId": 0,
        "barbarianVillage": 1,
        "backgroundView": "island",
        "currentIslandId": island["id"],
        "templateView": "plunder",
        "ajax": 1,
        "transporter": 0,
    }

    # Add all unit types with default values
    unit_upkeep = {
        301: 3, 302: 4, 303: 3, 304: 3, 305: 30, 306: 25, 307: 15,
        308: 45, 309: 45, 310: 10, 311: 20, 312: 15, 313: 30, 315: 1
    }

    for unit_id in range(301, 316):
        attack_data[f"cargo_army_{unit_id}"] = 0
        attack_data[f"cargo_army_{unit_id}_upkeep"] = unit_upkeep.get(unit_id, 1)

    # Set looting army amounts and calculate weight
    total_weight = 0
    units_data = {}

    for unit_id, amount in army_config['looting'].items():
        unit_id_str = str(unit_id)
        attack_data[f"cargo_army_{unit_id}"] = amount

        # Get unit data for weight calculation
        if unit_id_str not in units_data:
            units_data[unit_id_str] = get_unit_data(session, city["id"], unit_id_str)

        total_weight += amount * units_data[unit_id_str]['weight']

    # Calculate ships needed (prioritize cargo capacity for looting)
    ships_available = waitForArrival(session)
    ships_needed = min(ships_available - 2, max(3, int(total_weight / ship_capacity) + 5))
    attack_data["transporter"] = ships_needed

    # Send looting attack
    session.post(params=attack_data)

    # Wait for looting to complete
    wait_for_arrival(session, city, island)