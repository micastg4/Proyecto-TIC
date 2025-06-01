# Comparativa entre Máquina Virtual y Docker

## Introducción

### Máquinas Virtuales
Son una emulación de un sistema físico hecha para ejecutar un sistema operativo anfitrión. Esto requiere siempre un hipervisor (por ejemplo VirtualBox), el cual asigna los recursos necesarios a la máquina.

### Contenedores (Docker)
Es una unidad de software la cual empaqueta una aplicación y todas sus dependencias, pero que usa el kernel del sistema operativo en el que esté. Es conocido debido a que es muy sencillo para instalar y usar aplicaciones en éste.

## Explicación por la falta de datos

Debido a varios factores me atrasé mucho a la hora de crear el entorno de prueba, y solo he llegado a crear algo mínimamente funcional.

Por una parte, malinterpreté parte del trabajo y acabé teniendo problemas con mi máquina virtual de Ubuntu y con mi propio ordenador, así que decidí hacer que funcionara todo en un Codespace.

Por otra parte, tenía planeado usar Neo4j para el trabajo, pero costaba mucho hacer que siquiera funcionara en el Codespace, haciendo que lo considerase imposible y pasase a intentarlo con MySQL. De todas formas, el Codespace me resultó más complicado de lo que podría haber sido y me gastó muchísimo tiempo, haciéndome incapaz de hacer pruebas claras.

En el último día de la entrega me doy cuenta de que Codespace se parece más a Docker que a una máquina virtual y que he estado malinterpretando las presentaciones en las que se mostraba el trabajo en un Codespace.

Aún no entiendo por qué Neo4j no funcionó, pero he visto que más personas han mencionado que Neo4j no funciona bien en un Codespace. Aun así, ninguno me ha dado respuesta del por qué.

## Configuración del entorno de prueba

### VM en Codespace
- **Software de Virtualización:** Oracle VM VirtualBox  
- **Sistema Operativo Huésped:** Ubuntu (64-bit)  
- **Memoria base:** 3,8 GB  
- **Almacenamiento virtual:** alrededor de 30 GB  
- **Controlador gráfico:** VMSVGA

### Configuración de Docker
Docker se usó dentro de un Codespace de GitHub.

- **CPU:** 2 vCPU  
- **RAM:** 4 GB (límite de configuración)  
- **Aplicación:** MySQL

## Resultados

Debido a que no he sido capaz de terminar mi proyecto, me baso en los datos de mis compañeros.

Para los resultados se tiene en cuenta que se cumplan todos los factores de aislamiento que puedan compartir ambos entornos.

Docker ha sobrepasado cualquier máquina virtual de varias formas:

- Está activo más rápidamente.  
- Consume menos CPU y memoria durante la ejecución.  
- Requiere menos espacio.  
- Es más consistente.

La VM puede llegar a superar a Docker en dos casos:

- Cuando se le asignan más recursos.  
- Por azar. La baja estabilidad no implica siempre bajo rendimiento.

En resumen, se ha probado en múltiples casos que no solo el rendimiento de Docker es mayor que el de cualquier máquina virtual, sino también su estabilidad con los resultados. Solo una máquina virtual de mayor tamaño podría superar a Docker, lo cual sigue demostrando su ineficacia y uso excesivo de recursos.

Teniendo en cuenta proporciones similares entre ambos sistemas, una máquina virtual siempre es menos eficiente que Docker.

## Análisis

| Aspecto           | Máquina Virtual | Docker        |
|-------------------|------------------|----------------|
| **Uso de recursos** | Alto             | Bajo           |
| **Tiempo de arranque** | Lento          | Rápido         |
| **Aislamiento**    | Mayor (kernel separado) | Menor (kernel compartido) |
| **Seguridad**      | Alta (debido al aislamiento) | Baja (debido al aislamiento) |

## Conclusión

Un aspecto importante es que los contenedores son populares debido a que comparten el sistema operativo del host, haciendo que requieran de menos recursos que una máquina virtual a la que tienes que dar el hardware. Esto hace que, por definición, tengan menor aislamiento, volviéndose menos seguros de utilizar que una máquina virtual.

Los datos de múltiples trabajos han demostrado que un contenedor Docker es más rápido que una máquina virtual, pero no lo hace una mejor opción que la máquina virtual debido a su falta de aislamiento.

**Yo prefiero usar una máquina virtual**, ya que, al instalar Docker en mi ordenador, he notado varios problemas causados por la falta de separación entre mi máquina física y Docker.

## Bibliografía

- [Repositorio de referencia](https://github.com/micastg4/Proyecto-TIC)





