import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np


def create_space_trader_flowchart():
    fig, ax = plt.subplots(1, 1, figsize=(14, 18))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 22)
    ax.axis('off')

    # Title
    ax.text(6, 21, 'Space Trader Game Logic Flow', fontsize=18, fontweight='bold', ha='center')

    # Define box style
    box_style = "round,pad=0.15"

    # Game states with positions and colors
    states = [
        # Core Game Loop
        (6, 19.5, "GAME START\nAge: 30, Credits: 1000\nEngine: 1, Hold: 5, Shields: 1, Weapons: 1", 'lightgreen', 3.5,
         1),
        (6, 17.5, "CELASTRA EXCHANGE\n(Main Hub)", 'lightblue', 3, 1),

        # Exchange Options
        (2, 15.5, "Buy/Sell\nGoods", 'lightyellow', 1.5, 0.8),
        (4.5, 15.5, "Ship\nUpgrades", 'lightyellow', 1.5, 0.8),
        (7, 15.5, "Ship\nComputer", 'lightyellow', 1.5, 0.8),
        (9.5, 15.5, "Casino/\nBounty Office", 'lightyellow', 1.5, 0.8),

        # Exploration Branch
        (6, 13.5, "LAUNCH SHIP\nSpace Exploration\n(1-4 encounters based on engine)", 'orange', 4, 1),

        # Encounter Types
        (2, 11.5, "PIRATE\nATTACK", 'red', 1.5, 0.8),
        (4.5, 11.5, "SPACE\nTRADER", 'yellow', 1.5, 0.8),
        (7.5, 11.5, "PLANET\nLANDING", 'lightgreen', 1.5, 0.8),
        (10, 11.5, "EMPTY\nSPACE", 'lightgray', 1.5, 0.8),

        # Combat Resolution
        (2, 9.5, "COMBAT\nWeapons vs Pirates\nShields for Defense", 'orange', 2, 1),

        # Combat Outcomes
        (0.5, 7.5, "VICTORY\nEarn Bounty\nPoints", 'lightgreen', 1.5, 1),
        (2, 7.5, "ESCAPE\nShip Damage\nStat Reduction", 'yellow', 1.5, 1),
        (3.5, 7.5, "DEFEAT\nLose Goods\nShip Damage", 'red', 1.5, 1),

        # Planet Outcomes
        (7.5, 9.5, "PLANET EVENTS", 'lightgreen', 2, 0.8),
        (6, 7.5, "Planet Encounter\nRewards Player Choice", 'lightgreen', 1.8, 0.8),
        (8, 7.5, "Planet Pirate\nSame as in Space", 'red', 1.5, 0.8),
        (9.5, 7.5, "Planet Trader\nNo Tax/Limits", 'yellow', 1.5, 0.8),

        # Trading Details
        (4.5, 9.5, "TRADING\nNo Exchange Limits\nNo Trade Tax", 'yellow', 2.5, 1),

        # Return to Exchange
        (6, 5.5, "RETURN TO EXCHANGE\nPay Docking Fee (20 credits)\nAge +1 Year", 'lightblue', 4, 1),

        # End Conditions
        (6, 3.5, "AGE CHECK\nAge >= 60?", 'purple', 2, 0.8),
        (3, 1.5, "CONTINUE\nNext Turn", 'lightblue', 2, 0.8),
        (9, 1.5, "RETIREMENT\nFinal Score\nGame Over", 'gray', 2.5, 1),
    ]

    # Draw all boxes
    for state in states:
        x, y, text, color = state[:4]
        width = state[4] if len(state) > 4 else 2
        height = state[5] if len(state) > 5 else 0.8

        box = FancyBboxPatch((x - width / 2, y - height / 2), width, height,
                             boxstyle=box_style,
                             facecolor=color,
                             edgecolor='black',
                             linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold', wrap=True)

    # Define connections with arrows
    connections = [
        # Main flow
        (6, 19, 6, 18),  # Start to Exchange
        (6, 17, 6, 14),  # Exchange to Launch
        (6, 13, 2, 12),  # Launch to Pirate
        (6, 13, 4.5, 12),  # Launch to Trader
        (6, 13, 7.5, 12),  # Launch to Planet
        (6, 13, 10, 12),  # Launch to Empty

        # Combat flow
        (2, 11, 2, 10),  # Pirate to Combat
        (2, 9, 0.5, 8),  # Combat to Victory
        (2, 9, 2, 8),  # Combat to Escape
        (2, 9, 3.5, 8),  # Combat to Defeat

        # Planet flow
        (7.5, 11, 7.5, 10),  # Planet to Events
        (7.5, 9, 6, 8),  # Events to Boon
        (7.5, 9, 8, 8),  # Events to Pirate
        (7.5, 9, 9.5, 8),  # Events to Trader

        # Trader flow
        (4.5, 11, 4.5, 10),  # Space Trader to Trading

        # Return flow
        (6, 6, 6, 4),  # Return to Age Check
        (6, 3, 3, 2),  # Age Check to Continue (No)
        (6, 3, 9, 2),  # Age Check to Retirement (Yes)
        (3, 1, 6, 17),  # Continue back to Exchange (curved)
    ]

    # Draw arrows
    for x1, y1, x2, y2 in connections:
        if x1 == 3 and y1 == 1 and x2 == 6 and y2 == 17:
            # Special curved arrow for game loop
            ax.annotate('', xy=(x2 - 2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle='->', lw=2, color='blue',
                                        connectionstyle="arc3,rad=-0.8"))
        else:
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))

    # Add key game mechanics as text boxes
    mechanics_text = [
        "KEY MECHANICS:",
        "• Engine determines encounters per turn (1-4)",
        "• Hold limits cargo capacity",
        "• Weapons improve combat success",
        "• Shields help escape/defend",
        "• Exchange traders limited per visit",
        "• Planet traders unlimited & no tax",
        "• Trade tax (5cr) only at exchange",
        "• Docking fee (20cr) per return",
        "• Game ends at age 60"
    ]

    for i, text in enumerate(mechanics_text):
        style = 'bold' if i == 0 else 'normal'
        ax.text(0.5, 20.5 - i * 0.3, text, fontsize=9, fontweight=style, ha='left')

    # Add legend
    legend_elements = [
        mpatches.Patch(color='lightblue', label='Core Game States'),
        mpatches.Patch(color='lightyellow', label='Exchange Activities'),
        mpatches.Patch(color='orange', label='Exploration/Combat'),
        mpatches.Patch(color='red', label='Hostile Encounters'),
        mpatches.Patch(color='yellow', label='Trading'),
        mpatches.Patch(color='lightgreen', label='Beneficial Events'),
        mpatches.Patch(color='lightgray', label='Neutral/End States')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.85))

    plt.tight_layout()
    plt.savefig('space_trader_game_logic.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show()

    print("Space Trader game logic flowchart saved as 'space_trader_game_logic.png'")


# Create the flowchart
create_space_trader_flowchart()
