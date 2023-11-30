Trabajo final Prog-II
Constaba en desarrollar una simulación de un ecosistema

Nuestro trabajo consta de
Una "Simulación" de un bosque, existen las entidades plantas, herviboros y carnivoros, estás son representadas por clases que toman el valor de un png, cada clase tiene varias
opciones de png a tomar, para así intentar demostrar o identificarlos como lo que supuestamente son, el algoritmo cuenta con algunos eventos, como la lluvia, meteorito, incendio, le dimos png para darles forma para cumplir con las cantidades de especies de clases especificadas en la pauta, las clases cuentan con un radio, energia y funciones como, comer, moverse, reproducirse, cada clase y funcion con sus respectivas variables para el correcto funcionamiento, el ciclo es infinito debido a ciertas caracteristicas
de el algoritmo que ayudaban a que el algoritmo no de error al quedarse una clase sin entidades.

El código proporcionado implementa un ecosistema simple en Pygame, donde las plantas, herbívoros y carnívoros interactúan entre sí. A continuación, se presenta una descripción general del funcionamiento y los elementos clave del código:
Configuración inicial:

Pygame se inicializa y se configuran diversas constantes, colores, y la fuente para mostrar información en pantalla.
Se define un área de juego de dimensiones width por height.

Clases de Organismos:
Plant: Representa a las plantas en el ecosistema. Tienen una energía asociada y pueden reproducirse.
Herbivore: Representa a los herbívoros que se alimentan de plantas. Se desplazan hacia las plantas más cercanas, se reproducen y pueden morir si su energía llega a cero.
Carnivore: Representa a los carnívoros que se alimentan de herbívoros. Se desplazan hacia los herbívoros más cercanos, se reproducen y también pueden morir si su energía es insuficiente.
Meteorite: Representa la posibilidad de eventos catastróficos en el ecosistema, eliminando organismos en un área de impacto.
Fire: Representa un evento de incendio forestal que afecta a los organismos en su radio y reduce la energía de las plantas y elimina herbívoros y carnívoros.

Grupos de Sprites:
Se crean grupos para cada tipo de organismo (plantas, herbívoros, carnívoros, meteoritos, fuegos, gotas de lluvia).
Los grupos facilitan la actualización y dibujo eficiente de los sprites en pantalla(los usamos al principio para darles color a las clases e identificarlas pero les terminamos por dar la forma de los .png respectivos).

Inicialización del Ecosistema:
Se crean inicialmente 100 plantas, 20 herbívoros y 10 carnívoros en ubicaciones aleatorias.

Bucle Principal del Juego:
El bucle principal maneja eventos, actualiza los grupos de sprites, y dibuja en pantalla.
Se implementa una probabilidad de crear nuevas plantas en cada iteración del bucle(esto devido a que siempre se nos terminaba por extinguir alguna especie).

Eventos del Teclado:
Al presionar la tecla 'A', se genera un evento de lluvia que afecta positivamente a las plantas.
Al presionar la tecla 'ESPACIO', se genera un evento de incendio forestal que afecta negativamente a plantas, herbívoros y carnívoros en un área específica.

Meteorito y Contador de Ciclos:
Se utiliza un meteorito que cae cada 10 ciclos, eliminando organismos en su área de impacto.
Un contador de ciclos lleva el seguimiento del tiempo transcurrido en ciclos de juego.

Lógica de Interacción:
Los herbívoros se desplazan hacia las plantas más cercanas, se reproducen y pueden morir por falta de energía.
Los carnívoros se desplazan hacia los herbívoros más cercanos, se reproducen y pueden morir por falta de energía.
Las plantas pueden reproducirse y mueren si su energía llega a cero.
Los eventos de incendio y lluvia afectan a los organismos en sus áreas respectivas.

Prevención de Extinciones:
Se implementa lógica en las funciones de reproducción para asegurar que siempre haya al menos dos organismos de cada tipo después de la reproducción.

Pantalla de Estadísticas:
Se muestra información en pantalla, incluyendo el número de plantas, herbívoros, carnívoros y el número de ciclos transcurridos.

Cierre del Programa:
El programa se cierra al cerrar la ventana de Pygame.
Este código simula la interacción básica entre plantas, herbívoros y carnívoros en un ecosistema, con eventos ocasionales de meteoritos, incendios y lluvias que afectan dinámicamente a la población.

Tutorial de uso:
Primero muy importante tener las librerias a usar instaladas(pygame, random, math y time)
Segundo y tambien muy importante, estar en la ruta de el archivo .py, osea dentro de la carpeta "Ecosistema-Prog-II", para que al ejecutarse se tomen las rutas de las imagenes y se puedan usar correctamente, osino el codigo dará error.
Tercero, ejecutar y ponerlo a prueba, con sus eventos y infinitas posibilidades a pasar!

Patricio Quiroz R.
Bryam con eme.