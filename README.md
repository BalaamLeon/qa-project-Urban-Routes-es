# Proyecto Urban Routes

> - Alumno: **Balaam Jesús Delgadillo León**
> - Grupo: **19**
> - Sprint: **8**

## Descripción

Automatización de pruebas para el proceso de reservación de taxi con tarifa *Comfort*, en la aplicación **Urban Routes**.


## Requisitos

Para ejecutar estas pruebas, asegúrate de tener instalados Python y las librerías necesarias:

1. Instala [Python](https://www.python.org/downloads/) en tu sistema si aún no lo tienes.
2. Instala el controlador WebDriver de Chrome:
   <details>
   <summary>Instrucciones para descargar WebDriver</summary>
   
   - Descarga WebDriver a través de [este enlace](https://googlechromelabs.github.io/chrome-for-testing/). 
   - Busca la línea con la versión de Chromedriver que coincida con la versión de tu navegador y de tu sistema operativo.
      Necesitas la versión que coincida con la versión de tu navegador, al menos la parte antes del primer punto. 
      Por ejemplo, si la versión de tu navegador es <code>102.0.5005.115</code>, funcionarán tanto la versión 
      <code>102.0.5005.27</code> como la <code>102.0.5005.61</code> del controlador. 
      Si no puedes encontrar ninguna coincidencia, descarga la última versión estable. 
      Para averiguar tu versión de Chrome, abre el navegador. Pega <code>chrome://settings/help</code> en la barra de 
      direcciones y presiona Enter. Verás la versión de tu navegador en la nueva ventana. En la segunda columna de la 
      tabla, puedes ver diferentes sistemas operativos: Linux, mac o win para Windows. 
   - Copia el enlace al Chromedriver que seleccionaste y pégalo en la pestaña del navegador; debería comenzar a 
      descargarse automáticamente.
   - Descomprime el archivo. Crea una carpeta llamada <code>WebDriver/bin</code> y guarda el archivo allí. 
   - Agrega la ruta de <code>bin</code> a la variable de entorno <code>PATH</code>. 
      El algoritmo depende del sistema operativo:
   
      > **Para Windows**
      > 
      > Abre el Panel de control. Ve a Sistema → Configuración avanzada del sistema → Variables de entorno. 
      > Edita la variable del sistema <code>PATH</code> agregando la ruta a <code>bin</code>. 
      > Por ejemplo: <code>C:\\\\WebDriver\\\\bin</code>. 

      > **Para MacOS y Linux**
      > 
      > Abre la terminal <code>bin</code> A continuación te mostramos un ejemplo:
      > ```shell
      > export PATH=/Users/<username>/Downloads/WebDriver/bin:$PATH
      > ```
   
   Si planeas descargar WebDriver para otros navegadores y sus versiones, 
   guarda todos los archivos en la misma carpeta: <code>WebDriver/bin</code>. 
   De esta manera, no tendrás que editar <code>PATH</code> de nuevo.
   </details>

3. Abre una terminal y ejecuta los siguientes comandos para instalar las librerías necesarias:
    ```shell
    pip install selenium
    pip install pytest   
    ```

## Ejecución de pruebas

Para ejecutar las pruebas de este proyecto:

1. Abre una terminal en la raíz del proyecto.
2. Usa el siguiente comando para ejecutar todas las pruebas:
    ```shell
    pytest test.py
    ```

3. Los resultados de las pruebas se mostrarán directamente en la terminal, indicando si cada prueba pasó o falló, junto con detalles adicionales en caso de errores.