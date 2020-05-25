# Snake Game
Programa realizado en Python para emular el juego de Snake, con inteligencia
artificial por medio de algoritmos geneticos

## ADN
Comenzamos con 4 sensores, que detentan 4 estados en cada celda y 3 acciones
para cada snake
### Estados
```
00 Celda Vacia
01 Snake
10 Cereza
11 Muro
```
### Acciones
```
00 Avanzar
01 Girar Derecha
10 Girar Izquierda
11 Avanzar
```
### Sensores
```
000XX0000 Sensor izquierdo
00000XX00 Sensor frontal
0000000XX Sensor derecho
XXX000000 Cherry orientacion
```
### Cromosoma
Tres sensores de 2 bit mas 1 de 3 bit nos generan 2⁹ entradas, por los 2 bit de las
acciones nos da un total de 128 bit para el cromosoma


#### Links
https://chrispresso.github.io/AI_Learns_To_Play_Snake
https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/