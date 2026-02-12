# kalachakra-backend

Astronomical & Vedic astrology calculation API.

KalaChakra provides tropical and sidereal planetary positions, lunar nodes, equatorial coordinates, retrograde detection, and advanced Sadbala (ஷட்பலம்) planetary strength calculations through a modern FastAPI backend.

---

## 🚀 Features

### 🌍 Astronomical Calculations

- Geocentric & Heliocentric modes
- Ecliptic longitude, latitude, distance
- Planetary speed (retrograde detection)
- Right Ascension & Declination
- True Node & Mean Node (Rahu/Ketu)
- ~0.001° precision using Swiss Ephemeris

### 🕉 Zodiac Systems

- Tropical zodiac (default)
- Sidereal zodiac (configurable)
- Configurable Ayanamsa modes

### 📿 Vedic Astrology Support

- Full Shadbala (ஷட்பலம்) computation
- Rahu/Ketu support
- Sidereal ayanamsa configuration
- Vedic-compatible planetary motion calculations

---

## 🏗 Tech Stack

- Python
- FastAPI
- Pydantic Settings
- Swiss Ephemeris https://github.com/aloistr/swisseph

---

## 📦 Swiss Ephemeris Data Files

Swiss Ephemeris divides historical data into 600-year blocks.
For modern astrology (1800 CE – 2399 CE), you need:

| Category           | File        |
| ------------------ | ----------- |
| Planets            | sepl_18.se1 |
| Moon               | semo_18.se1 |
| Main Asteroids     | seas_18.se1 |
| Nodes / Fictitious | sefplan.se1 |

Place these files inside:

```bash
./app/ephe/
```

---

## 📅 File Suffix Reference

| Suffix | Date Range        | Use Case    |
| ------ | ----------------- | ----------- |
| \_m06  | 600 BCE – 1 BCE   | Ancient     |
| \_00   | 1 CE – 599 CE     | Classical   |
| \_06   | 600 CE – 1199 CE  | Medieval    |
| \_12   | 1200 CE – 1799 CE | Renaissance |
| \_18   | 1800 CE – 2399 CE | ✅ Standard |
| \_24   | 2400 CE – 2999 CE | Future      |

---

## 🌍 Geocentric vs ☀️ Heliocentric

KalaChakra supports both coordinate systems.

### 🌍 Geocentric (Default)

Planetary positions are calculated as observed from Earth.

Used in:

- Western astrology
- Vedic astrology
- Natal charts
- Transit analysis
- Shadbala calculations

Default behavior:

- geocentric = true
- Retrograde motion appears naturally
- Houses and ascendant are meaningful

### ☀️ Heliocentric

Planetary positions are calculated relative to the Sun.

Used mainly in:

- Astronomical research
- Orbital mechanics
- Modern heliocentric astrology

Important notes:

- No apparent retrograde motion
- Houses are not applicable
- Lunar nodes are not physically meaningful heliocentrically

---

## 🚀 Getting Started (Local Dev)

#### 1. Clone the Repo

```bash
git clone https://github.com/lavelu-profile/kalachakra-backend.git
```

#### 2. Create and Activate a Python Virtual Environment

```bash
uv venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
uv sync
```

#### 4. Setup the environment variables

```bash
APP_HOST=0.0.0.0
APP_PORT=8000
APP_RELOAD=true
EPHEMERIS_PATH=./ephe
ZODIAC_TYPE=sidereal
AYANAMSA=LAHIRI
USE_TRUE_NODE=True
```

#### 5. Run the Backend Server

```bash
python -m app.main
```

---
