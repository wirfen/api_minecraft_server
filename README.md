﻿# Api Minecraft Server
 Esta aplicación te permitira controlar un servidor de Minecraft con sencillas llamadas API Rest.
 ## Caracteristicas
 * Instalar/Actualizar la version del servidor de Minecraft
 * Gestionar el servidor:
   * Parar, iniciar o reiniciar el servidor.
   * Ver el estado y jugadores activos.
   * Enviar un mensaje.
   * Cambiar el clima y la hora dentro del juego.
 * Gestionar a los jugadores:
   * Añadir/Remover de la Whitelist.
   * Añadir/Remover como operador.
   * Cambiar su modo de juego (Survival, Creative, Spectator)
   * Kickear o dis/banear al jugador.
   * Proporcionarle distintos objetos iniciales.
 * Mapas:
   * Ver listado de mapas y backups.
   * Hacer backups.
   * Descargar un mapa.
   * Restaurar un mapa.
   * Cambiar de mapa.
   * Borrar mapas y backups
   * Ver y editar el archivo de propiedades.

## Primeros pasos
 Podemos instalarlo de dos formas:
 * Servidor dentro de nuestra maquina:
   Hola
 * Servidor dentro de un contenedor de Docker:  
Nos descargamos la imagen del repositorio de Docker:  
  ``` docker
  docker pull wirfen/minecraftserver
  ```
Una vez descargada la imagen, la ejecutamos:  
  ``` docker
  docker run -d -p 12345:12345 -p 25565:25565 --name minecraft wirfen/minecraftserver
  ```
