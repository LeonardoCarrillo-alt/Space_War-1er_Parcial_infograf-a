# Space War

Space War es un videojuego desarrollado en **Python** con la librería **Arcade**, donde el jugador controla una nave espacial y debe enfrentarse a oleadas de enemigos alienígenas a lo largo de distintos niveles.  
El juego incluye soporte tanto para **teclado** como para **mando (gamepad)**.

---

## Características principales
- Niveles progresivos de dificultad (Nivel 1, Nivel 2, ...).
- Detección y destrucción de enemigos mediante disparos.
- Sistema de puntuación y tiempo límite.
- Explosiones animadas con efectos de sonido.
- Game Over y pantallas de transición entre niveles.
- Soporte para **controlador (joystick/gamepad)**.

---

## Controles

### Teclado
- **← / →** → Mover la nave.
- **Espacio** → Disparar.

### Gamepad 
- **Stick izquierdo (eje X)** → Mover la nave.
- **Botón A / X / 0** → Disparar.

---

## ⚙️ Requisitos
- Python **3.8+**
- Librerías:
  - [arcade](https://api.arcade.academy/en/latest/)
  - random (incluida en Python estándar)
  - time (incluida en Python estándar)

Instala arcade con:
```bash
pip install arcade
