# Bot-a_tu_toma

## Brief Description (<20 words)

App that automates the process of selecting classes for the Pontificia Universidad Católica de Chile.

## General Description

App that automates the process of selecting classes for the Pontificia Universidad Católica de Chile using the Selenium module for python.

It is capable to finish the process in under 2 seconds, while doing it manually takes more than 10 seconds.

## Descripción

Applicación que toma los ramos automáticamente para la UC, hecho con el módulo Selenium de Python. No guarda ningún tipo de información, por lo que una vez que el programa se cierra todos los datos ingresados son borrados, para tener mayor seguridad.

Termina el proceso en menos de 2 segundos, mientras que completar el proceso manualmente toma más de 10 segundos.

## Instrucciones de uso

1. Ingresar tus datos de la cuenta (solo Usuario UC, no el mail), contraseña.

2. Ingresar los NCR a tomar (Si se quieren tomar menos de 3, se pueden dejar en blanco).

3. Ingresar la hora en que tienes que tomar (está en formato de 24 horas, por lo que si es a las 2 pm, hay que ponerlo como 14:00).

4. Apretar el botón para comenzar entre 5 y 2 minutos antes de que comience tu banner (para que pueda abrir un navegador, iniciar sesión y entrar a las páginas requeridas).

5. Justo a la hora ingresada, el proceso va a comenzar, se va a meter a la página e inscribir todos los ramos.

6. El navegador que se abrió va a quedar abierto después de haber mandado la solicitud, ahí se puede revisar si las inscripciones fueron aceptados, o si por algún motivo (sobre créditos, no habían cupos) fue rechazada, y en el mismo navegador pueden seguir inscribiendo.

* En el caso de que se presente cualquier error (la constraseña es incorrecta, la hora es incorrecta, etc), el navegador quedará abierto para dar la opción de hacer el proceso manualmente.