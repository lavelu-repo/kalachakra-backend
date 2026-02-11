# kalachakra-backend

This is description

---

### Summary of the File Naming System

The Swiss Ephemeris splits history into 600-year blocks to keep file sizes manageable. The files are named by category and century. For a standard project covering the years 1800 AD – 2399 AD, you only need these core binary files:

- Planets: `sepl_18.se1` (covers 1800–2399 AD).
- Moon: `semo_18.se1` (high-precision lunar data).
- Main Asteroids: `seas_18.se1` (includes Ceres, Pallas, Juno, Vesta, and Chiron).
- Fictitious/Nodes: `sefplan.se1` (required for certain nodes and fictitious planets).

| File Suffix | Date Range (Approx) | Use Case                       |
| ----------- | ------------------- | ------------------------------ |
| \_m06       | 600 BCE to 1 BCE    | Ancient History / Biblical     |
| \_00        | 1 CE to 599 CE      | Classical Era                  |
| \_06        | 600 CE to 1199 CE   | Medieval Era                   |
| \_12        | 1200 CE to 1799 CE  | Renaissance / Early Modern     |
| \_18        | 1800 CE to 2399 CE  | Current Era (The standard set) |
| \_24        | 2400 CE to 2999 CE  | Far Future                     |

---

### Summary of Common Ayanamsa Modes

| Mode                   | Name                   | Usage                    |
| ---------------------- | ---------------------- | ------------------------ |
| swe.SIDM_FAGAN_BRADLEY | Fagan/Bradley          | Western Sidereal         |
| swe.SIDM_LAHIRI        | Lahiri (Chitra Paksha) | Official Indian/Vedic    |
| swe.SIDM_RAMAN         | Raman                  | Specific Vedic tradition |
| swe.SIDM_KP            | Krishnamurti (KP)      | KP System astrology      |
| swe.SIDM_USER          | User-defined           | Custom degree offset     |

---
