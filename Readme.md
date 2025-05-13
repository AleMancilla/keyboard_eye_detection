# Teclado Virtual Controlado con la Mirada 👁️🕹️

Una solución open-source de visión por computadora que detecta la dirección de la mirada en tiempo real y la traduce en pulsaciones de “joystick” para controlar un teclado virtual. Ideal para devolver independencia y autonomía a personas con movilidad reducida.

---

## 🔍 Descripción

utiliza un modelo de Computer Vision entrenado con un dataset personalizado para interpretar hacia dónde mira el usuario (arriba, abajo, izquierda, derecha o centro). A partir de esa información:

1. **Procesa** cada fotograma de vídeo (webcam o cámara integrada).  
2. **Predice** la dirección de la mirada en tiempo real.  
3. **Simula** eventos de teclado o movimientos de cursor como si fuesen “joystick” basados en esa dirección.  

---

## 🚀 Características principales

- Detección de mirada en 6 estados (
    arriba, abajo, izquierda, derecha, centro  y cerrado
).  
- Control de teclado virtual sin necesidad de hardware EEG.  

---

## 🤝 Contribuciones
¡Todas las contribuciones son bienvenidas! Si quieres:

- Proponer mejoras al modelo o al dataset.

- Añadir soporte para más gestos o ángulos de mirada.

- Integrar con otras aplicaciones o frameworks.

Abre un issue o crea un pull request en GitHub.

## 📄 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## 🔗 Enlaces útiles
📂 Dataset: https://universe.roboflow.com/alemancilla/eye_direction

📑 Modelo y dataset: en el codigo archivo best.pt


<video width="640" height="360" controls>
  <source src="HACKATHON/demo.mp4" type="video/mp4">
  Tu navegador no soporta la etiqueta de video.
</video>