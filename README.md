<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#current-state">Current State</a></li>
        <li><a href="#future-state">Future State</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

I wanted to give Object-Oriented Programming a go on my own before taking the course this coming semester. Independent Study Period was the perfect opportunity to do that and get credit for it as well. I decided to implement an Agent based Sugarscape in Python to get some OOP experience.

I covered some topics of Sugarscape and some topics of OOP throughout this ISP and got to make some design choices on my own for the first time.

Sugarscape topics covered:
* The Environment (The Sugarscape)
  - Resource Distribution
  - Resource Regeneration
    
* Agents
  - Searching, Moving, Eating
  - Reproducing

OOP topics covered:
* Classes - Created classes for the environment, agents, and grid cells.
* Objects - Agents and cells were treated as objects.
* Encapsulation - Cell and Agent information is limited to its own class unless needed.
* Inheritance - A special Agent that can reproduce inherited from the Agent class. 
* Polymorphism - The special Agent inherits the ability to update from Agent parent class but has unique updates as well.

### Current State

The current state of my Sugarscape is basic. Although the Sugarscape content is basic, I got to learn and practice many
OOP topics during this ISP. There are some issues with changing the grid dimensions. The way I scale the agent sprites
doesn't work for higher grid dimensions.

Environment:
* Map
* Cell
  - Current Sugar
  - Maximum Sugar
  - Regen Rate
  - Current Agent

Agents:
* Agent
  - Look
  - Move
  - Eat
  - Die
* Reproductive Agent
  - Everything Agent does
  - Reproduce

### Future State

In the future I there is plenty to add for Sugarscape. Alongside Sugarscape content I could add graphs and such to
visualize population state for Agents. Sugarscape can end up being a decently sized project and I barely scratched the
surface of it. I should also give Agents and Cells less information to better follow the OOP practice of encapsulation. 



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python3
    - PyGame module



<!-- USAGE EXAMPLES -->
## Usage

To run the program enter `python3 sugarscape.py` into the terminal.

Some properties of the simulation can be modified in the settings.py file:
* Grid Width/Height
* Window Resolution
* Number of Agents and Reproductive Agents
* Simulation Speed (FPS)

To pause/resume the simulation press the space key:
![pause/resume]

Example 400 Agents at 10 FPS:
![example1]

Example 20 Agents and 5 Reproductive Agents at 5 FPS:
![example2]



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [KidsCanCode (Pygame Tutorials)](http://kidscancode.org/)
* [README Template](https://github.com/othneildrew/Best-README-Template)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png
[pause/resume]: images/pauseresume.gif
[example1]: images/example1.gif
[example2]: images/example2.gif
